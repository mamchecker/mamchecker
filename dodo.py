# -*- coding: utf-8 -*-
import os, os.path 
import fnmatch, shutil
from subprocess import check_output, CalledProcessError
import sys
import re
import pytest
import fnmatch

is_win = (sys.platform == 'win32')

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
def iteritems(d, **kw):
    return iter(getattr(d, "items" if PY3 else "iteritems")(**kw))

from doit.task import clean_targets

thisdir = os.getcwd()
basedir = os.path.dirname(__file__)
sphinxbase = os.path.join(basedir,'mamchecker')

def recursive_glob(pattern):
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return filter(lambda x: not any([x.find(w)>=0 for w in ['bottle','simpleauth','sympy']]), matches)

def task_included():
    '''tasks that find files (recursively) included by one rst file or tex file
    included:<file>
    included:recurse:<file>
    '''
    rstinclude = re.compile(r'\n\.\. (?:include|texfigure)::\s*(.*)')
    #[m.group(1) for m in rstinclude.finditer('\n\n.. texfigure:: test.tex\n')]
    texinput = re.compile(r'\n\\(?:input|include)\s*{([^}]*)}')
    #[m.group(1) for m in texinput.finditer('\n\n\\input{test}\n')]
    include_rexes = {'.rst':rstinclude,'.tex':texinput}
    def includes(filename,ext,rex):
        pathn,filen = os.path.split(filename)
        all_includes = set()
        with open(filename) as f:
            for m in rex.finditer(f.read()):
                included = m.group(1)
                fn,ex = os.path.splitext(included)
                if not ex:#\input can go without '.tex'
                    included = fn+ext
                included = os.path.join(pathn,included)
                all_includes.add(included)
        return {'file_dep':list(all_includes)}
    def recurse(mod, task, dependencies):
        return {'calc_dep': ["included:recurse:"+d for d in dependencies] ,
                'file_dep': list(dependencies)}
    for ext, rex in iteritems(include_rexes):
        allfn = recursive_glob('*'+ext)
        for fn in allfn:
            yield {'name': fn,
                   'actions': [(includes,[fn,ext,rex])],
                   'file_dep': [fn],
                   }
        for fn in allfn:
            yield {'name': 'recurse:'+fn,
                   'actions': [(recurse,(fn,))],
                   'calc_dep': ["included:"+fn],
                   'uptodate': [False],
                   }

def which_sphinx(totry = ['sphinx-build2','sphinx-build']):
    for sphinx in totry:
        try:
            if is_win:
                fndr = 'where '
            else:
                fndr = 'which '
            sphinx = check_output(fndr+sphinx,shell=True)
            return sphinx.splitlines()[0].strip()
        except CalledProcessError:
            pass
    raise Exception('None of '+', '.join(totry)+' found')

def task_html():
    r'''compile rst files in directory to html (body only) using sphinx

    From dir and dodo.py in ancestor dir:
        doit -kd. 
    In dodo.py directory:
        doit /path/to/rstdir 
    or 
        doit 

    conf.py and page.htm containing {{body}} must be in the base dir, i.e where dodo.py is.

    conf.py::

        import os.path
        extensions = ['sphinx.ext.mathjax','sphinxcontrib.tikz','sphinxcontrib.texfigure']
        templates_path = ['.']#i.e. same as conf.py and with page.html containing only {{body}}
        source_suffix = '.rst'
        source_encoding = 'utf-8'
        default_role = 'math'
        pygments_style = 'sphinx'
        tikz_proc_suite = 'ImageMagick'
        tikz_tikzlibraries = 'arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks'
        latex_elements = {
        'preamble': '\usepackage{amsfonts}\usepackage{amssymb}\usepackage{amsmath}\usepackage{siunitx}\usepackage{tikz}' 
            + """
            \usetikzlibrary{""" + tikz_tikzlibraries+ '}'
        }


    The rst file can have texfigure includes (or tikz or any other installed sphinxcontrib package)::
        
        .. texfigure:: diagram.tex
             :align: center

    The tex file can itself include other tex files (\input{othertexfile}).
    '''

    os.chdir(thisdir)#other task generators might have changed cwd

    sphinxbuild = [which_sphinx()]
    conf_py = ['-c',sphinxbase,'-Q']
    dfn = lambda n,v:['-D',n+'='+v]

    sphinxcmd = lambda srcpath,master,build: (sphinxbuild + conf_py +
            dfn('master_doc',master) +
            dfn('project',os.path.basename(srcpath)) +
            [srcpath,build])

    def move_images_if_any(build):
        try:
            imagepath = os.path.join(build, '_images')
            images = os.listdir(imagepath)
            imagedest = os.path.join(sphinxbase, '_images')
            if not os.path.exists(imagedest):
                os.makedirs(imagedest)
            for img in images:
                imgfile = os.path.join(imagepath,img)
                shutil.move(imgfile, os.path.join(imagedest,img))
        except OSError:
            pass
        return True

    sources = recursive_glob('*.rst')

    for src in sources:
        srcpath,srcname = os.path.split(src)
        name = os.path.splitext(srcname)[0]
        build = os.path.join(srcpath,'_build')
        tmptgt = os.path.join(build,name+'.html')
        #everything starting with _ is generated
        finaltgt = os.path.join(srcpath,'_'+name+'.html') 
        yield {'name':finaltgt+'<-'+src,
            'actions':[ sphinxcmd(srcpath,name,build),
                          (move_images_if_any,[build]),
                          ['mv', tmptgt, finaltgt],
                          ['rm', '-rf', build]
                         ],
            'file_dep':[src],
            'calc_dep':['included:recurse:'+src],
            'targets':[finaltgt],
            'clean':[clean_targets]}

### create new problem / content
# for content delete the __init__.py

from mamchecker.hlp import int_to_base26, base26_to_int, mklookup
import yaml

nextid_file = os.path.join(basedir,'nextids.yaml')
authors_file = os.path.join(basedir,'authors.yaml')

def author_next():
    #get author_id
    gitemail = check_output('git config --global --get user.email',shell=True).decode('utf-8').strip()
    with open(authors_file,'r') as f:
        authors = yaml.load(f)
    author = [author for author in authors if author['gitemail'] == gitemail][0]
    author_id = author['author_id']
    #get next_id for author
    with open(nextid_file,'r') as f:
        nextids = yaml.load(f)
    next_id = nextids[0][author_id]
    newnext = int_to_base26(base26_to_int(next_id)+1)
    nextids[0][author_id] = newnext
    with open(nextid_file,'w') as f:
        f.write('- \n')
        for k,v in nextids[0].items():
            #k,v = nextids[0].items()[0]
            ln = '  {0}:  "{1}"\n'.format(k,v)
            f.write(ln)
    return author, next_id

init_starter = '''# -*- coding: utf-8 -*-

from mamchecker.hlp import Struct
# randomize numbers using e.g. sample and randrange
import random 

def given():
    g = Struct()
    #fill g 
    return g

def calc(g):
    res = []
    #fill res
    return res

# remove if default norm_rounded works fine
# def norm(answers):
#     return norm_rounded(answers)

# remove if default equal_eq works fine
# def equal(a, r):
#     return equal_eq(a, r)
'''
    
lang_starter = '''%path = "path/goes/here"
%kind = "kindgoeshere"
%level = 0

%# text here

'''

def new_path():
    author, next_id = author_next()
    path = os.path.join(basedir,'mamchecker',author['author_id'],next_id)
    os.makedirs(path)
    return path

def newproblem(init_starter=init_starter,lang_starter=lang_starter):
    try:
        path = new_path()
        with open(os.path.join(path,'__init__.py'),'a') as f:
            f.write(init_starter)
        with open(os.path.join(path,'en'+'.html'),'a') as f:#author['default_lang']+'.html'),'a') as f:
            f.write(lang_starter)
        return path
    except OSError:
        raise OSError('ID path exists.')

rst_starter = '''.. raw:: html

    %path = "path/goes/here"
    %kind = kinda["<choose from languages.py/kinds[lang]>"]
    %level = 0 #in school years
    <!-- html -->

.. role:: asis(raw)
    :format: html latex

.. contents::

.. content here
'''

def newrst(rst_starter=rst_starter):
    try:
        path = new_path()
        with open(os.path.join(path,'en.rst'),'a') as f:#author['default_lang']+'.rst'),'a') as f:
            f.write(rst_starter)
        return path
    except OSError:
        raise OSError('ID path exists.')

def task_new():
    return {
            'actions':[new_path],
           }

def task_problem():
    return {
            'actions':[newproblem],
           }

def task_rst():
    return {
            'actions':[newrst],
           }


def task_initdb():

    import mamchecker.languages as languages
    import pprint

    def make_initdb():
        with open(authors_file,'r') as f:
            authors = yaml.load(f)

        inits = ['# -*- coding: utf-8 -*-',
                 '# generated file',
                 'from mamchecker.model import Index, index_add, delete_all',
                 'delete_all(Index.query())','']

        available_langs = set([])
        for author in authors:
            #author = authors[0]
            adir = author['author_id']
            authordir = os.path.join(sphinxbase,adir)
            allauthorIDs = [d for d in os.listdir(authordir) if not d.startswith('_')
                    and os.path.isdir(os.path.join(authordir,d))]
            for anid in allauthorIDs:
                #anid = allauthorIDs[1]
                def langcode(x): 
                    #x = '_de.html'
                    #x = '__pycache__'
                    lng_ext = x.split('.')
                    if len(lng_ext) == 2:
                        lng,ext = lng_ext 
                        return ext == 'html' and lng.strip('_')
                problemdir = os.path.join(authordir,anid)
                langfiles = [fl for fl in os.listdir(problemdir) 
                        if langcode(fl) in languages.languages]
                for langfile in langfiles:
                    #langfile = langfiles[0]
                    full = os.path.join(problemdir,langfile)
                    with open(full,'rb') as ff:
                        src = unicode(ff.read(),'utf-8')
                    defines = []
                    for ln in src.splitlines():
                        #ln = src.splitlines()[0]
                        lnstr = ln.strip()
                        if lnstr:
                            if not lnstr.startswith('%'):
                                break
                            lnstr1 = lnstr[1:]
                            defines.append(lnstr1)
                            if lnstr1.strip().startswith('level'):
                                break#level must be last define
                    deftext = u'\n'.join(defines)
                    lang = langcode(langfile)
                    available_langs.add(lang)
                    defs = {'kinda':languages.make_kinda(lang)}
                    try:
                        exec deftext in defs
                    except KeyError:
                        print(full)
                        raise
                    inits.append('index_add(u"{0}", u"{1}", "{2}", "{3}",\n        u"{4}")'.format(
                        adir+'.'+anid
                        ,lang
                        ,defs['kind']
                        ,defs['level']
                        ,defs['path']))
                    # TODO: make <em><i><b><strong> to keywords

        initdb = os.path.join(sphinxbase,'initdb.py')
        with open(initdb, 'w') as f:
            f.write('\n'.join(inits))
            f.write('\n\n')
            f.write('available_langs = ')
            f.write(pprint.pformat(available_langs,width=1))

        #assert that languages does not need more localization
        langdicts = [(k,o) for k,o in languages.__dict__.iteritems() 
                if not k.startswith('__') and isinstance(o,dict)]
        for k,o in langdicts:
            extendlangs = available_langs - set(o.keys())
            assert not extendlangs, k + ' in languages.py needs ' + ','.join(extendlangs)

    return {'actions':[make_initdb]}

CODE_FILES = [os.path.join(dirpath,f) 
        for dirpath, dirnames, files in os.walk('mamchecker')
        for f in fnmatch.filter(files,'*.py')]
TEST_FILES = [os.path.join(dirpath,f) 
        for dirpath, dirnames, files in os.walk('mamchecker')
        for f in fnmatch.filter(files,'test_*.py')]
PY_FILES = CODE_FILES + TEST_FILES
def run_test(test):
    return not bool(pytest.main(test))
def task_test():
    return {'actions':['py.test2'],
            'verbosity':2}
def task_cov():
    return {'actions':
                ["coverage2 run --parallel-mode `which py.test2` ",
                 "coverage2 combine",
                 ("coverage2 report --show-missing %s" % " ".join(PY_FILES))
                 ],
            'verbosity': 2}


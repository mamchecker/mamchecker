# -*- coding: utf-8 -*-

import datetime
import uuid
import hashlib
import re
import time
import logging
from itertools import chain
from bottle import SimpleTemplate
from urlparse import parse_qsl

#_initshell.py to initialize manually
from mamchecker.hlp import int_to_base26, datefmt
from mamchecker.kinds import make_kind0

from google.appengine.api.datastore_errors import BadKeyError

import webapp2
#http://blog.abahgat.com/2013/01/07/user-authentication-with-webapp2-on-google-app-engine/
import webapp2_extras.appengine.auth.models
from webapp2_extras import security


from google.appengine.ext import ndb
delete_all = lambda query: ndb.delete_multi(query.iter(keys_only=True))
def copy_all(model,oldkey,newkey):
    computed = [k for k,v in model._properties.iteritems() if isinstance(v,ndb.ComputedProperty)]
    for entry in model.query(ancestor=oldkey).iter():
        cpy = model(id=entry.key.string_id(),parent=newkey)
        cpy.populate(**{k:v for k,v in entry.to_dict().items() if k not in computed})
        cpy.put()

class User(webapp2_extras.appengine.auth.models.User):

    current_student = ndb.KeyProperty(kind = 'Student')

    def set_password(self, raw_password):
        #raw_password = "tstthis"
        self.password = security.generate_password_hash(raw_password, length=12)
    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp
        return None, None

class Secret(ndb.Model):#root
    secret = ndb.StringProperty() 

make_secret = lambda :str(uuid.uuid5(
                        uuid.UUID(bytes=datetime.datetime.now().isoformat()[:16]),
                        datetime.datetime.now().isoformat()))
stored_secret = lambda name: str(Secret.get_or_insert(name, secret = make_secret()).secret)

def gen_student_path(seed=None):
    ''' used if no federated user id
    >>> #myschool,myperiod,myteacher,myclass,myself = gen_student_path().split('-')
    '''
    if not seed:
        seed = datetime.datetime.now().isoformat()
    while len(seed)<16:
        seed = seed + datetime.datetime.now().isoformat().split(':')[-1]
    un = str(uuid.uuid5(uuid.UUID(bytes=seed[:16]),datetime.datetime.now().isoformat()))
    return un

class Base(ndb.Model):#root
    userkey = ndb.KeyProperty(kind = 'User') 
    created = ndb.DateTimeProperty(auto_now_add=True)

#these are roles 
#a user can have more such roles
class School(Base):#root
    pass
class Period(Base):#parent:School
    pass
class Teacher(Base):#parent:Period
    pass
class Class(Base):#parent: Teacher
    pass
class Student(Base):#parent: Class
    color = ndb.StringProperty()

myschool=School.get_or_insert('myschool')
myperiod=Period.get_or_insert('myperiod',parent=myschool.key)
myteacher=Teacher.get_or_insert('myteacher',parent=myperiod.key)
myclass=Class.get_or_insert('myclass',parent=myteacher.key)
myself = Student.get_or_insert('myself',parent=myclass.key)

def add_student(studentpath, color=None, user=None):
    school_,period_,teacher_,class_,student_ = studentpath
    school=School.get_or_insert(school_ or 'myschool' ,userkey=user and user.key) 
    period=Period.get_or_insert(period_ or 'myperiod' ,parent=school.key,userkey=user and user.key) 
    teacher=Teacher.get_or_insert(teacher_ or 'myteacher' ,parent=period.key,userkey=user and user.key) 
    clss=Class.get_or_insert(class_ or 'myclass' ,parent=teacher.key,userkey=user and user.key) 
    self=Student.get_or_insert(student_ or 'myself',parent=clss.key,
            userkey=user and user.key,color=color or '#EEE')
    if self.userkey==(user and user.key) and (color and self.color != color):
        self.color = color
        self.put()
    return self

#dict(filter(lambda x:isinstance(x[1],ndb.ComputedProperty),Problem._properties.iteritems()))
#[k for k,v in Problem._properties.iteritems() if isinstance(v,ndb.ComputedProperty)]
class Problem(Base):#parent: Student
    query_string = ndb.StringProperty()
    lang = ndb.StringProperty()
    given = ndb.PickleProperty()#the numbers randomly chosen, in python dict format
    created = ndb.DateTimeProperty(auto_now_add = True)
    answered = ndb.DateTimeProperty()
    collection = ndb.KeyProperty(kind = 'Problem')#links to a collection: 1-n, p.problem_set.get()!
    inputids = ndb.StringProperty(repeated=True)#a list of names given to the questions (e.g '1','2')
    results = ndb.StringProperty(repeated=True)#calculated from given, then standard formatted to strings
    oks = ndb.BooleanProperty(repeated=True)
    points = ndb.IntegerProperty(repeated=True)#points for this sub-problem
    answers = ndb.StringProperty(repeated=True)#standard formatted from input
    nr = ndb.IntegerProperty()#needed to restore order
    allempty = ndb.ComputedProperty(lambda self: ''.join(self.answers)=='')

    def link(self):
        return '/'+self.lang+'/?'+self.query_string

    @classmethod
    def from_resolver(cls,rsv,nr,parentkey):
        d = rsv.load()
        g = d.given()
        r = d.norm(d.calc(g))
        pkwargs = d.__dict__.copy()
        pkwargs.update(dict(
            g = g,
            answered = None,
            lang = rsv.lang,
            query_string = rsv.query_string,
            nr = nr,
            results = r,
            given = g,
            inputids = ["{:0=4x}".format(nr)+"_{:0=4x}".format(a) for a in range(len(r))],
            points = d.points or [1]*len(r or [])
            ))
        problem = cls(parent=parentkey,
            **{s:pkwargs[s] for s,v in cls._properties.items() if s in pkwargs})
        return problem, pkwargs

#e=myself.key
#dir(e)
keyparams = lambda k: '&'.join([r+'='+str(v) for r,v in k.pairs()])
#keyparams(e)
ctxkey = lambda x: ndb.Key(*list(chain(*zip(problemCtx[:len(x)],x))))
studentCtx = [k for k,v in myself.key.pairs()]
problemCtx = studentCtx+['Problem']
problemCtxObjs = [School,Period,Teacher,Class,Student,Problem]

def table_entry(s):
    if isinstance(s,Problem) and s.answered:
        problem_set = Problem.query(Problem.collection == s.key).order(Problem.nr)
        if problem_set.count():
            return [datefmt(s.answered),s.answers]
        else:
            return [datefmt(s.answered),s.oks,s.answers,s.results]
    elif isinstance(s,Student):
        return ['','','','',s.key.string_id()]
    elif isinstance(s,Class):
        return ['','','',s.key.string_id()]
    elif isinstance(s,Teacher):
        return ['','',s.key.string_id()]
    elif isinstance(s,Period):
        return ['',s.key.string_id()]
    elif isinstance(s,School):
        return [s.key.string_id()]
    elif isinstance(s, Assignment):
        now = datetime.datetime.now()
        overdue = now>s.due
        return [(datefmt(s.created),s.query_string),datefmt(s.due),overdue]
    #elif s is None:
    #    return ['no such object or no permission']
    return []

class Index(ndb.Model):
    #name = <query id>:<lang>, like 'r.i:de'
    path = ndb.StringProperty()
    knd = ndb.IntegerProperty()
    level = ndb.IntegerProperty()

def index_add(query, lang, kind, level, path):
    Index.get_or_insert(query+':'+lang, knd = int(kind), level = int(level), path = path)

def kvld(p_ll):#key_value_leaf_depth
    '''
    >>> p_ll = [('a/b','ab'),('a/c','ac'),('n/b','nb')]
    >>> list(kvld(p_ll))
    [('a', 'ab', False, '1a'), ('b', 'ab', True, '2a'), ('c', 'ac', True, '2b'), ('n', 'nb', False, '1b'), ('b', 'nb', True, '2c')]

    '''
    previous_set = set([])
    depths = []
    for p,ll in p_ll:
        keypath = p.split('/')
        this = set([])
        nkeys = len(keypath)
        for depth,kk in enumerate(keypath):
            if depth >= len(depths):
                depths.append(0)
            this.add(kk) 
            if this < previous_set:
                continue
            else:
                lvl_idx = str(depth + 1) + int_to_base26(depths[depth])
                depths[depth] = depths[depth] + 1
                yield (kk,ll,depth==nkeys-1,lvl_idx)
                previous_set = this.copy()

def filteredcontent(lang,opt=[]):
    #opt = [] #[('level', '2'), ('kind', 'exercise')]
    #lang = 'en'
    optd = dict(opt)
    knd_pathlink = {}
    itr = Index.query().iter()
    for e in itr:
        #e=itr.next()
        #knd_pathlink
        link, lng = e.key.string_id().split(':')
        if lng == lang:
            if 'level' not in optd or int(optd['level']) == e.level:
                if 'kind' not in optd or int(optd['kind']) == e.knd:
                    if 'path' not in optd or optd['path'] in e.path:
                        if 'link' not in optd or optd['link'] in link:
                            lpl = knd_pathlink.setdefault(e.knd,[])
                            lpl.append((e.path,(link,e.level)))
                            lpl.sort()
    knd0 = make_kind0(lang)
    s_pl = sorted(knd_pathlink.items())
    knd_pl = [(knd0[k], kvld(v)) for k,v in s_pl]
    #[('Problems', <generator>), ('Content', <generator>),... ]
    return knd_pl

def keysOmit(path):
    "[name1,name2,nonstr,...]->[key2,key2]"
    keys = []
    pth = map(lambda x: isinstance(x,str),path)
    ipth = pth.index(False) if False in pth else len(pth)
    if ipth > 0:
        keys = [ctxkey(path[:ipth])]*ipth
    return keys
def depth_1st(path = []
        ,keys = []#start keys, keysOmit(path) to skip initial hierarchy
        ,models = problemCtxObjs
        ,permission = False
        ,userkey = None
        ):
    ''' path entries are names or filters ([] for all)
    translated into keys along the levels given by **models** depth-1st-wise.
    >>> from mamchecker.test.hlp import problems_for
    >>> #del sys.modules['mamchecker.test.hlp']
    >>> path = ['a', 'b', 'c', 'd', 'e']
    >>> student = add_student(path, 'EEE')
    >>> problems_for(student)
    >>> lst = list(depth_1st(path+[[]]))
    >>> [k.get() for k in list(depth_1st(path+[[('query_string','=','r.u')]]))][0]._get_kind()
    'School'
    >>> path = ['a', 'b', 'c', 'x', 'e']
    >>> student1 = add_student(path, 'EEE')
    >>> problems_for(student1)
    >>> path = ['a','b','c',[],[],[('query_string','=','r.u')]]
    >>> list(depth_1st(path))[0].kind()
    'School'
    >>> list(depth_1st(path,keys=keysOmit(path)))[0].kind()
    'Class'
    >>> list(depth_1st())
    []
    
    '''
    N = len(models)
    if not path:
        path = [[]]*N
    while len(path)<N:
        path += [[]]
    i = len(keys)
    parentkey=keys and keys[-1] or None
    permission = permission or parentkey and parentkey.get().userkey == userkey
    if isinstance(path[i],str): 
        k = ndb.Key(models[i]._get_kind(), path[i], parent=parentkey)
        if k:
            yield k
            if i < N-1:
                keys.append(k)
                for e in depth_1st(path,keys,models,permission,userkey):
                    yield e
                del keys[-1]
    elif permission:
        q = models[i].query(ancestor=parentkey)
        #q = Assignment.query(ancestor=studentkey)
        if models[i]==Problem:
            q=q.order(Problem.answered)
        elif 'created' in models[i]._properties:
            q=q.order(models[i].created)
        for ap,op,av in path[i]:
            if ap in models[i]._properties:
                fn = ndb.FilterNode(ap,op,av)
                q=q.filter(fn)
        #qiter = q.iter(keys_only=True)
        for k in q.iter(keys_only=True):
            #k=next(qiter)
            yield k
            if i < N-1:
                keys.append(k)
                for e in depth_1st(path,keys,models,permission):
                    yield e
                del keys[-1]
    #else:
    #    yield None #no permission or no such object

def filter_student(qs):
    '''take out studentCtx and color
    >>> qs = 'School=b7034ff7&Period=3986&Teacher=527e&Class=9eed&Student=0&color=#EEE&bm&ws>0,d~1&b.v=3'
    >>> filter_student(qs)
    'bm&ws>0,d~1&b.v=3'

    '''
    qfiltered = filter(lambda x:x[0] not in studentCtx + ['color'],parse_qsl(qs,True))
    qsfiltered = '&'.join([k+'='+v if v else k for k,v in qfiltered])
    return qsfiltered

def set_student(request, user=None, session=None):
    '''logic for student role
    - there is a student role per client without user
    - there are more student roles for a user with one being current

    >>> request = webapp2.Request.blank('/')
    >>> request.response = request.get_response()
    >>> request.GET.update(dict(zip(studentCtx,[str(x) for x in range(len(studentCtx))])))
    >>> st=set_student(request)
    >>> request.student.key is not None
    True
    >>> #request.student.key.flat()

    '''
    request.student = None
    studentpath = [request.get(x) for x in studentCtx]
    color = request.get('color')
    request.query_string = filter_student(request.query_string)
    studentwithoutuser = 'studentwithoutuser'
    if ''.join(studentpath) != '':
        student = add_student(studentpath,color,user)
        if student.userkey == (user and user.key):
            request.student = student
        else:#student role does not belong to user, so don't change current student
            return 'message?msg=e'
    elif user:
        request.student =  user.current_student and user.current_student.get()
    elif session is not None and studentwithoutuser in session:
        try:
            request.student = ndb.Key(urlsafe=session[studentwithoutuser]).get()
        except (TypeError,BadKeyError,AttributeError):
            pass #no valid cookie available 
    if not request.student and user:
        request.student = Student.query(Student.userkey == user.key).get()
    if not request.student:#generate
        studentpath = gen_student_path(seed=request.remote_addr).split('-')
        request.student = add_student(studentpath, color, user)
    if user:
        if user.current_student != request.student.key:
            user.current_student = request.student.key
            user.put()
    elif session is not None:
        session[studentwithoutuser]=request.student.key.urlsafe()
    SimpleTemplate.defaults.update(dict(zip(problemCtx,problemCtxObjs)))
    SimpleTemplate.defaults["contextcolor"] = request.student.color or '#EEE'
    SimpleTemplate.defaults["keyparams"] = keyparams
    SimpleTemplate.defaults["ctxkey"] = ctxkey
    return request.student

class Assignment(Base):#parent: Student
    query_string = ndb.StringProperty()
    due = ndb.DateTimeProperty()

#teacherkey = ctxkey(['5ec07249','af76','56f2'])
#teacher = teacherkey.get()
#ass = list(assignable(teacherkey,teacher.userkey))
def assignable(teacherkey, userkey):
    for st in depth_1st(keys=[teacherkey], models=[Teacher,Class,Student], userkey=userkey):
        yield st

def normqs(qs):
    '''
    >>> qs = 'r.bm=1'
    >>> normqs(qs)
    'r.bm'
    >>> qs = 'r.bm=2'
    >>> normqs(qs)
    'r.bm=2'
    >>> qs = 'r.bm'
    >>> normqs(qs)
    'r.bm'
    >>> qs = 'r.bm&r.x=1'
    >>> normqs(qs)
    'r.bm&r.x=1'

    '''
    qparsed = parse_qsl(qs,True)
    if len(qparsed) == 1 and qparsed[0][1]=='1':
        return qparsed[0][0]
    return qs

#assign_to_student(student.key.urlsafe(), 'r.i&r.u', 1)
#assign_to_student(student.key.urlsafe(), 'r.s&r.v', 0)
#assign_to_student(student.key.urlsafe(), 'r.x=2', 0)
def assign_to_student(studentkeyurlsafe, query_string, duedays):
    now = datetime.datetime.now()
    studentkey = ndb.Key(urlsafe=studentkeyurlsafe)
    Assignment(parent=studentkey, query_string = normqs(query_string), 
            due = now + datetime.timedelta(days = int(duedays))).put()

#studentkey = ctxkey(['5ec07249','af76','56f2','7','6'])
#assign_to_student(studentkey.urlsafe(),'r.i=3',1)

#alla=Assignment.query().iter(keys_only=True)
#na = next(alla)
#na.parent()==studentkey
#allb=Assignment.query(ancestor=studentkey).iter(keys_only=True)
#nb = next(allb)

#follow a..
#Key('School', '5ec07249', 'Period', 'af76', 'Teacher', '56f2', 'Class', '7', 'Student', '6', 'Assignment', 4783425336639488)
#Key('School', '5ec07249', 'Period', 'af76', 'Teacher', '56f2', 'Class', '7', 'Student', '6')
#na1 = next(alla)
#na2 = next(alla)

#at = list(assigntable(student))
#s = at[0]
#studentkey = ctxkey(['5ec07249','af76','56f2','7','6'])
#userkey = studentkey.get().userkey
#list(assigntable(studentkey,userkey))
def assigntable(studentkey,userkey):
    #studentkey = student.key
    #akey=list(depth_1st(keys=[studentkey], models=[Student,Assignment]))[0]
    for e in depth_1st(keys=[studentkey], models=[Student,Assignment], userkey=userkey):
        yield e

def done_assignment(akey):
    if not akey:
        return False
    assignm = akey.get()
    q = Problem.query(ancestor=akey.parent()).filter(
            Problem.query_string==normqs(assignm.query_string)
            ,Problem.answered>assignm.created)
    if q.count() > 0:
        return True
    else:
        return False

def remove_done_assignments(studentkey,userkey):
    for s in assigntable(studentkey,userkey):
        if done_assignment(s):
            s.delete()



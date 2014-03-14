# -*- coding: utf-8 -*-

import os
import re
import webapp2
from urllib import pathname2url
from webtest import TestApp

import pytest #conftest.py will have been parsed

from mamchecker.app import make_app, app
from mamchecker.model import problemCtx

def test_routing():
    match = app.router.match(webapp2.Request.blank('http://mamchecker.appspot.com'))
    assert match[0].name == 'entry'
    assert match[1:][1] == {}
    match = app.router.match(webapp2.Request.blank('http://mamchecker.appspot.com/'))
    assert match[0].name == 'entry_'
    assert match[1:][1] == {}
    bl = webapp2.Request.blank('http://mamchecker.appspot.com/en')
    assert bl.query_string == ''
    match = app.router.match(bl)
    assert match[0].name == 'entry_lang'
    assert match[1:][1] == {'lang':'en'}
    bl = webapp2.Request.blank('http://mamchecker.appspot.com/en/?b')
    match = app.router.match(bl)
    assert match[0].name == 'entry_lang_'
    assert match[1:][1] == {'lang':'en'}
    bl = webapp2.Request.blank('http://mamchecker.appspot.com/en/content?r.a=2&r.b=3')
    match = app.router.match(bl)
    assert match[0].name == 'page'
    assert match[1:][1] == {'lang': 'en', 'pagename': 'content'}
    assert bl.query_string == 'r.a=2&r.b=3'
    assert int(bl.params['r.a'])==2 and int(bl.params['r.b'])==3
    bl = webapp2.Request.blank('http://mamchecker.appspot.com/en/test/sub?r.a=2&r.b=3')
    match = app.router.match(bl)
    assert match[0].name == 'page'
    assert match[1:][1] == {'lang': 'en', 'pagename': 'test/sub'}
    assert bl.query_string == 'r.a=2&r.b=3'
    assert int(bl.params['r.a'])==2 and int(bl.params['r.b'])==3

@pytest.fixture(scope='module')
def mamapp(request,gaetestbed):
    return TestApp(make_app())

#see
#http://stackoverflow.com/questions/12538808/pytest-2-3-adding-teardowns-within-the-class
#but cleanup is not necessary if testbed is in-memory
@pytest.mark.incremental
class TestRegistered(object):
    #>> self = TestRegistered()
    #>> self.setup(mamapp(finrequest,None))
    @classmethod
    @pytest.fixture(scope='class',autouse=True)
    def setup(cls,mamapp):
        cls.app = mamapp
        cls.resp = None
    @classmethod
    def _store(cls,name,value):
        setattr(cls,name,value)
    def _signup(self):
        self._store('resp',self.app.get('/de/signup'))
        assert 'POST' == self.resp.form.method
        #self.resp.showbrowser()
        self.resp.form[u'username']=u'tusername'
        #self.resp.form[u'username'].value
        self.resp.form[u'email']=u'temail@email.com'
        self.resp.form[u'password']=u'tpassword'
        self.resp.form[u'confirmp']=u'tpassword'
        self.resp.form[u'name']=u'tname'
        self.resp.form[u'lastname']=u'tlastname'
        r = self.resp.form.submit()
        self._store('resp',r.follow())
    def test_lang_redirect(self):
        r = self.app.get('/')
        assert '302' in r.status
        self._store('resp',r.follow())
        assert '/en' in self.resp.request.url
    def test_wrong_lang(self):
        r = self.app.get('/wrong')
        assert '302' in r.status
        self._store('resp',r.follow())
        assert '/en' in self.resp.request.url
    def test_wrong_page(self):
        r = self.app.get('/de/wrong')
        assert '302' in r.status
        self._store('resp',r.follow())
        assert '/de' in self.resp.request.url
    def test_wrong_content(self):
        r = self.app.get('/de/?wrong',status=404)
        assert '404' in r.status
    def test_register(self):
        self._signup()
        #self.resp.showbrowser()
        assert '/de/verification' in self.resp.request.url
    def test_logout(self):
        r = self.resp.goto('/de/logout')
        self._store('resp',r.follow())
        assert 'Twitter' in self.resp
        #self.resp.showbrowser()
    def test_registersame(self):
        self._signup()
        assert 'msg=a' in self.resp.request.url
    def test_anonymous(self):
        self._store('resp',self.resp.goto('/de/edits'))
        for p in problemCtx[:-1]:
            self.resp.form[p]='tst'
        #later we will check access permission
        self._store('resp',self.resp.form.submit())
    def test_anonym_exercise(self):
        self._store('resp',self.resp.goto('/de/?r.bu'))
        self.resp.form[u'0000_0000']=u'x'
        self._store('resp',self.resp.form.submit())
        assert '0P' in self.resp
    def test_login(self):
        self._store('resp',self.app.get('/de/login'))
        assert 'POST' == self.resp.form.method
        #self.resp.showbrowser()
        self.resp.form[u'username']=u'tusername'
        #self.resp.form[u'username'].value
        self.resp.form[u'password']=u'tpassword'
        r = self.resp.form.submit()
        self._store('resp',r.follow())
        #self.resp.showbrowser()
        assert '/de/todo' in self.resp.request.url
        assert 'Abmelden' in self.resp
    def test_password(self):
        self._store('resp',self.resp.goto('/de/password'))
        self.resp.form[u'password']=u'tpassword'
        self.resp.form[u'confirmp']=u'tpassword'
        r = self.resp.form.submit()
        self._store('resp',r.follow())
        assert 'msg=d' in self.resp.request.url
    def test_edits(self):
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"Schule")]/text()')
        self._store('curs',curx[1].strip())
        self._store('resp',self.resp.goto('/de/edits'))
        for p in problemCtx[:-1]:
            self.resp.form[p]='tst'
        self.resp.form[problemCtx[-2]]='U'
        self.resp.form['color'] = '#BBB'
        self._store('resp',self.resp.form.submit())
        assert 'edits' in self.resp.request.url
        assert 'tst' in self.resp
        assert '#BBB' in self.resp
    def test_registered_exercise(self):
        self._store('resp',self.resp.goto('/de/?r.bu'))
        self.resp.form[u'0000_0000']=u'x'
        self._store('resp',self.resp.form.submit())
        assert '0P' in self.resp
    def test_no_permission(self):
        self._store('resp',self.resp.goto('/de/done?tst&*&*'))
        cur = self.resp.lxml#tst does not belong to this user, therefore not listed
        tds = cur.xpath('//td[contains(text(),"tst")]/text()')
        assert len(tds) == 4
        trs = cur.xpath('//tr')
        assert len(trs) == 5
    def test_contexts(self):
        self._store('resp',self.resp.goto('/de/contexts'))
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"Schule")]//text()')
        assert curx[1].strip() != self.curs
        curh = cur.xpath('//a[contains(text(),"'+self.curs+'") and contains(@href,"todo")]/@href')[0]
        self._store('resp',self.resp.goto(curh))
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"Schule")]/text()')
        assert curx[1].strip() == self.curs
        #self.resp.showbrowser()
    def test_delete(self):
        self._store('resp',self.resp.goto('/de/edits'))
        self.resp.form['choice'] = '2'
        r = self.resp.form.submit()
        self._store('resp',r.follow())
        assert 'msg=g' in self.resp.request.url
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"Schule")]//text()')
        self._store('curs',curx[2].strip())
        assert self.curs == 'tst'
    def test_change_color(self):
        self._store('resp',self.resp.goto('/de/edits'))
        self.resp.form['choice'] = '1'
        self.resp.form['color'] = '#CDE'#only color
        self._store('resp',self.resp.form.submit())
        assert 'edits' in self.resp.request.url
        assert '#CDE' in self.resp
        #self.resp.showbrowser()
    def test_change_path(self):
        self._store('resp',self.resp.goto('/de/edits'))
        self.resp.form['Teacher'] = self.resp.form['Teacher'].value+'x'
        self.resp.form['choice'] = '1'
        r = self.resp.form.submit()
        self._store('resp',r.follow())
        assert 'msg=h' in self.resp.request.url
    def test_assign(self):
        self._store('resp',self.resp.goto('/de/content'))
        assert "Übungen" in self.resp
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"de/?")]/@href')
        assert probs
        for prob in probs:
            #prob = '/de/?r.bu'
            self._store('resp',self.resp.goto(prob))
            if len(self.resp.forms)>1:
                form = self.resp.forms[1] #assign
                assignees = form.fields.get('assignee')
                if assignees:
                    for a in assignees:
                        a.checked = True
                    res = form.submit('assign')
                    assert 'todo' in res.request.url
    def test_todo(self):
        self._store('resp',self.resp.goto('/de/todo'))
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"de/?")]/@href')
        assert probs
        for prob in probs:
            #prob = '/de/?r.bc'
            self._store('resp',self.resp.goto(prob))
            form = self.resp.forms[0]
            inps = form.fields.values()
            allnames = [i[0].name for i in inps]
            names = [n for n in allnames if n and re.match('\d+',n)]
            for n in names:
                #n=names[3]
                inp = form[n]
                if inp.attrs['type'] == 'text':
                    form[n] = '1.,-' 
                else:
                    form[n] = '1' 
            if 'submit' in allnames:
                res = form.submit('submit')
            assert "<form" not in res, prob
        self._store('resp',self.resp.goto('/de/todo'))
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"de/?")]/@href')
        assert probs == []
    def test_done_delone(self):
        self._store('resp',self.resp.goto('/de/done'))
        #self.resp.showbrowser()
        curx = self.resp.lxml
        delone = curx.xpath('//a[contains(@href,"de/?r.bb")]/../..//input')
        value = ''
        if 'value' in delone[0].keys():
            value = dict(delone[0].items())['value']
        if value:
            form = self.resp.form
            deletees = form.fields.get('deletee')
            d = [d for d in deletees if d._value==value]
            if d: 
                d = d[0]
                d.checked = True
        self._store('resp',form.submit('submit'))
        curx = self.resp.lxml
        delone = curx.xpath('//a[contains(@href,"de/?r.bb")]/../..//input')
        assert delone == [] #deleted
    def test_done_delall(self):
        self._store('resp',self.resp.goto('/de/done'))
        form = self.resp.form
        deletees = form.fields.get('deletee')
        for d in deletees:
            d.checked = True
        self._store('resp',form.submit('submit'))
        form = self.resp.form
        assert None == form.fields.get('deletee')
    def test_access_to_other_exercise(self):
        self._store('resp',self.resp.goto('/de/?r.bu'))
        self.resp.forms[0][u'0000_0000']=u'x'
        self._store('resp',self.resp.forms[0].submit())
        assert '0P' in self.resp
    def test_check_done(self):
        self._store('resp',self.resp.goto('/de/done'))
        curx = self.resp.lxml
        self._store('rbuhref',curx.xpath('//a[contains(text(),"r.bu")]/@href')[0])
        self._store('resp',self.resp.goto(self.rbuhref))
        assert '0P' in self.resp
    def test_check_done_outside(self):
        r = self.resp.goto('/de/logout')
        self._store('resp',r.follow())
        self._store('resp',self.resp.goto(self.rbuhref))
        assert '0P' in self.resp
        #self.resp.showbrowser()
    def test_list_done_from_parent(self):
        self._store('resp',self.resp.goto('/de/done?tst&*&*'))
        curx = self.resp.lxml
        u_student = curx.xpath('//td[contains(text(),"tst")]/text()')
        assert len(u_student)==1


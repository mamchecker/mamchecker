# -*- coding: utf-8 -*-

from docutils import nodes
from sphinx.util.compat import Directive

'''usage :inl:`r.cp`
to inline fragments'''

class inl(nodes.Inline, nodes.Element):
    pass

def inl_role(role, rawtext, text, lineno, inliner, option={}, content=[]):
    return [inl(text=text)], []

def visit_inl_node(self, node):
    self.body.append(self.starttag(
        node, 'span', CLASS=('inlined')))
    self.body.append("% include('{}')\n".format(node['text']))

def depart_inl_node(self, node):
    self.body.append('</span>')


'''usage :inline:`r.cp`
to inline non-fragments'''

class inline(nodes.Inline, nodes.Element):
    pass

def inline_role(role, rawtext, text, lineno, inlineiner, option={}, content=[]):
    return [inline(text=text)], []

def visit_inline_node(self, node):
    self.body.append(self.starttag(
        node, 'div', CLASS=('subproblem1')))
    self.body.append("% include('{}')\n".format(node['text']))

def depart_inline_node(self, node):
    self.body.append('</div>')

'''usage :lnk:`r.cp`
to reference content or excercises'''
class lnk(nodes.Inline, nodes.Element):
    pass

def lnk_role(role, rawtext, text, lineno, lnkiner, option={}, content=[]):
    return [lnk(text=text)], []

def visit_lnk_node(self, node):
    self.body.append('{{{{!util.a("{0}")}}}}'.format(node['text']))

def depart_lnk_node(self, node):
    pass

def setup(app):
    app.add_node(inl,
                 html=(visit_inl_node, depart_inl_node))
    app.add_node(inline,
                 html=(visit_inline_node, depart_inline_node))
    app.add_node(lnk,
                 html=(visit_lnk_node, depart_lnk_node))

    app.add_role('inl', inl_role)
    app.add_role('inline', inline_role)
    app.add_role('lnk', lnk_role)


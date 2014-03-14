# -*- coding: utf-8 -*-

import random
from sympy import latex, Poly, Rational
from sympy.abc import x

from mamchecker.hlp import Struct, norm_frac as norm

__all__ = ['given','calc','norm','tex_lin']

def tex_lin(a,b):
    p=Poly([a,b],x,domain='QQ')
    return latex(p.as_expr())

def given():
    #ax+b=cx
    a,c = random.sample(range(2,10)+range(-9,-2),2)
    da,dc = random.sample(range(2,4)+range(-3,-1),2)
    xx = random.sample(range(1,6)+range(-5,0),1)[0]
    b = (Rational(c,dc) - Rational(a,da)) * xx
    g = Struct(a=Rational(a,da),b=b,c=Rational(c,dc))
    return g

def calc(g):
    return [1.0*g.b/(g.c-g.a)]

# -*- coding: utf-8 -*-

import numpy as np
import random

from mamchecker.hlp import Struct

def given():
    while True:
        A = np.array(random.sample(range(1,19)+range(-19,-1),4))
        A.shape=(2,2)
        try:
            np.linalg.inv(A)
        except:
            continue
        break
    x = np.array(random.sample(range(2,9)+range(-9,-2),2))
    b = np.dot(A,x)
    A = A.tolist()
    b = b.tolist()
    g = Struct(A=A,b=b)
    return g

def calc(g):
    iA = np.linalg.inv(np.array(g.A))
    x = np.dot(iA,np.array(g.b))
    return [i for i in x.round().tolist()]


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 16:40:10 2019

@author: sehaj
"""

import matplotlib.pyplot as plt

labs = ['Spent', 'Limit']
vals = [10, 120]
colors = ("red", "green")

figureObject, axesObject = plt.subplots()
wedges, texts = axesObject.pie(vals, labels = labs, colors = colors,  wedgeprops=dict(width=0.3), startangle= 90)


axesObject.axis('equal')

plt.show()
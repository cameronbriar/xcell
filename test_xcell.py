#!/usr/bin/env/ python

"""
Tests for xCell.py
"""

import sys


# Simple quota definitions
# These are located in 'test_simple.txt' and 'test_complex.txt'
QUAL_QUOTA = """
--defines
qual|plus
+
--qualified
# = Qualified
qual|150
+
"""
COMPLEX_QUOTA = """
--defines
qual|plus
age1|Q1.check('0-9')
age2|Q1.check('10-19')
age3|Q1.check('20-29')
age4|Q1.check('30-39')
age5|Q1.check('40-49')
age6|Q1.check('50-59')
age7|Q1.check('60-69')
age8|Q1.check('70-79')
age9|Q1.check('80-89')
Male|Q2.r1
Female|Q2.r2
+
--qualified
# = Qualified
qual|5000
+
--general
# = Age
age1|10
age2|10
age3|10
age4|10
age5|10
age6|10
age7|10
age8|10
age9|10

# = Gender
Male|100
Female|100

# = Gender / Age|age1|age2|age3|age4|age5|age6|age7|age8|age9
Male
Female
+
"""

# Load xc class from xCell.py
from xcell import XC

xc = XC()


# -- Test #1 --
# BUILD - Given a well-written quota, return sheetnames and marker definitions
def test_build_and_compile_proper_quota():
    sheets, markers = xc.build('test_simple.txt')

    assert len(sheets) == len(markers)
    assert type(sheets[0]) == str

# -- Test #2 --
# CONVERT - Given a pre-existing quota xls file, convert to txt file
def test_convert_proper_quota():
    xc.convert('xquota.xls')

test_build_and_compile_proper_quota()
test_convert_proper_quota()

print '\n\nAll tests passed!'

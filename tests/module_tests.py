# -*- coding:utf-8 -*-

from nose.tools import *
import re

from modules import dbutils

def setup():
    print ("\nmodules test start")
    
def teardown():
    print ("\nmodules test end")
    
def test_wanip():
	assert_regexp_matches(wanip.query(), r'(\d*)\.(\d*)\.(\d*)\.(\d*)')

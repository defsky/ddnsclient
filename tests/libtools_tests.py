# -*- coding:utf-8 -*-

from nose.tools import *
import re

from libtools import wanip

def setup():
    print ("\nmodule libtools test start")
    
def teardown():
    print ("\nmodule libtools test start")
    
def test_wanip():
	assert_regexp_matches(wanip.query(), r'(\d*)\.(\d*)\.(\d*)\.(\d*)')
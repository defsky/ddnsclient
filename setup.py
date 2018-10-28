# -*- coding:utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'name' : 'ddnsclient',
    'version' : '0.1',
    'license' : 'MIT License',
    
    'description' : 'ddns client',
    'long_description' : 'long description for project',
    'keywords' : ('test','xxx'),
    
    'author' : 'def',
    'author_email' : 'defsky@qq.com',
    'url : 'URL to get it at.'.
    'download_url' : 'Where to download it.',
    
    'platforms' : 'any',
    'packages' : ['libtools'],
    'install_requires' : ['nose'],
    'scripts' : [],
    'entry_points' : {
        'console_scripts' : [
            'ddnsclient = test.help:main'
        ]
    }
    
    #fix windows error when uninstall
    'zip_safe' : False
}

setup(**config)
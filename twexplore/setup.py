#setup.py

## This file is used to build the twexplore.exe program
## from this source. It uses the excellent py2exe package,
## which is available at:
##
## http://starship.python.net/crew/theller/py2exe
##
## Command:
##    python setup.py py2exe

from distutils.core import setup
import py2exe

setup(name='twexplore',
        windows=['twexplore.py'
])

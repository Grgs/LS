#!/usr/bin/env python3
'''compile ls.py'''
import compileall
import py_compile

compileall.compile_dir('./', force=True)
py_compile.compile('./ls.py', cfile='cls.pyc', optimize=2)

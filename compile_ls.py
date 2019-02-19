#!/usr/bin/env python3
'''compile ls.py'''
import compileall
import py_compile

compileall.compile_dir('./ls/', force=True)
py_compile.compile('./ls/ls.py', cfile='cls.pyc', optimize=2)

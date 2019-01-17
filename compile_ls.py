#!/usr/bin/env python3
"""compile ls.py"""
import py_compile
import compileall

compileall.compile_dir('./', force=True)
py_compile.compile("ls.py", cfile="cls.pyc", optimize=2)

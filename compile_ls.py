#!/usr/bin/env python3
"""compile ls.py"""
import py_compile

py_compile.compile("ls.py", cfile="cls.pyc", optimize=2)

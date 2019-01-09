#!/usr/bin/env python3
import os

with os.scandir('.') as osscandir:
    for d in osscandir:
        print('{:<12}{:>60}'.format(d.stat().st_size, d.name))


#!/usr/bin/env python3
import sys
sys.path.append('.')

import ast
from evality import purifier
from testsimple import *

plan(tests=8)

ok(purifier.Purifier, 'Purifier object exists')
ok(purifier.Purifier.visit, 'Purifier has visit method')

def raises_exception(code):
    p = purifier.Purifier()

    ok(p, 'Got purifier object')
    tree = ast.parse(code)

    try:
        p.visit(tree)
        return False
    except purifier.Insecure:
        return True

diag('Purify clean code')

code = '''
a = "Hello"
b = 5
print(a * b)
'''

ok(not raises_exception(code), 'Code should not raise an exception')

diag('Purify code with imports')

code = '''
import requests
'''

ok(raises_exception(code), 'Code raised an exception')

diag('Purify code with from import')

code = '''
from requests import get
'''

ok(raises_exception(code), 'Code raised an exception')

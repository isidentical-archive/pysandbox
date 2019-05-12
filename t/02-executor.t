#!/usr/bin/env python3
import sys
sys.path.append('.')

from evality.executor import execute
from testsimple import *

plan(tests=10)

ok(execute, 'Execute method exists')

diag('Basic contract')

res = execute('')
ok(res)
ok('out' in res)
ok('err' in res)
ok(not res['out'])
ok(not res['err'])

diag('Getting stdout')

res = execute('print("Test message")')
ok(res['out'] == 'Test message\n')
ok(not res['err'])

diag('Multiline test')

res = execute('''
result = "Hello, "

for c in "World!":
    result += c

print(result)
''')

ok(res['out'] == 'Hello, World!\n')
ok(not res['err'])

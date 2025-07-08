import re
import sys

backend = open('backend/main.py').read()
if '/export/frontend' in backend:
    docs = open('README.md').read()
    if '/export/frontend' not in docs:
        print('Docs missing /export/frontend')
        sys.exit(1)
print('Documentation check passed')

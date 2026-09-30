"""Write the last inline <script> of index.html to m3.js (LF line endings) for the node harness."""
import os, re
here = os.path.dirname(os.path.abspath(__file__))
h = open(os.path.join(here, '..', '..', 'index.html'), encoding='utf-8').read().replace('\r\n', '\n')
s = re.findall(r'<script>(.*?)</script>', h, flags=re.S)[-1]
open(os.path.join(here, 'm3.js'), 'w', encoding='utf-8', newline='\n').write(s)

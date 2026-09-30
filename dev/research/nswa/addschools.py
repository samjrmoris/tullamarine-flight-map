import sys,re
path='raw.txt'
s=open(path).read()
sub=sys.argv[1]
lines=sys.stdin.read().strip().splitlines()
m=re.search(r"#"+re.escape(sub)+r"\|\d+\n",s); assert m, sub
s=s[:m.end()]+"".join("S "+x.strip()+"\n" for x in lines if x.strip())+s[m.end():]
open(path,'w').write(s)

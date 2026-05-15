import os, sys, re, codecs, binascii, cgi, cgitb


print("Content-type: text/html; charset=utf-8\n\n")
print("<h3>Test</h3>")

#for s in os.environ:
#    print(f"<br>{s}: {os.environ[s]}")


q = cgi.FieldStorage();
print(q.getvalue("f6", "Default"))

exit()

q = os.environ["QUERY_STRING"]
print(q)
l = q.split('&')
inp = {}
for p in l:
    (n, v) = p.split('=')
    inp[n] = v;
    
    
print(inp)

print(inp['f1'])
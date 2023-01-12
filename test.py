s = "mail2kv@kvsangathan.kvs.in"
s = s.split("kv")
op = s[0] + "@kv" + s[2]
print(op)

i = "1#2#3#4##5#6###"
print(i.split("#"))

d = {1: "a", 2: "b"}
print(d)
D = {'rno': 32, 'name': 'Ms Archana', 'subject': [
    'hindi', 'english', 'cs'], 'marks': (85, 75, 89)}
print(D)
D['subject'][2] = 'IP'
# D['marks'][2]=80
str = "My program is program for you"
l = str.partition("program")
print(l)
data = {'a': 300, "a": 800}
print(data)


def change(m, n=10):
    global x
    x += m
    n += x
    m = n+x
    print(m, n, x)


x = 20
change(10)
change(20)

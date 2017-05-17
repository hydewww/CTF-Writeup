from ctypes import *
import telnetlib

road = CDLL('./road.dylib')

def judge(ans):
    if ans:
        return b'yes\n'
    else:
        return b'no\n'

if __name__ == '__main__':
    tn = telnetlib.Telnet('10.105.42.5', 44444)
    road.init()

    o = tn.read_until(b'(press enter to continue)\n')
    print(o.decode('utf-8'))
    tn.write(b'\n')

    o = tn.read_until(b'\n')
    print(o.decode('ascii'))

    for i in range(799):
        x, y = [int(j) for j in tn.read_until(b'\n').split(b' ')]
        road.combine(x, y)

    tn.read_until(b'\n')
    print(o.decode('ascii'))

    while True:
        o = tn.read_until(b'\n')
        print(o.decode('ascii'))

        inp = tn.read_until(b'\n')
        print(inp.decode('ascii'))
        x, y = [int(j) for j in inp.split(b' ')]
        a = road.query(x, y)

        o = tn.read_until(b'\n')
        print(o.decode('ascii'))

        tn.write(judge(a))
        print(judge(a).decode('ascii'))


while True:
    o = tn.read_until(b'\n')
    print(o.decode('ascii'))
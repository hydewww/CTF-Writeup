import telnetlib

def judge(x: int, y: int):
    return pow(x, y, 10000)


def nice(i: str):
    x, y = [int(a) for a in i.split(b' ')]
    res = judge(x, y)
    return str(res).encode('ascii')

if __name__ == '__main__':
    tn = telnetlib.Telnet('10.105.42.5', 42222)

    while True:
        o = tn.read_until(b'here are for you\n')
        print(o.decode('utf-8'))
        num = tn.read_until(b'\n')
        print(num.decode('ascii'))
        o = tn.read_until(b'\n')
        print(o.decode('ascii'))

        tn.write(nice(num) + b'\n')
        print(nice(num).decode('ascii'))

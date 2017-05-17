import telnetlib

def judge(total: int, max_take: int):
    return total % (max_take + 1)


if __name__ == '__main__':
    tn = telnetlib.Telnet('10.105.42.5', 43333)

    for i in range(1, 51):
        o = tn.read_until(b'%d--------------------\n' % i)
        print(o.decode('utf-8'))
        num = tn.read_until(b'\n')
        print(num.decode('ascii'))

        total, max_take = [int(a) for a in num.split(b' ')]

        while True:
            o = tn.read_until(b'\n')
            print(o.decode('ascii'))

            inp = b'%d\n' % judge(total, max_take)
            tn.write(inp)
            print(inp.decode('ascii'))

            if total <= max_take:
                o = tn.read_until(b'\n')
                print(o.decode('ascii'))
                break
            else:
                o = tn.read_until(b'left ')
                print(o.decode('ascii'))

                n = tn.read_until(b'\n')
                total = int(n)
                print(n.decode('ascii'))


    while True:
        o = tn.read_until(b'\n')
        print(o.decode('ascii'))
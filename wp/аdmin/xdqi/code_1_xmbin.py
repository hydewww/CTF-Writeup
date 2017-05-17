#!/usr/bin/env python3
import telnetlib
from math import log10, ceil

def judge(i: int):
    str_num = str(i)
    len_num = len(str_num)
    digits = [int(i) for i in str_num]

    total = 0
    while True:
        if int(''.join([str(i) for i in digits])) == 0:
            break
        for i in range(len_num):
            if digits[i] > 0:
                digits[i] -= 1
        total += 1

    return total


def nice(i: str):
    res = judge(int(i))
    return str(res).encode('ascii')

if __name__ == '__main__':
    tn = telnetlib.Telnet('10.105.42.5', 41111)

    while True:
        o = tn.read_until(b'The number:\n')
        print(o.decode('gbk'))
        num = tn.read_until(b'\n')
        print(num.decode('ascii'))
        o = tn.read_until(b'\n')
        print(o.decode('ascii'))

        tn.write(nice(num) + b'\n')
        print(nice(num).decode('ascii'))

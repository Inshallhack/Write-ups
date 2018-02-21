#!/usr/bin/env python3

from binascii import unhexlify as unhexlify

ME_FLAGE = '<censored>'

def flip(num):
    '''
        flip(1234567) = 7654321 so flip(flip(x)) = x
        @param num : int
        @output int
    '''
    out = 0
    while num != 0:
        out = (out * 10) + (num % 10)
        num //= 10
    return out

def parseInt(txt):
    '''
        parseInt produce the same output as the built in fonction int.
        ex: parseInt("1337") = int("1337") = 1337
        @param txt : String
        @output int
    '''
    out = 0
    for c in txt:
        out *= 10
        out += ord(c) - ord('0')
    return out

def main():
    flaginput = input()[:7]
    print(flaginput)
    if not flaginput.isdigit():
        print("that's not a number lol")
        return

    #flaginput = ???????
    a = parseInt(flaginput)
    #a = 2365552391
    a = flip(a)
    #a = 1932555632
    b = hex(a)[2:].zfill(8)[-8:]
    #b = "73307570"
    if unhexlify(b) == 's0up'.encode():
        #here we need b = "s0up".encode('hex') = 0x73307570 = 1932555632 
        print("oh yay it's a flag!", ME_FLAGE)
    else:
        print('oh noes rip u')

if __name__ == '__main__':
    main()




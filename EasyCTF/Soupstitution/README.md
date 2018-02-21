# Soupstitution Cipher
Reverse Engineering - 150 points

## Challenge 

> We had a flag, but lost it in a mess of alphabet soup! Can you help us [find it?](soupstituted.org.py)

> Connect to the server via `nc c1.easyctf.com 12484`.

## Solution

### First glance


The challenge program is ~~obfusced~~ souped.

![org](https://github.com/Inshallhack/Write-ups/raw/master/EasyCTF/Soupstitution/soupstituted.py.png)
	

### beautify the program:


I've refactored the program like this:

![beautify](https://github.com/Inshallhack/Write-ups/raw/master/EasyCTF/Soupstitution/soupstituted.cleaned.py.png)
	

### what i'm looking for ?


As you can see, if we send "2365552391" as input the program should return the flag. but unfortunately the length of the input is limited to 7 characters.

So we have to find another input that returns "2365552391" after the parseInt function.


### Python3 my love


After a long search time I noticed that in Python3 the function isdigit() is not limited to the simple ASCII character like in python2 but works with utf8 and unicode characters.

So we need to generate a list of characters that pass the isdigit() condition in python3.

```
dico = [chr(i) for i in range(9999) if chr(i).isdigit()][::-1]
```

### Bruteforce (or not)


```
>>> len(dico)
358
```
As you can see, there are 358 characters who pass the isdigit() condition in the first 9999 characters.

My first idea was to bruteforce the 7 characters with 358 characters. But, having calculated the number of possibilities I have forgotten this solution.

```
>>> pow(len(dico),7)
753669927250029952
```

### Use my brain (and maybe lose some time)


So I looked more at the parseInt function. It works like this:

```
parseInt('123') =>

out = 0
out = 0
out += ord('1') - ord('0') = 49 - 48 = 1
out = 10
out += ord('2') - ord('0') = 50 - 48 = 12
out = 120
out += ord('3') - ord('0') = 51 - 48 = 123
```

```
but now if we take 'A23' =>

out = 0
out = 0
out += ord('A') - ord('0') = 65 - 48 = 17
out = 170
out += ord('2') - ord('0') = 50 - 48 = 172
out = 1720
out += ord('3') - ord('0') = 51 - 48 = 1723
```

As we can see, we now have one more digit in the output that great.

#### Found the solution


Remember we want 2365552391 as output with only 7 characters. we can split 2365552391 like this 2365 5 5 2 3 9 1 or 236 55 5 2 3 9 1 or 23 65 55 2 3 9 1 and so on.

So we have to find a solution that passes the isdigit condition. Lets try this with the first one :

```
>>> chr(2365 + ord('0')).isdigit()
True
```

wow! first time :)

So one of the correct input is :  chr(2365 + ord('0')) + "5" + "5" + "2" + "3" + "9" + "1" = "७552391"

we sended it to the online service and we received the flag.


> easyctf{S0up_soup_soUP_sOuP_s0UP_S0up_s000000OOOOOOuuuuuuuuppPPppPPPp}
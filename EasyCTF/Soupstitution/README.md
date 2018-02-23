# Soupstitution Cipher
Reverse Engineering - 150 points

## Challenge 

> We had a flag, but lost it in a mess of alphabet soup! Can you help us [find it?](soupstituted.org.py)

> Connect to the server via `nc c1.easyctf.com 12484`.

## Solution

### First glance

The program provided is ~~obfuscated~~ souped.

![org](https://github.com/Inshallhack/Write-ups/raw/master/EasyCTF/Soupstitution/soupstituted.py.png)
	
Let's clean that up!

### Beautifying the program

After refactoring the program, it looks like this:

![beautify](https://github.com/Inshallhack/Write-ups/raw/master/EasyCTF/Soupstitution/soupstituted.cleaned.py.png)
	

### What are we looking for?

As you can see, if we provide the string **2365552391** as input to the
program, it should return the flag. Unfortunately, the length of the input is
limited to 7 characters.

So we have to find another input that translates to **2365552391** after the
call to `parseInt`.

### Python 3, my love…

After searching for a long time, I noticed that unlike in Python 2, the
`isdigit` function is not limited to ASCII-encoded inputs but also accepts
UTF-8 or Unicode-encoded strings in Python 3.

```python
dico = [chr(i) for i in range(9999) if chr(i).isdigit()]
```

### Bruteforcing (or not)


```python
>>> len(dico)
358
```

As you can see, 358 characters out of the first 9999 pass the `isdigit`
condition.

My first idea was to bruteforce which 7 characters to use; checking the number
of possibilities quickly ruled out that possibility.

```python
>>> pow(len(dico),7)
753669927250029952
```

### Actually using my brain (and maybe losing some time)

Let's look at `parseInt` some more; it basically works like this:

```python
# parseInt('123') =>

out = 0
out = 0
out += ord('1') - ord('0') = 49 - 48 = 1
out = 10
out += ord('2') - ord('0') = 50 - 48 = 12
out = 120
out += ord('3') - ord('0') = 51 - 48 = 123
```

```python
# but what if we take 'A23' as input =>

out = 0
out = 0
out += ord('A') - ord('0') = 65 - 48 = 17
out = 170
out += ord('2') - ord('0') = 50 - 48 = 172
out = 1720
out += ord('3') - ord('0') = 51 - 48 = 1723
```

As we can see, we now have one more digit in our output! Success!

#### Solving the problem

Remember that we want `parseInt` to output **2365552391** based on an input of
at most 7 characters. The key here is that we can split **2365552391** in
a lot of different ways, such as **[2365, 5, 5, 2, 3, 9, 1]** or **[236, 55, 5,
2, 3, 9, 1]** or **[23, 65, 55, 2, 3, 9, 1]**, and so on.

Let's try to find characters of interest that pass the `isdigit` check. Let's
try with **2365**:

```python
>>> chr(2365 + ord('0')).isdigit()
True
```

Yup, first try! :-)

This means that a possible input would be:
```python
chr(2365 + ord('0')) + "5" + "5" + "2" + "3" + "9" + "1" = "७552391"
```

Sending it to the online service, and… **Flagged!**
we sended it to the online service and we received the flag.

**Flag:** `easyctf{S0up_soup_soUP_sOuP_s0UP_S0up_s000000OOOOOOuuuuuuuuppPPppPPPp}`


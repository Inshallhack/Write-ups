# Ecoin

## Challenge description

> ecoin - hard
> I think I'm getting crazy! I see things in things. Like this: PDF

The PDF file : [https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/ecoin_vuln_notes.pdf](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/ecoin_vuln_notes.pdf)

## First glance
First, I opened the PDF and did not notice anything out of the ordinary. This PDF contains an advertisement for Ecoin (*wink to Mr.Robot*) as well as a blank page *"[This page unintentionally left blank]"*.

I then issued some basic forensics-related commands :

```bash
pdfinfo ecoin_vuln_notes.pdf
```
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/1.png)
```
Syntax Error (1288034): Missing 'endstream' or incorrect stream length
```

That's interesting. Let's check it out:

```bash
binwalk ecoin_vuln_notes.pdf
```
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/2.png)

I see a split ZIP file at the end of the PDF.
Let's try to extract it.
## Part II - Extract the ZIP file
First step,
retrieving the pieces of the ZIP file in the PDF:

To do this I make use of the information previously retrieved using binwalk and the `dd` command,
and then I use the  `zip -FF` command to check the file and fix it if needed:
```
zip -FF ecoin-merged.zip --out ecoin.zip
```
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/3.1.png)

and now I can extract it:

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/3.2.png)

F.CK

Ok, I need a password to extract **hint.pdf**.

I reread the binwalk output and notice something peculiar. In the PDF, I can only see one picture, but in the binwalk I see a PNG and a JPEG file. Weird.

The `pdfextract` (*origami*) command allows me to extract both files. YEAH! The JPEG file seems very interesting :)

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/extracted.jpg)
 
Let's try *"Pure_Funk"* as password for the ZIP.
 
**It works. :-)**

So now, we have two new files, **flag.png** and **hint.pdf**.

flag.png:
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/flag.png)

hint.pdf:
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/hint.pdf.png)



## Part II - Recover the flag

I open hint.pdf and notice something strange at the top. I do a CTRL+A, CTRL+C and CTRL+V in SublimeText and obtain the following result:
```
AES IV: F01D86CDBB7E1CD88815BEB4106A558C
```

Very, very, very promising.

I summarize: we have a *JPEG file* containing the text "Pure_Funk", a *flag.png* file that is unusable in the current state and a *hint.pdf* file containing an **AES IV** as well as the text **"AngeWouldLoveIt!"**.

I immediately think of a [https://speakerdeck.com/ange/funky-file-formats-31c3](presentation) from 31C3 by **Ange Albertini** called *"Funky File Formats"*.

In this presentation, there was a POC called **"Angecryption"**. This POC showed that **it is possible to retrieve a valid file from another valid file by encrypting it or decrypting it using a block cipher and a well-chosen IV**.

Let's try this.

```python
from Crypto.Cipher import AES

IV="F01D86CDBB7E1CD88815BEB4106A558C".decode('hex')

key = "AngeWouldLoveIt!"

aes = AES.new(key, AES.MODE_CBC, IV)

with open("flag.png", "rb") as f:
	d = f.read()

d = aes.encrypt(d)

with open("out", "wb") as f:
	f.write(d)

```

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/arf.png)

Arff… :(

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/whew.png)

Whew! :)

So, after encrypting *flag.png* using **AES**, I obtain a new PNG file.

The image is a white square containing transparent holes, I name it *mask.png*, and merge both images together to obtain the following result:

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/flagged.png)

YES, that is the flag! :)

**Flag**: 34c3_F1L3_FORMA7S_AR3_COMMUN17Y_CONNEC7ORS

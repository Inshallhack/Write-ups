# Ecoin

## Challenge description

> ecoin - hard

> I think I'm getting crazy! I see things in things. Like this: PDF

The pdf file : [https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/ecoin_vuln_notes.pdf](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/ecoin_vuln_notes.pdf)

## First look
First, I opened the PDF and did not see anything particular. This PDF contains an advertisement for Ecoin (wink to Mr.Robot) and a blank page '[This page unintentionally left blank]'.

I then made some basic forensic commands :

```
pdfinfo ecoin_vuln_notes.pdf
```
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/1.png)
```
Syntax Error (1288034): Missing 'endstream' or incorrect stream length
```
that's interesting. Let's go watch this :

```
binwalk ecoin_vuln_notes.pdf
```
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/2.png)

I see a ZIP file splited at the end of the PDF.
Let's try to extract it.
## Part II - Extract the zip file
First stage,
retrieve the pieces of the ZIP file in the PDF :

To do this I use the binwalk's information previously retrieved and the DD command.
then I used the command zip -FF to check and repare the ZIP if needed
```
zip -FF ecoin-merged.zip --out ecoin.zip
```
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/3.1.png)

and now we can extract it :

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/3.2.png)

F.CK

Ok, I need a password to extract the hint.pdf

I reread the binwalk and something appear to me weird. In the pdf I see only one picture but in the binwalk I see a png and a jpeg file. weird.
The pdfextract (origami) command allows me to get this png and jpeg and YEAH the jpeg file seems very interesting :)

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/extracted.jpg)
 
 Let's try "Pure_Funk" as password for the zip..
 
 Yeah it's works :)

So now, we have two new files, flag.png and hint.pdf

flag.png:
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/flag.png)

hint.pdf:
![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/hint.pdf.png)



## Part II - Recover the flag

I opened hint.pdf and noticed something strange at the top. I did a CTRL + A CTRL + C and CTRL + V in SublimeText :
```
AES IV: F01D86CDBB7E1CD88815BEB4106A558C
```

Very very very interesting.

I summarize, we have a jpg file with text "Pure_Funk", a flag.png file unusable in this state and a file hint.pdf containing an IV AES and text "AngeWouldLoveIt!".

I immediately thought of a conference, "Funky File Formats".
In this conference there was a POC called "Angecryption". This POC showed us that it was possible to obtain a valid file from another valid file by encrypting it or deciphering it with a block cipher and a well chosen IV.
([https://speakerdeck.com/ange/funky-file-formats-31c3](https://speakerdeck.com/ange/funky-file-formats-31c3))

So let's try.

```
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

Arff :(

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/screenshots/whew.png)

whew :)

So, after AES encryption of the flag.png file, I got another png file.

This image is a white square containing transparent holes, I named it mask.png, I merged the two images and I got this:

![](https://github.com/Inshallhack/Write-ups/raw/master/34C3-2017/ecoin/flagged.png)

Yes is the flag :)

So the flag was
```
34c3_F1L3_FORMA7S_AR3_COMMUN17Y_CONNEC7ORS
```

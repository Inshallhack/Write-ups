# Gr8 Pictures 

![gr8](https://jenaye.fr/CTF/TUCTF/Misc/chall.png)

1. the challenge is to find the encrypted data inside a PNG picture

Challenge come with 2 things, a picture containing the flag and its sha1.

you should download picture in some folder. Next, if you send some random string to the NC server, you'll notice it sends back a very large base64 data. This is the same picture as flag.PNG but with your random string encrypted and hidden in it.

let's save the base64 data to a file :

```
touch randomstring.txt
nano randomstring.txt # just add some random string inside the file
nc gr8pics.tuctf.com 4444 < somestring.txt > test.b64 
```

with this command, we save the content of response server to test.b64
Notice : server send base64 format

after that let's decode : 

```
cat test.b64 | base64 --decode > picture.png
```

we need to count all of the difference between the flag.png and picture.png, here its 50 bytes

```
hexdump -C picture.png > picture_hex.txt # this command dump hex to a txt file, then it's easier to compare both using the app meld
```

let's create a file with 50 bytes too, and watch, what happens

![gr8](https://jenaye.fr/CTF/TUCTF/Misc/diff.png)

```
echo "AZERTYUIOPQSDFGHJKLMWXCVBNAZERTYUIOPQSDFGHJKLMWXCV" >> 50bytes.txt
```

lets convert the string to ASCII with online website 

you will have 

```
// 50bytes.txt 
41 5a 45 52 54 59 55 49 4f 50 51 53 44 46 47 48 4a 4b 4c 4d 57 58 43 56 42 4e 41 5a 45 52 54 59 55 49 4f 50 51 53 44 46 47 48 4a 4b 4c 4d 57 58 43 56
```

Reponse of server 
```
08 29 2B 26 0B 21 65 3B 10 23 24 30 2C 19 07 17 29 7B 7C 21 08 3E 36 38 21 3A 28 35 2B 6D 1D 34 0A 3A 3A 33 39 0C 25 19 76 7B 79 7C 13 25 36 20 73 24
```

lets use : http://xor.pw/ end enter the first and second string
XOR : 
```
49736e745f7830725f737563685f405f6330306c5f66756e6374696f6e3f496d5f737563685f615f313333375f6861783072
```

So just we just need to use it as a XOR with the same 50 Bytes from flag.png

```
// Flag 
TUCTF{st3g@e0gr@phy's_so_c00l,No0ne_steals_my_msg}
```

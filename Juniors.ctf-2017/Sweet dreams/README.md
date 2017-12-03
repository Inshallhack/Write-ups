Sweet Dreams
-------

**Category**: La catégorie **Points**: 100:

> Do you also want to see what is below? 


Write up
-------

so we got the _.docx document, let's watch it work binwalk 

```
binwalk _.docx
```

it will output the following content 

![sweet](https://jenaye.fr/CTF/JUNIORCTF/Sweet-Dreams/binwalk.png)

we can watch "Flag.png" let's extract everything 

```
binwalk --dd=".*" _.docx 
```

then we have folder called " __.docx.extracted ", and here we are,  flag.png found just open it
 
![dreams](https://jenaye.fr/CTF/JUNIORCTF/Sweet-Dreams/zip.png)

just open picture now

Flag :

```
DIFFERENT AGE SANDWICH?
```

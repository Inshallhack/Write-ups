# Unusual Traffic

Category : **Stega** Points : **150**  Description : **There is someone sharing the flag on our Xiomara server but we couldn't find the culprit, so help us & we will reward your flag!**


At the start we got Zip file called "Ezio.rar"

when i opened file i found picture

my first reaction was to use binwalk, let's see

```
binwalk --dd=".*" Ezio.bmp 
```

![sweet](https://jenaye.fr/CTF/Xiomara-2018/Unusual-traffic/binwalk.png)

This command gna create  folder with all files extracted, so as we can see, there is an other picture inside the Ezio.bmp


then, i tried to use  https://github.com/Fluffet/stegano-bmp but it didn't work, 

so let's try with Zsteg 

```

./zsteg /home/jenaye/Bureau/_Ezio.bmp.extracted/0 -a > output

```

![sweet](https://jenaye.fr/CTF/Xiomara-2018/Unusual-traffic/flag.png)


And we got it  

" xiomara{stegan0graphy_mAkes_pErfect_Secrecy_:)} "



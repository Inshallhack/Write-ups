# SkeletonKey

- **Category :** misc
- **Points :** 200
- **Description :**
```
Find the flag :)
```

## Writeup

All we have is an apk file, after unpacking it and browsing the files we can see that it is pretty minimal, and the only thing it does is print a skull svg image on the screen.
If we open the assets/logo.svg file, we can see that there are mentions of fonts, character width and so on on a few objects. We can change their color to green for example to be able to recognize them. We can then load the image in an svg editor (here we used https://vectr.com/tmp/c37GXckddN/b1PrML99Ln). We juste have to remove all the unnecessary elements and zoom on the remaining elements). We can then see the flag on the screen : **be278492ae9b998eaebe3ca54c8000de**

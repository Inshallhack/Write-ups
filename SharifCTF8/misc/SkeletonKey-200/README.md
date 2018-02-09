# SkeletonKey

- **Category :** misc
- **Points :** 200
- **Description :**
```
Find the flag :)
```

## Writeup

All we have is an apk file. After unpacking it and browsing the files, we can
see that it is pretty minimal, and that the only thing it does is print a
svg image of a skull on the screen.

If we open the `assets/logo.svg` file, we can see mentions of fonts,
character width and related information on a few objects.

We can change their color to another color (*we used green*) to be able to
spot them. We then load the image in an svg editor (here we used
[vectr.com](https://vectr.com/tmp/c37GXckddN/b1PrML99Ln)).

We remove all the unnecessary elements and zoom in on what remains.
We can then see the flag on the screen: **be278492ae9b998eaebe3ca54c8000de**

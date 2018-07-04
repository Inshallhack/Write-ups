# On a pas les bases

**"On a pas les bases"** was a 50-point Steganography challenge at **Nuit Du Hack 2018**. 

## Challenge description

Because we can't access the platform anymore, this challenge shall remain without description for now.
We are provided with the following picture:

![Oreilles Sales](images/OREILLES_SALES.png)

## Analysis

We start by running `exiftool` on the file:

```bash
~$ exiftool OREILLES_SALES.png 
ExifTool Version Number         : 11.03
File Name                       : OREILLES_SALES.png
Directory                       : .
File Size                       : 396 kB
File Modification Date/Time     : 2018:07:04 15:47:47+02:00
File Access Date/Time           : 2018:07:04 15:48:34+02:00
File Inode Change Date/Time     : 2018:07:04 17:07:41+02:00
File Permissions                : rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 680
Image Height                    : 520
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Exif Byte Order                 : Little-endian (Intel, II)
User Comment                    : aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUXc0dzlXZ1hjUQ==
Thumbnail Offset                : 154
Thumbnail Length                : 5176
Gamma                           : 2.2222
White Point X                   : 0.3127
White Point Y                   : 0.329
Red X                           : 0.64
Red Y                           : 0.33
Green X                         : 0.3
Green Y                         : 0.6
Blue X                          : 0.15
Blue Y                          : 0.06
Background Color                : 255 255 255
Modify Date                     : 2017:09:22 11:41:16
Datecreate                      : 2017-09-22T13:41:16+02:00
Datemodify                      : 2017-09-22T13:41:16+02:00
Signature                       : f0140da3c2e1bf77c4183d771f341d8f3a8e3afc4c7c3b1b65917e8678b16b3e
Software                        : Adobe ImageReady
Warning                         : [minor] Trailer data after PNG IEND chunk
Image Size                      : 680x520
Megapixels                      : 0.354
Thumbnail Image                 : (Binary data 5176 bytes, use -b option to extract)
```

We notice three interesting things in the output:

- there's a **user comment**;
- there's a **thumbnail image**;
- there's a **warning** indicating that there is trailer data after the PNG IEND chunk.

### Checking the user comment

The user comment looks like a **base64-encoded URL** (*I've seen base64-encoded strings starting with "aHR0" often enough to figure this out*). It decodes to the following [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ). Although it's a useful hint, it's not clear enough to us so we discard it for now.

### Extracting the thumbnail

Let's extract the thumbnail then:

```bash
~$ exiftool -b -ThumbnailImage OREILLES_SALES.png > thumbnail.jpg
```

and we get the following image:

![Thumbnail](images/thumbnail.jpg)

I'll pass on the `exiftool` output for this image, which doesn't return anything interesting.
We're left with one last option, which is **to extract possible embedded data in the image that could trigger the warning**.

### Extracting the trailer data

We use `binwalk` to extract the data:

```bash
~$ binwalk --dd=".*" OREILLES_SALES.png -e

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 680 x 520, 8-bit/color RGBA, non-interlaced
64            0x40            Zlib compressed data, best compression
6164          0x1814          Zlib compressed data, best compression
189795        0x2E563         PNG image, 680 x 510, 8-bit/color RGBA, non-interlaced
189859        0x2E5A3         Zlib compressed data, best compression
190382        0x2E7AE         Zlib compressed data, best compression
```

Interesting! We found another **PNG image** embedded within the file. Let's run `exiftool` on this one, then:

```bash
~$ ExifTool Version Number         : 11.03
File Name                       : 2E563
Directory                       : .
File Size                       : 210 kB
File Modification Date/Time     : 2018:07:04 17:54:35+02:00
File Access Date/Time           : 2018:07:04 17:55:33+02:00
File Inode Change Date/Time     : 2018:07:04 17:54:35+02:00
File Permissions                : rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 680
Image Height                    : 510
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Special Instructions            : 4D4A57564533324E4B524E474D5A4A544F5256553436544850424844455354494A555A4653364B5A474A4D5445544B584C453255344D5356474E475855514C5A4A555A4555334B5049524354435753584A4A5755365632474E5247573252544B4A56564655323232495247584F574C4E4A553245325243534E42484732534A524A5A4346534D433249354C47595453454E4D32453656324F4E4A4E4649554C324A564C565336434F4E4A4558515753584B4532553652434B4E564E4549554C594C4A57554B4E434E495241584F54544E4A553245365632534E4A4D5855524A544C4A4B464B36535A4B5249584F5432454C4A554655334B4B4E4A4D564F534C324C455A455532535049354954475454324A555A553256434B4E524846495A5A534A555A54434F493D
Gamma                           : 2.2222
White Point X                   : 0.31269
White Point Y                   : 0.32899
Red X                           : 0.63999
Red Y                           : 0.33001
Green X                         : 0.3
Green Y                         : 0.6
Blue X                          : 0.15
Blue Y                          : 0.05999
Background Color                : 255 255 255
Pixels Per Unit X               : 15748
Pixels Per Unit Y               : 15748
Pixel Units                     : meters
Modify Date                     : 2017:09:22 12:01:42
Datecreate                      : 2017-09-22T14:01:42+02:00
Datemodify                      : 2017-09-22T14:01:42+02:00
Signature                       : 5e6790047fb3e3c8a74d63cdf6e91766d0ba9f513f8d5ea2020e51514bc3ee05
Image Size                      : 680x510
Megapixels                      : 0.347
```

And this time, there's a field of interest as well: **Special Instructions**, which seems to contain a **hex-encoded string**.

Let's find out using python:

```python
>>> encString = "4D4A57564533324E4B524E474D5A4A544F5256553436544850424844455354494A555A4653364B5A474A4D5445544B584C453255344D5356474E475855514C5A4A555A4555334B5049524354435753584A4A5755365632474E5247573252544B4A56564655323232495247584F574C4E4A553245325243534E42484732534A524A5A4346534D433249354C47595453454E4D32453656324F4E4A4E4649554C324A564C565336434F4E4A4558515753584B4532553652434B4E564E4549554C594C4A57554B4E434E495241584F54544E4A553245365632534E4A4D5855524A544C4A4B464B36535A4B5249584F5432454C4A554655334B4B4E4A4D564F534C324C455A455532535049354954475454324A555A553256434B4E524846495A5A534A555A54434F493D"
>>> result = bytes.fromhex(encString)
# Result is: b'MJWVE32NKRNGMZJTORVU46THPBHDESTIJUZFS6KZGJMTETKXLE2U4MSVGNGXUQLZJUZEU3KPIRCTCWSXJJWU6V2GNRGW2RTKJVVFU222IRGXOWLNJU2E2RCSNBHG2SJRJZCFSMC2I5LGYTSENM2E6V2ONJNFIUL2JVLVS6CONJEXQWSXKE2U6RCKNVNEIULYLJWUKNCNIRAXOTTNJU2E6V2SNJMXURJTLJKFK6SZKRIXOT2ELJUFU3KKNJMVOSL2LEZEU2SPI5ITGTT2JUZU2VCKNRHFIZZSJUZTCOI=' 
# The result now looks like a base32-encoded string!
>>> import base64
>>> result = base64.b32decode(result)
# Result is: b'bmRoMTZfe3tkNzgxN2JhM2YyY2Y2MWY5N2U3MzAyM2JmODE1ZWJmOWFlMmFjMjZkZDMwYmM4MDRhNmI1NDY0ZGVlNDk4OWNjZTQzMWYxNjIxZWQ5ODJmZDQxZmE4MDAwNmM4OWRjYzE3ZTUzYTQwODZhZmJjYWIzY2JjOGQ3NzM3MTJlNTg2M319'
# The result now looks like a base64-encoded string!
>>> result = base64.b64decode(result)
# Result is: b'ndh16_{{d7817ba3f2cf61f97e73023bf815ebf9ae2ac26dd30bc804a6b5464dee4989cce431f1621ed982fd41fa80006c89dcc17e53a4086afbcab3cbc8d773712e5863}}'
# And flagged!
```

**Flag: ndh16_{{d7817ba3f2cf61f97e73023bf815ebf9ae2ac26dd30bc804a6b5464dee4989cce431f1621ed982fd41fa80006c89dcc17e53a4086afbcab3cbc8d773712e5863}}**
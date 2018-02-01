Break In CTF 2018: Connecting Will
-------------

**Catégorie**: Misc **Points**: 500 **Description**:

> Will is lost in the Upside-Down and is stuck with the Demogorgon. El is looking for Will, when, she stumbles across a piece of code that Will wrote. The Demogorgon could not decipher the code and hence just left it lying around. El needs your help to find the 2 numbers that can get her the secret key which Will was trying to share. Can you help her?
Link to submit: https://felicity.iiit.ac.in/contest/breakin/findingwill/index.html

**HINT**: 
> It’s a magical world without magical methods


Write up
-------

**Connecting Will** was the second challenge of the CTF (the challenge was
tagged as Misc but should be tagged Web), flagged simultaneously by
**SIben** and **Shrewk**.

<p align="center">
<img src="https://thumbs.gfycat.com/ChillyMadAfricangoldencat-max-1mb.gif">
</p>

## Source code

The provided source code is the following:

```php
<?php
/**
 * Find hashes which match
*/
if (!array_key_exists('val1', $_POST) || !array_key_exists('val2', $_POST)) {
    echo "Please send the inputs correctly\n";
    exit(0);
}

$first = $_POST['val1'];
$second = $_POST['val2'];

if (!(is_numeric($first) || is_numeric($second))) {
    echo "Invalid input\n";
    exit(0);
}

$hash1 = hash('md5', $first, false);
$hash2 = hash('md5', $second, false);

if ($hash1 != $hash2) {
    $hash1 = strtr($hash1, "abcd", "0123");
    $hash2 = strtr($hash2, "abcd", "0123");
    if ($hash1 == $hash2) {
        // Flag will be echoed here.
    } else {
        echo "Hard luck :(\nKeep trying\n";
    }
} else {
    echo "Hard luck :(\nKeep trying\n";
}

?>
```

## Code analysis

The code is fairly straightforward, and its analysis teaches us **lots of
things**:

- two parameters `hash1` and `hash2` passed in our request are used;

```php
    $first = $_POST['val1'];
    $second = $_POST['val2'];
```

- at least one of them has to be a number;

```php
 if (!(is_numeric($first) || is_numeric($second)))
```

- both parameters are hashed using MD5 (coupled with the provided hint, this
clearly hints at [magic hashes](https://www.whitehatsec.com/blog/magic-hashes/));

```php
    $hash1 = hash('md5', $first, false);
    $hash2 = hash('md5', $second, false);
```

- `hash1` has to be different of `hash2`;

```php
if ($hash1 != $hash2) {
```

- characters *a*, *b*, *c* and *d* are respectively transformed into *0*, *1*,
*2* and *3*;

```php
    $hash1 = strtr($hash1, "abcd", "0123");
    $hash2 = strtr($hash2, "abcd", "0123");
```

- after this step and in order to obtain the flag, *hash1* has to evaluate as
equal to *hash2*;

```php
        if ($hash1 == $hash2) {
        // Flag will be echoed here.
        }
```

Sounds easy enough, let's flag this!

## Exploitation

We need to find one or more value(s) whose MD5 hash starts with **ae** and does
not contain any **e** or **f** past the second character. All of these hashes
will evaluate as different during the first comparison, but be transformed
into magic hashes when the conversion between the two checks occurs.

<p align="center">
<img src="https://media.tenor.com/images/84dbf692a249261cf1df2074298e02dc/tenor.gif">
</p>

A quick calculation tells us that this pattern should occur on average every
1/16 × 1/16 × (14/16)^30 = **~14060** hashes. This can easily be bruteforced.

I implemented my bruteforcing algorithm using Powershell, because I'm lazy and
it is very easy to use:

```
$i=0
$count = 0
while($i -lt 1000000000 -and $count -lt 2 )
{
    $md5 = new-object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider
    $utf8 = new-object -TypeName System.Text.UTF8Encoding
    $hash = [System.BitConverter]::ToString($md5.ComputeHash($utf8.GetBytes($i)))
    $hash = $hash.replace("-", "")
    if($hash -like "AE*" -OR $hash -like "0E" -and $hash.substring(2) -notmatch "[EF]" )
    {
        
        write-host -f cyan "Nombre:" $i
        write-host -f Magenta "Hash:" $hash
        write-host "`r`n"
        ++$count
    }
    ++$i
}
```

… Aaaand, I found two results!

<p align="center">
<img src="https://raw.githubusercontent.com/Inshallhack/Write-ups/master/Break%20In%20CTF%202018/Connecting%20Will/resultat.PNG">
</p>

Let's try them…

**FLAGGED !!!**

<p align="center">
<img src="https://media.giphy.com/media/4AZ7jvyD54AFO/giphy.gif">
</p>

```
Success. The flag is BREAKIN{I_Will_Connect}
```

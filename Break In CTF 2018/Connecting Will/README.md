Break In CTF 2018: Connecting Will
-------------

**Catégorie**: Misc **Points**: 500 **Description**:

> Will is lost in the Upside-Down and is stuck with the Demogorgon. El is looking for Will, when, she stumbles across a piece of code that Will wrote. The Demogorgon could not decipher the code and hence just left it lying around. El needs your help to find the 2 numbers that can get her the secret key which Will was trying to share. Can you help her?
Link to submit: https://felicity.iiit.ac.in/contest/breakin/findingwill/index.html

**HINT**: 
> It’s a magical world without magical methods


Write up
-------

This challenge was the second of the CTF, flagged at the same time by SIben and Shrewk.

Before the begin of this chall we can read the source code and hint.

Now we know a lot of things:

 - We need to use 2 parameters

 ```
    $first = $_POST['val1'];
    $second = $_POST['val2'];
 ```

 - One param need to be numeric

 ```
 if (!(is_numeric($first) || is_numeric($second)))
 ```

 - Vars are hashed in md5 (So with hint we know "Magic Hashes" is the solve)

 ```
    $hash1 = hash('md5', $first, false);
    $hash2 = hash('md5', $second, false);
```

- First hash1 can't be equal to hash2 (We can't use magic hash for moment)

```
if ($hash1 != $hash2) {
```

- chars abcd are converted into 0123

```
    $hash1 = strtr($hash1, "abcd", "0123");
    $hash2 = strtr($hash2, "abcd", "0123");
```

- Finally to flag hash1 need to be equal to hash2 -_-

```
        if ($hash1 == $hash2) {
        // Flag will be echoed here.
        }
```

Let's go to flag this shit !

It's easy we need to find one value (or more) with md5 hash which begin with AE and not contain E and F.

To make easy script i used Powershell:

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

I've found two result:

<p align="center">
<img src="https://raw.githubusercontent.com/Inshallhack/Write-ups/master/Break%20In%20CTF%202018/Connecting%20Will/resultat.PNG">
</p>

Try results and FLAGGED !!!

```
Success. The flag is BREAKIN{I_Will_Connect}
```



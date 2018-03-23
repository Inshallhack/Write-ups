# gmx

**gmx** was a 160 point cryptography challenge in **Ångstrom CTF 2018**. I thought it was very interesting, especially because it used an actual cryptosystem I had no knowledge of, and surprisingly validated by less than 30 teams among the almost 2000 that were participating.

## Challenge description

defund created a nonconformist hybrid cryptosystem. He even made a service running at `web.angstromctf.com:3000`; here's the [public key](https://angstromctf.com/static/crypto/gmx/pk). All you have to do is decrypt this [flag](https://angstromctf.com/static/crypto/gmx/flag.enc), which was encrypted with this [key](https://angstromctf.com/static/crypto/gmx/key.enc). We've also provided the relevant [source code](/static/crypto/gmx/gmx.zip). Note: connect with netcat or an equivalent tool.

## Analyzing the source code

The source is composed of **4 files**: **aes.py**, **gen.py**, **gm.py**, and **server.py**. Let's start with **aes.py**:

### aes.py

```python
from Crypto import Random
from Crypto.Cipher import AES

def encrypt(k, m):
        iv = Random.new().read(16)
        cipher = AES.new(k, AES.MODE_CFB, iv)
        return iv + cipher.encrypt(m)

def decrypt(k, c):
        cipher = AES.new(k, AES.MODE_CFB, c[:16])
        return cipher.decrypt(c[16:])
```

Nothing special happening here, these functions are pretty much wrappers to **encrypt** and **decrypt** with **AES in CFB mode** with a **random IV that is prepended to the ciphertext during encryption**.

### gen.py

```python
from Crypto import Random

import aes
import gm

flag = open('flag').read()

key = Random.new().read(16)
pk, sk = gm.generate()

encflag = aes.encrypt(key, flag)
enckey = gm.encrypt(key, pk)

with open('pk', 'w') as f:
        f.write('\n'.join([str(x) for x in pk]))

with open('sk', 'w') as f:
        f.write('\n'.join([str(x) for x in sk]))

with open('key.enc', 'w') as f:
        f.write('\n'.join([str(x) for x in enckey]))

with open('flag.enc', 'w') as f:
        f.write(encflag)
```

In **gen.py**, we can basically see how the files we were provided were generated; the flag is encrypted using the `encrypt` function from **aes.py**, and then written to a file. The key is then encrypted with an `encrypt` function presumably defined in **gm.py**, using the **public key** we have been provided, and then written to a file. Each of the keys in the generated keypair (*pk and sk*) is then also written to a file.

Because the crux of the problem will most likely lie in **gm.py** (*that's my experience speaking*), let's continue with **server.py** so as to not get too deep in unnecessary considerations.

### server.py

```python
import base64
import signal
import SocketServer

import aes
import gm

PORT = 3000

message = open('message').read()

with open('sk') as f:
        p = int(f.readline())
        q = int(f.readline())
        sk = (p, q)

class incoming(SocketServer.BaseRequestHandler):
        def handle(self):
                req = self.request

                def receive():
                        buf = ''
                        while not buf.endswith('\n'):
                                buf += req.recv(1)
                        return buf[:-1]

                signal.alarm(60)

                req.sendall('Welcome to the Goldwasser-Micali key exchange!\n')
                req.sendall('Please send us an encrypted 128 bit key for us to use.\n')
                req.sendall('Each encrypted bit should be sent line by line in integer format.\n')

                enckey = []
                for i in range(128):
                        enckey.append(int(receive()))
                key = gm.decrypt(enckey, sk)
                encmessage = aes.encrypt(key, message)

                req.sendall(base64.b64encode(encmessage)+'\n')
                req.close()

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
        pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(('0.0.0.0', PORT), incoming)

print 'Server listening on port %d' % PORT
server.serve_forever(
```

So basically, the code here waits for us to send an **AES key encrypted with gm** (*which we can now deduce means "Goldwasser-Micali"*), then it **decrypts it using the secret key** generated in **gen.py**. Then, a **certain message** is **encrypted using the decrypted AES key**. It is then **base64-encoded** and sent back to us. Since `message` is also read from a file, it is safe to assume that it doesn't change between each connection to the service. An obvious deduction is that the **service will serve as some kind of oracle**.

### gm.py

```python
from Crypto.Util.number import *
from gmpy import legendre

def generate():
        p = getStrongPrime(1024)
        q = getStrongPrime(1024)
        n = p*q
        x = getRandomRange(0, n)
        while legendre(x, p) != -1 or legendre(x, q) != -1:
                x = getRandomRange(0, n)
        return (n, x), (p, q)

def encrypt(m, pk):
        n, x = pk
        for b in format(int(m.encode('hex'), 16), 'b').zfill(len(m) * 8):
                y = getRandomRange(0, n)
                yield pow(y, 2) * pow(x, int(b)) % n

def decrypt(c, sk):
        p, q = sk
        m = 0
        for z in c:
                m <<= 1
                if legendre(z % p, p) != 1 or legendre(z % q, q) != 1:
                        m += 1
        h = '%x' % m
        l = len(h)
        return h.zfill(l + l % 2).decode('hex')
```

Here comes the non-straightforward part… Because only `gm.decrypt` is used in **server.py** (*and not `gm.encrypt`*), we can assume that it is the function of interest in this challenge. Let's break it down:

```python
p, q = sk
```

First it splits `sk` in two components. A quick look at the `generate` function confirms that `sk` is a tuple.

```python
m = 0
for z in c:
	m <<= 1
  		if legendre(z % p, p) != 1 or legendre(z % q, q) != 1:
  			m += 1 
```

Seeing `m = 0`, `m <<= 1` and `m += 1`, we understand that the rightmost bit of `m` is set at each iteration. If `legendre(z % p, p) != 1` or if `legendre(z % q, q) != 1`, it is set to **1**; otherwise, it is set to **0**. It is not clear what `legendre` is supposed to do; let's have a look at Wikipedia:

**&lt;Wikipedia&gt;**

In number theory, the **Legendre symbol** is a multiplicative function with values 1, −1, 0 that is a quadratic character modulo an odd prime number p: its value on a (nonzero) quadratic residue mod p is 1 and on a non-quadratic residue (non-residue) is −1. Its value on zero is 0.

**&lt;/Wikipedia&gt;**

Now, just for the sake of being clear, let's check what a **quadratic residue** is:

**&lt;Wikipedia&gt;**

In number theory, an integer q is called a **quadratic residue** modulo n if it is congruent to a perfect square modulo n.

**&lt;/Wikipedia&gt;**

Phew, that is clearer!

Let's note that when this function is called from **server.py**, since **128 lines are parsed by the service, 128 iterations of the loop occur**. This means that **128 bits are set**, which corresponds exactly to the length of an **AES-128 key**.

```python
h = '%x' % m
l = len(h)
return h.zfill(l + l % 2).decode('hex')
```

Then, `m` is formatted in **hex**, properly padded, decoded and returned.
From this analysis follows the fact that `m` is at most `len(c)` bits long, and most likely close to that.

## Exploitation

Our goal is obviously to retrieve the **AES key** in **key.enc**, so that we can use it to decrypt **flag.enc**.

First, we know that `legendre(a, p)` returns **0** if **a % p = 0**. Since we have the following line:

```python
if legendre(z % p, p) != 1 or legendre(z % q, q) != 1:
	m += 1
```

we can deduce that sending 128 lines equal to **"0"** to the service will result in the generation of a key `key = "\xff" * 16`.

Using this property, we retrieve the value of `message` (*defined in **server.py***) using the following script:

```python
import aes
import base64
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('web.angstromctf.com', 3000))

print '[+] Connected'

print sock.recv(1024)

for i in range(128):
    sock.send('0\n')

print sock.recv(1024)
key = '\xff' * 16
print aes.decrypt(key, base64.b64decode(sock.recv(1024)))

sock.close()
```

and we get the following message:

```
Hi, this is defund and you're reading my super secret message! Unfortunately, getting this message is not the challenge whatsoever. I don't have much else to talk about, so I guess follow me at github.com/defund, twitter.com/defunded, and keybase.io/defund.

Also, here's a fake flag that you're going to submit anyways:
actf{this_is_a_fake_flag}

Good luck with the challenge! ;)
```

Obviously, we try to validate using the fake flag… But it doesn't work, surprisingly.

We figured that we're somehow able to control the return value of `legendre` so that it returns 0 **regardless of what the secret GM key actually is**.

If we were to replace the first line in our all "0" encrypted key with the first line of **key.enc**, we would be able to receive a ciphertext encrypted with a key whose first bit corresponds to the first line of **key.enc**. Then, **it is just a matter of testing whether the bit should be a 1 or a 0**; this is **easily doable by checking which of the two possible keys decrypts the ciphertext to the expected plaintext**!

Because we're pretty lazy (*at least I am*), we want to reuse the `gm.decrypt` function to generate our key. It is therefore useful to know that, in the same way `legendre(a, p)` returns **0** for any value of `p` provided that `a = 0`, `legendre(a, p)` returns **1** for any value of `p` provided that `a = 1`. The reason is obvious: **1 is a perfect square**, and since **it is not a prime**, it is not an adequate value for `p`. Note that **4** would also be an acceptable value, as **2 is not an odd prime**.

With this idea, we create the following (*dirty*) script:

```python
import aes
import base64
import gm
import socket

# Connecting to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('web.angstromctf.com', 3000))

# Yay!
print '[+] Connected'

# Reading the encrypted key
with open('key.enc') as f:
    enc_key = f.read().split('\n')

# Initializing the key for our method
base_key = [0] * 128

# recv useless garbage
print sock.recv(1024)

# Send the key, which is basically all 0s at this point
for i in range(len(base_key)):
    sock.send(str(base_key[i]) + '\n')

# recv useless garbage again
print sock.recv(1024)

# Setting the decryption key to its initial value
dec_key = '\xff' * 16

# Retrieving the "witness" base64 encrypted string
b64witness = sock.recv(1024)

# Decrypting the witness and storing it so as to compare all the subsequent
# results with it.
witness = aes.decrypt(dec_key, base64.b64decode(b64witness))

print 'Witness is: ' + witness

# :'( gotta open again
sock.close()

for i in range(128):
    # Open, open, open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('web.angstromctf.com', 3000))
    print '[+] Connected (' + str(i + 1) + ')'

    # Getting useless garbage
    sock.recv(1024)

    # Setting the current encrypted bit to the one in the encrypted key
    base_key[i] = int(enc_key[i])

    # Send the key
    for j in range(len(base_key)):
        sock.send(str(base_key[j]) + '\n')
     
    res = ''

    # Fetching the result, with super dirty error correction, idc
    while len(res) < 10 or 'Please send' in res:
        res = sock.recv(1024)
    
    # Checking whether the decryption works properly with the key we have
    if aes.decrypt(dec_key, base64.b64decode(res)) == witness:
        base_key[i] = 0
    # Otherwise, we need to change the key
    else:
        # Cause I'm lazy
        base_key[i] = 1
        # Modifying the key as it should be
        dec_key = gm.decrypt(base_key, (17, 19))

    sock.close()

# Got the key :-)
print '[+] Key is: ' + ' '.join([str(ord(c)) for c in dec_key])

# Writing to file
print '[+] Writing to \'result\'...'
with open('result', 'w') as fres:
    with open('flag.enc') as flag:
        fres.write(aes.decrypt(dec_key, flag.read()))
```

Aaand, we get a jpg file, which contains… **the flag**!

![Flag](./images/angstrom_gmx_flag.jpg)

**Flag: actf{a_bit_of_homomorphism}**

## Conclusion

This CTF was really quite interesting. I especially enjoyed this challenge; quit making **RSA challenges** people, we need more of these!

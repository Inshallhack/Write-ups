# ndash

ndash was a 250-point Crypto challenge at **Nuit Du Hack 2018**. I was very surprised to see it has only been solved 8 times, since it was probably the easiest challenge I encountered (*disregarding icmp*). I believe we missed getting first blood by not opening the challenge quickly enough :). From what I gathered though, the solution presented here was **not intended**.

## Challenge description

Because we can't access the platform anymore, this challenge shall remain without description for now.
We know that we are supposed to read the **flag.txt** file in the folder where this script runs, and we are provided with a link to the following source:

```python
#!/usr/bin/env python3.6
"""

#####################################
###### Module Documentation #########
#####################################

This module is the main loop of the application,
it is used to interact with the user and to validate that
they have access to the resources they are asking for.

#####################################
###### General Documentation ########
#####################################

File read wrapper.
This program is used to expose some safe files to the internet.

Contributions are welcome.

# Dev instructions

You'll need:
    - Python3.6.5
    - docker
    - a brain

* Login:
    $ export DOCKER_ID_USER="ndhovh2018"
    $ docker login

* Build:
    $ docker build -t ndh-reader-wrapper .
    $ docker tag ndh-reader-wrapper $DOCKER_ID_USER/ndh-reader-wrapper
    $ docker push $DOCKER_ID_USER/ndh-reader-wrapper

* Run:
    $ docker run -d --restart unless-stopped -p 5000:5000 $DOCKER_ID_USER/ndh-reader-wrapper

#####################################
############# License ###############
#####################################

Copyleft

"""
import os
import pathlib
import myhash
import signal
import sys

signal.alarm(20)


def sanitize(path: str) -> str:
    path = path[:os.statvfs(".").f_namemax]
    print(path)
    assert os.path.isfile(path)
    return path


def check_is_safe(user_path: str):
    path = sanitize(user_path)
    assert pathlib.PurePath(path) == pathlib.PurePath("./hello_world.txt")


def main():
    safe_path_user = input("Enter the only safe file there is: ")
    file_to_read = input("Enter the file you want to read: ")
    check_is_safe(safe_path_user)

    print(f"Trying safe_path_user={safe_path_user} and file_to_read={file_to_read}", file=sys.stderr)

    # Compute the hash of the file names
    safe_path_hash = myhash.NDHash(safe_path_user)
    file_to_read_hash = myhash.NDHash(file_to_read)

    if safe_path_hash != file_to_read_hash:
        print("Sorry, you are not allowed to read this file", flush=True)
        exit(0)

    with open(os.path.normpath(file_to_read)) as f:
        print("File content is:", flush=True)
        print("#"*40, flush=True)
        print(f.read(), flush=True)
        print("#"*40, flush=True)


if __name__ == "__main__":
    main()
```

## Analyzing the source code

Our aim is obviously to reach the following part of code:

```python
with open(os.path.normpath(file_to_read)) as f:
	print("File content is:", flush=True)
	print("#"*40, flush=True)
	print(f.read(), flush=True)
	print("#"*40, flush=True)
```

with `os.path.normpath(file_to_read)` somehow being equivalent to `./flag.txt`.
 
This essentially means that we have to avoid this block of code:

```python
if safe_path_hash != file_to_read_hash:
	print("Sorry, you are not allowed to read this file", flush=True)
	exit(0)
```

This means that `safe_path_hash` and `file_to_read_hash` must be equal.

```python
# Compute the hash of the file names
safe_path_hash = myhash.NDHash(safe_path_user)
file_to_read_hash = myhash.NDHash(file_to_read)
```

Both hashes are computed using a custom hash function which we don't seem to have the code for (*spoiler: we can actually get the code, but we did not even try*).

`safe_path_user` and `file_to_read` are two strings that we can control, one of which (*safe_path_user*) is passed through a sanitizing function as seen below:

```python
safe_path_user = input("Enter the only safe file there is: ")
file_to_read = input("Enter the file you want to read: ")
check_is_safe(safe_path_user)

print(f"Trying safe_path_user={safe_path_user} and file_to_read={file_to_read}", file=sys.stderr)

# Compute the hash of the file names
safe_path_hash = myhash.NDHash(safe_path_user)
file_to_read_hash = myhash.NDHash(file_to_read)
```

Let's add comments to the sanitizing code:

```python
# Basically truncates a string to its first f_namemax characters, and checks that the resulting file exists
def sanitize(path: str) -> str:
    path = path[:os.statvfs(".").f_namemax] # truncating to f_namemax characters
    print(path)
    assert os.path.isfile(path) # Checking that path still points to a valid file
    return path

# Sanitizes the path using the above function and then checks that the resulting path points to './hello_world.txt'
def check_is_safe(user_path: str):
    path = sanitize(user_path) # Sanitizes the path
    assert pathlib.PurePath(path) == pathlib.PurePath("./hello_world.txt") # Checks that it points to './hello_world.txt'
```

So, it seems we're left with two options to get the flag:

1. find the hashing function source and **create a hash collision between the file we want to request and the sanitized path**;
2. work from what we have and **exploit the sanitizing function**.

We decided to go with **2**, because `check_is_safe` is doing something very wrong: it does not return the sanitized path after checking it. This means that as long as we're able to modify our path in a meaningful way after the first `f_namemax` characters and to pad it correctly so that the first `f_namemax` characters correspond to a path semantically equal to `./hello_world.txt`, we can pretty much pass any path we want. **Path truncation + directory traversal**, it is!

If we set both variables to this path, we'll be able to **pass the sanitizing function** as well as the subsequent condition, as we'll be **comparing the hash of a string with itself**.

On my Debian system, `os.statvfs(".").f_namemax` is a constant equal to **255**. We can assume it is probably the same on the remote server. Therefore, a valid payload would be:

```python
payload = "././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././hello_world.txt/../flag.txt"
```

We connect to the service, send this twice and… **Flagged!**

**Flag: ndh16_793a07af2612eb79254e2f22ce25ccac8d3698cac05ea25ec6f6a2c66eca8802959ab77e2a29c177437ab8ebd0a681834429197b6a5acf654d0a1de83b6dae65**

## Wrapping up

This challenge was easy, but amusing. I think that the "correct" solution actually involves a hash collision. Nevertheless, I am quite disappointed that this was the **only challenge tagged as "cryptography"** and that it **didn't actually require any of that**.

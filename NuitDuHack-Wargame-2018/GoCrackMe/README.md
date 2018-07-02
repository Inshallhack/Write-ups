# GoCrackMe

- **Category:** crackme
- **Points:** 400

# Writeup
As the name of the challenge implies, this binary is a Go executable. After a quick static analysis we saw that the whole binary was stripped which made static analysis pretty difficult (we also had to consider all indirections used by the language itself).
Using strace we can quickly guess how the binary works.

```
(print message) -> (read user input) -> (check input) -> (print fail/win)
```

[Screenshot strace](img/strace.jpg)

Since the code base is huge (thanks Go) we needed a way to pinpoint the exact functions processing our input. We first tried to breakpoint at the read syscall loading our flag in memory and then checking were this would take us. Unfortunately the abstraction of Go prevented us from discovering anything interesting as we quickly got lost in the numerous calls to other functions.
Our second idea was to breakpoint at the second write syscall (result message) and go up the call stack until the flag verification function. This turned out to be the right idea but not in the way we expected. 

When looking at the parameters in gdb we saw that rsi (buffer address) after the syscall was pointing at the fail string, but this one was not null terminated and there was a weird ascii string afterwards that we couldn't find in the executable itself.
[Screenshot weirdstring](img/weirdstring.jpg)

To gather information we looked up the section containing the string and we dumped it. We ran strings on it and so a lot of ascii strings including fake flags. 
[Screenshot strings](img/strings.jpg)

After trying a few of them we were surprised to discover that our dump actually contained the flag.
[Screenshot flagged](img/flag.jpg)

challenge password : This1sATotalLyDumbPa5$wordBut1tW0rkN3h
challenge flag : ndh16\_2c51459d50d04a8705493d2ab9696e21f17ddd62ebbe106dbbca8a18a867c82f9ea1c84319035b95cbc64303dbf26172c67adac64a45f48854c272cbc2608957

# Note
Sometimes running **strings** on random binary blob seem to yield surprinsing results.

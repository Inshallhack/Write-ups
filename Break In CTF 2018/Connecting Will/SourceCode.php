<?php
/** 
 * Find hashes which match 
*/
if (!array_key_exists('val1', $_POST) || !array_key_exists('val2', $_POST)) {
    echo "Please send the inputs correctly\n";
    exit(0);
}

$first = $_POST['val1'];
$second = $_POST['val2'];

if (!(is_numeric($first) || is_numeric($second))) {
    echo "Invalid input\n";
    exit(0);
}

$hash1 = hash('md5', $first, false);
$hash2 = hash('md5', $second, false);

if ($hash1 != $hash2) {
    $hash1 = strtr($hash1, "abcd", "0123");
    $hash2 = strtr($hash2, "abcd", "0123");
    if ($hash1 == $hash2) {
        // Flag will be echoed here.
    } else {
        echo "Hard luck :(\nKeep trying\n";
    }
} else {
    echo "Hard luck :(\nKeep trying\n";
}

?>
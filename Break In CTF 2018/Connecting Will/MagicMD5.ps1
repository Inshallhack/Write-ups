
$i=0
$count = 0
while($i -lt 1000000000 -and $count -lt 2 )
{
    $md5 = new-object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider
    $utf8 = new-object -TypeName System.Text.UTF8Encoding
    $hash = [System.BitConverter]::ToString($md5.ComputeHash($utf8.GetBytes($i)))
    $hash = $hash.replace("-", "")
    if($hash -notmatch "F" -and $hash -like "AE*" -OR $hash -like "0E" -and $hash.substring(2) -notmatch "E" )
    {
        
        write-host -f cyan "Nombre:" $i
        write-host -f Magenta "Hash:" $hash
        write-host "`r`n"
        ++$count
    }
    ++$i
}
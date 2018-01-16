
TPCTF 2017: That's not latin...
-------

**Catégorie**: Misc **Points**: 10 **Description**:

> Free 10 points...right? Here's the flag, I hope: 
tpctf{nеv3r_7h15_3z}


Write up
-------

In the description we have tpctf{nеv3r_7h15_3z}.

Try it as a flag, but don't work. :(

<p align="center">
<img src="https://i.skyrock.net/8962/46148962/pics/1867901609_1.jpg">
</p>

In the title we have one clue "latin".

Now i try to see what is the char not in UTF8 encode:

> <?php
echo utf8_decode("nеv3r_7h15_3z");


The result was:

> n?v3r_7h15_3z


Replace ? with e and flag.

> tpctf{nev3r_7h15_3z}


<p align="center">
<img src="http://mfs0.bp.cdnsw.com/fs/Root/normal/fsqc-Bob_l_eponge_heureux.jpg">
</p>




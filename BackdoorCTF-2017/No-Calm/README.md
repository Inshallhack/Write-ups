Backdoor CTF 2017: No-Calm
-------

**Catégorie**: Reverse **Points**: 350

Write up
-------

Code source en python:

```python 
  import angr
import claripy

"""
Lorsqu'on lance le programme  on a :
"Usage ./challenge <each byte of flag seperated by spaces>"

=> il va falloir faire quelque chose du genre ./challenge f l a g

Au début du programme on trouve un

cmp dword [local_44h], 0x1f

Le programme prends donc 30 paramètres (le 1er étant le nom du programme)

On en déduis que le flag fait 30 chars, il reste plus qu'a scripter le tout avec angr
On peut surement faire plus propre avec des boucles mais bon x)
"""

p = angr.Project('challenge', load_options={"auto_load_libs": False})

arg1 = claripy.BVS('arg1', 2*8)
arg2 = claripy.BVS('arg2', 2*8)
arg3 = claripy.BVS('arg3', 2*8)
arg4 = claripy.BVS('arg4', 2*8)
arg5 = claripy.BVS('arg5', 2*8)
arg6 = claripy.BVS('arg6', 2*8)
arg7 = claripy.BVS('arg7', 2*8)
arg8 = claripy.BVS('arg8', 2*8)
arg9 = claripy.BVS('arg9', 2*8)
arg10 = claripy.BVS('arg10', 2*8)
arg11 = claripy.BVS('arg11', 2*8)
arg12 = claripy.BVS('arg12', 2*8)
arg13 = claripy.BVS('arg13', 2*8)
arg14 = claripy.BVS('arg14', 2*8)
arg15 = claripy.BVS('arg15', 2*8)
arg16 = claripy.BVS('arg16', 2*8)
arg17 = claripy.BVS('arg17', 2*8)
arg18 = claripy.BVS('arg18', 2*8)
arg19 = claripy.BVS('arg19', 2*8)
arg20 = claripy.BVS('arg20', 2*8)
arg21 = claripy.BVS('arg21', 2*8)
arg22 = claripy.BVS('arg22', 2*8)
arg23 = claripy.BVS('arg23', 2*8)
arg24 = claripy.BVS('arg24', 2*8)
arg25 = claripy.BVS('arg25', 2*8)
arg26 = claripy.BVS('arg26', 2*8)
arg27 = claripy.BVS('arg27', 2*8)
arg28 = claripy.BVS('arg28', 2*8)
arg29 = claripy.BVS('arg29', 2*8)
arg30 = claripy.BVS('arg30', 2*8)


initial_state = p.factory.entry_state(args=['./ch24.bin',arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12,arg13,arg14,arg15,arg16,arg17,arg18,arg19,arg20,arg21,arg22,arg23,arg24,arg25,arg26,arg27,arg28,arg29,arg30], add_options={angr.options.LAZY_SOLVES})
pg = p.factory.simgr(initial_state)

pg.explore(find=0x4007b6,avoid=0x4007cc)

found = pg.found[0]
flag = ""
flag += found.se.any_str(arg1)
flag += found.se.any_str(arg2)
flag += found.se.any_str(arg3)
flag += found.se.any_str(arg4)
flag += found.se.any_str(arg5)
flag += found.se.any_str(arg6)
flag += found.se.any_str(arg7)
flag += found.se.any_str(arg8)
flag += found.se.any_str(arg9)
flag += found.se.any_str(arg10)
flag += found.se.any_str(arg11)
flag += found.se.any_str(arg12)
flag += found.se.any_str(arg13)
flag += found.se.any_str(arg14)
flag += found.se.any_str(arg15)
flag += found.se.any_str(arg16)
flag += found.se.any_str(arg17)
flag += found.se.any_str(arg18)
flag += found.se.any_str(arg19)
flag += found.se.any_str(arg20)
flag += found.se.any_str(arg21)
flag += found.se.any_str(arg22)
flag += found.se.any_str(arg23)
flag += found.se.any_str(arg24)
flag += found.se.any_str(arg25)
flag += found.se.any_str(arg26)
flag += found.se.any_str(arg27)
flag += found.se.any_str(arg28)
flag += found.se.any_str(arg29)
flag += found.se.any_str(arg30)

print "FLAG : {}".format(flag)
```

[Script](https://github.com/Inshallhack/Write-ups/blob/master/BackdoorCTF-2017/No-Calm/solve.py)



## System call vs Shell command 
A system call is a low level api provided by OS kernel , compiled binaries or it is used via code, runs in kernel model 

A shell command is standalone executable program , runs in user mode

think of the operating system like a restaurant: The kernel is the kitchen, a system call is the window where orders are passed to the chefs, and a shell command is the waiter you actually talk to.




## Globbing and basic patterns

vasanthansr@Vasanthan-SR ~
❯ touch img_{001..098}                                                                                      ✔  16:55:03
vasanthansr@Vasanthan-SR ~
❯ ls                                                                                                        ✔  16:55:32
app.js       img_007  img_016  img_025  img_034  img_043  img_052  img_061  img_070  img_079  img_088  img_097
dead.letter  img_008  img_017  img_026  img_035  img_044  img_053  img_062  img_071  img_080  img_089  img_098
glob-lab     img_009  img_018  img_027  img_036  img_045  img_054  img_063  img_072  img_081  img_090  test-py
img_001      img_010  img_019  img_028  img_037  img_046  img_055  img_064  img_073  img_082  img_091  test-vim
img_002      img_011  img_020  img_029  img_038  img_047  img_056  img_065  img_074  img_083  img_092
img_003      img_012  img_021  img_030  img_039  img_048  img_057  img_066  img_075  img_084  img_093
img_004      img_013  img_022  img_031  img_040  img_049  img_058  img_067  img_076  img_085  img_094
img_005      img_014  img_023  img_032  img_041  img_050  img_059  img_068  img_077  img_086  img_095
img_006      img_015  img_024  img_033  img_042  img_051  img_060  img_069  img_078  img_087  img_096
vasanthansr@Vasanthan-SR ~
❯                                                                                                           ✔


{001..009} is brace expansion.
[0-9] is a glob set.


* and ?

```bash
vasanthansr@Vasanthan-SR ~
❯ echo simpl*.txt                                                                                           ✔  12:26:41
simpl.txt simple.txt
vasanthansr@Vasanthan-SR ~
❯ echo simpl?.txt                                                                                           ✔  12:26:48
simple.txt
vasanthansr@Vasanthan-SR ~
❯               
```

[] : one character from a set

```bash
❯ echo img_00[123]                                                                                          ✔  12:26:57
img_001 img_002 img_003
vasanthansr@Vasanthan-SR ~
❯ echo img_01[2468]                                                                                         ✔  12:29:20
img_012 img_014 img_016 img_018
```

{} : generate a list of strings
- Braces are completely different. They don’t look at files at all. They write out text for you.
- Quotes turn off brace expansion



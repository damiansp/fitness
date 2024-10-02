# kickboxing

A simple boxing/kickboxing/circuit training workout generator.

Usage:
```
./main [-c CATEGORY] [-t TIME] [-w WORK] [-r REST]                           
```

Where                                                                        
- `CATEGORY` in [ `b` | `kb` | `bc` | `kbc` ] (b: boxing, kb: kickboxing, c: circuit). Default: `kbc`
- `TIME`: total time (min). Default: 30
- `WORK`: exercise time per round (min). Default: 3
- `REST`: rest time per round (min). Default: 1

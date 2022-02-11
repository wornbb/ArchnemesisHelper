# ArchnemesisHelper
Help you to loot and make archnemesis mods

## Installation
Simply clone it.
This is a command line `python` program so you have to launch it from the command line and make sure you have python installed. It does not use any other dependencies.

## Usage
First, you have to modify the `chase_recipe` to fit your need. The provided defualt `chase_recipe` should be good for most cases. `chase_recipe` your ultimate juicing plan, and you can have as many as you want.

This program support 4 commands. Namely `loot`, `plan`, `use` and `check`. Usage is command + mod name. For example, `loot gargantuan`. Partial mod name is also support so input `loot garg` will do the same thing. Note, some mods share identical parts such as `soul eater` and `soul conduit`. In this case, both matches will be shown.

1. `loot mod` command tells you how many of this mod you should loot from the ground to full fill all your `chase_recipe`.
2. `plan mod` and `use mod` are very similar. It tells you what is the next mod you should make from this mod, and how many should you make. The difference of the 2 are the output format. `plan` is more verbose for it tells you the whole recipe chain.
3. `check mod` tells you how to make this mod.

## Examples
```
How can I help you? (one mod at a time)
loot soul
mod                  count used for
soul conduit         2     ['mirror image', 'soul eater']
mod                  count used for
soul eater           1     ['shakari-touched']
How can I help you? (one mod at a time)
check soul
soul eater :  {'necromancer', 'gargantuan', 'soul conduit'}

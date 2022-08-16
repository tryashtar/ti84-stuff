My failed attempt to create cross-calculator multiplayer rock-paper-scissors.

The only way to communicate between connected calculators is the `GetCalc` command, which is very slow, and simply overwrites the value of a local variable with the value of that same variable on the connected calculator. Assuming both calculators are running the same program, it seems nearly impossible to coordinate them.

First, you need to establish a shared identity. My first thought was to generate a random number on each calculator and choose the calculator with the higher number to be the "authority." But how can you even compare numbers?

```
rand→A
A→B
GetCalc(A
Disp B>A
```

The first problem with this is that if the partner calculator hasn't started the program yet, it won't even have a random value for `A`, invalidating the state. The next problem is that whichever calculator runs `GetCalc` second will just be receiving the very value for `A` it just sent over, not the first calculator's `A`, so it will always think it's second, even if the first calculator's number was lower.

Now that I'm thinking about it, perhaps you could just generate a random number, then try to get the other calculator's number. If you see the numbers are different, you are the authority calculator, and if they're the same, you ran second. Oh well, I don't have any calculators anymore to experiment.

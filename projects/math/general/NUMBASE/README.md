Converts a number in an arbitrary base to another arbitrary base. Digits greater than 9 are represented using letters A-Z. The magic of this conversion takes place in two highly esoteric lines that I'm rather proud of:

```
sum(L₁seq(B^I,I,dim(L₁)-1,0,⁻1
int(CfPart(Ans/seq(C^I,I,iPart(1+log(Ans)/log(C)),1,⁻1→L₁
```

The inputs are:
* `L₁`: List of digits
* `B`: Starting base
* `C`: Desired base

The `seq` function is like an inline loop: it creates a list by evaluating an expression on a variable multiple times. `B^I` is the expression here, and we iterate using `I` from `dim(L₁)-1` to `0`, counting by `⁻1`. This results in a list as long as our input digits, where each item is equal to the value of that place in that base.

`L₁` contains the digits associated with those places, so we multiply the lists together element-wise, then take the sum. This gives us the value of the input number in `Ans`.

The number of digits required to write a number in a base is the log of the number in that base, plus one. There is a `logBASE` function, but TI-83s don't support it, so the change-of-base formula `log(Ans)/log(C)` works just as well. Round down and add one.

Another `seq` function creates a list of that length, populating it with `C^I`, counting down. Like before, this list represents the place values of the destination base, but the iteration is one value higher this time, multiplying all values by `C`.

Next we element-wise divide `Ans` over the list, taking the remainder instead of the quotient. Again, there is a `remainder` function, but `CfPart(Ans)` works on older calculators. This leaves us with every digit properly fitting into the range for that place.

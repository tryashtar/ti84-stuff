A collection of some of the TI-Basic programs I wrote on my TI-84 mostly between 2014 and 2017.

The compiled tokenized `.8xp` files are provided as well as the source code in text form.

In order to build the `.8xp` file from the source code, I have created a very simple compiler that can be found in [`compiler.py`](compiler/compiler.py). I created it after running into a minor issue with [Cemetech's SourceCoder 3](https://www.cemetech.net/sc/). Basically, when loading a program that contained text like `pin`, it loaded fine, but it would export that as `πn`, essentially breaking round-trip interop. My compiler detects ambiguous symbols and inserts a placeholder character to forcibly separate them, allowing for byte-for-byte identical round-trip conversions.

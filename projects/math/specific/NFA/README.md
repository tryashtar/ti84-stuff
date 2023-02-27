This program determines if a [finite state machine](https://en.wikipedia.org/wiki/Finite-state_machine) state machine is a [DFA](https://en.wikipedia.org/wiki/Deterministic_finite_automaton); that is, every state has only and exactly one transition for every symbol in the alphabet.

First, the alphabet is provided, and the name of the starting state. Then you input the transitions for each state. Each transition is written with the name of an alphabet symbol, then the name of a state. If any new state names are discovered at this point, the program asks for its transitions later.

Since this check is trivial to verify by hand, I believe I intended to add more functionality to this program later.

The source for this program was written in the browser, so it contains comments and non-canonical syntax.

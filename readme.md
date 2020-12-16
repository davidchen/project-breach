# Project Purpose
To create a tool that can optimally solve any "Breach Protocol" mini-game found in _Cyberpunk 2077_.

# Rules of Breach Protocol
* The board will always be a square of size _n_ x _n_. There will be a buffer of size _b_.
* There will be multiple possible answer sequences. Board can have any number of solutions concurrently, up to total number of answer sequences.
* Every element on the board can only be selected once to be added to the buffer.
* Selection will always start at the top-most row, and will start alternating to columns and back to rows following the first row selection.
* Timer only begins upon selecting first element to add to buffer.

# How to Read Test Case File
The test case file is in _tests.txt_. Instructions are next to each line:

```text
6  # this denotes the size of the board, n; in this case a 6x6 board
E9,E9,7A,BD,55,55  # the next n lines make up the board; 6 lines for 6 rows
1C,1C,1C,7A,55,E9
1C,7A,7A,1C,55,1C
BD,E9,55,7A,55,7A
55,55,55,7A,55,1C
BD,BD,E9,1C,55,E9
55,55,7A;BD,BD,BD;55,E9,55  # the 2nd last line contain the possible answer sequences, delimited by semicolon
1,2,3  # the last line lists all the sequences that can be solved using just one buffer, in this case all 3 sequences can be solved in 1 buffer try
```
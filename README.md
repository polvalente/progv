#Attempt at a basic programming language called ProgV

The first interpreter is being written in Python.

The language has C-like syntax and currently contains the following:

VERSION 0.1:
- var declarations (no type declarations)
- function declarations
- if/else statements
- print() function
- return statement
- &&, ||, !, == for logical operations
- optional semicolons
- Math operations: +, -, /, \*(multiplication), **(power), %(mod)
- strings

VERSION 0.2:
- for and do-while loops
- != for logical difference
- continue and break statements for loops

VERSION 0.3:
- lists (implemented but not really tested)
- changed number type to float and int types

to-do:
- tuples
- map, filter, reduce
- classes


Running the interpreter:

- Clone the repo
- go to the root dir, which contains directories 'pvi' and 'tests'
- run 'python -m pvi <filename>' to run the code contained in the file you want to run

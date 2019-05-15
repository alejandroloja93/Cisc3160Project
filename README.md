# Cisc3160Project
Interpreter that takes inputs and is able to do basic math operations 

tok.py - This is the tokenizer, the language syntax which takes the group of integers, letters & symbols to peform operations. 

text_buufer.py - This reads the upcoming parts of the text

lexer.py - divides the input into tokens. 

Cparser.py - didn't name it parser.py as i kept getting errors that the module didn't exist. Anyways this file 
analyzes the tokens produced by the lexer. 

visitor.py - The output of the parser will be executed here. 

complier.py - Here is where the result is printed. 

Imports:
import sys - if you're using MAC, 
import re- I use this import for regular expressions. 
I use the .complile() function to compile a regular expression pattern into a regular expression object. 

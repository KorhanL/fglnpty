#!/usr/bin/env python3

import ctypes
import os
import sys

class c:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def die(message):
    print(f"{c.RED}oh no! {message}{c.RESET}")
    exit(1)

# compile gnl as a shared object
def compile(path, buffersize):
    flag = ""
    if buffersize is not None:
        flag = f" -D BUFFER_SIZE={buffersize} "
    return os.system(f"gcc -Wall -Werror -Wextra {flag} {path}get_next_line.c {path}get_next_line_utils.c -shared -o gnl.so")

# test a file against python's own readline
def testfile(path):
    fd = os.open(path, os.O_RDONLY)
    f = open(path, "r")

    gnlso = ctypes.CDLL("gnl.so")
    gnl = gnlso.get_next_line
    gnl.argtypes = [ctypes.c_int]
    gnl.restype = ctypes.c_char_p

    linenumber = 1
    errors = ""
    errorcount = 0
    while True:
        mine = gnl(fd)
        theirs = bytes(f.readline(), "ascii")
        if not mine and not theirs:
            break
        if mine != theirs:
            errors += f"{c.RED}line {linenumber}:\n\tgot:    \"{mine}\"\n\twanted: \"{theirs}\"{c.RESET}"
            errorcount += 1
        #else:
        #    print(f"{c.GREEN}line {linenumber}: {mine}{c.RESET}")
        linenumber += 1
    return errors, errorcount

# MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN

files = [
        "test_1char_noeol.txt",
        "test_alphabet.txt",
        "test_lipsum_noeol.txt",
        "test_simple.txt",
        "test_8chars.txt",
        "test_lipsum.txt",
        "test_nl.txt",
        ]

buffersizes = [
        None,
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50,
        100,
        1000,
        10000,
        100000,
        1000000,
        10000000,
        100000000,
        1000000000,
        10000000000,
        100000000000,
        1000000000000,
        ]

try:
    gnlpath = sys.argv[1]
except:
    die("first argument should be the path to your gnl repo")

if not os.path.isdir(gnlpath):
    die("first argument should be the path to your gnl repo")

for buffersize in buffersizes:
    print(f"{c.UNDERLINE}{c.BLUE}BUFFER_SIZE = {buffersize}{c.RESET}")
    if compile(gnlpath, buffersize):
        die("gcc went wrong")
    for file in files:
        print(f"TESTING FILE \"{file}\": ", end='')
        errors, errorcount = testfile("tests/"+file)
        if errorcount > 0:
            print(f"{c.RED}{errorcount} errors{c.RESET}\n")
            print(errors)
        else:
            print(f"{c.GREEN}All good!{c.RESET}")
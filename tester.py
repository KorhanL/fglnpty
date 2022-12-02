#!/usr/bin/env python3

import ctypes
import os
import sys
import glob

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

def red(string):
    return f"{c.RED}{string}{c.RESET}"

def green(string):
    return f"{c.GREEN}{string}{c.RESET}"

def blue(string):
    return f"{c.BLUE}{string}{c.RESET}"

def ul(string):
    return f"{c.UNDERLINE}{string}{c.RESET}"

def die(message):
    print(red(f"oh no! {message}"))
    exit(1)

# compile gnl as a shared object
def compile(path, buffersize):
    flag = ""
    if buffersize is not None:
        flag = f" -D BUFFER_SIZE={buffersize} "
    return os.system(f"gcc -Wall -Werror -Wextra {flag} {os.path.join(path, 'get_next_line.c')} {os.path.join(path, 'get_next_line_utils.c')} -shared -o gnl.so")

# test a file against python's own readline
def testfile(path, gnl):
    fd = os.open(path, os.O_RDONLY)
    f = open(path, "r")

    linenumber = 1
    errors = ""
    errorcount = 0
    while True:
        mine = gnl(fd)
        theirs = bytes(f.readline(), "ascii")
        if not mine and not theirs:
            break
        if mine != theirs:
            errors += red(f"line {linenumber}:\n\tgot:    \"{mine}\"\n\twanted: \"{theirs}\"");
            errorcount += 1
        linenumber += 1
    os.close(fd)
    f.close()
    return errors, errorcount

# MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN

files = glob.glob("tests/*")

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
    print(ul(blue(f"BUFFER_SIZE = {buffersize}")))
    if compile(gnlpath, buffersize):
        die("gcc went wrong")

    # import gnl as a c function
    gnlso = ctypes.CDLL("gnl.so")
    gnl = gnlso.get_next_line
    gnl.argtypes = [ctypes.c_int]
    gnl.restype = ctypes.c_char_p

    for file in files:
        print(f"TESTING FILE \"{file}\": ", end='', flush=True)
        errors, errorcount = testfile(file, gnl)
        if errorcount > 0:
            print(red(f"{errorcount} errors\n"))
            print(errors)
        else:
            print(green(f"All good!"))

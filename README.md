# `ft_gnl_tester`
A tester for getnextline that uses python's C interoperability.

I have no experience with python so this probably sucks.

## TODO:
- Isolation. If the `get_next_line` being tested has an infinite loop, the entire tester gets stuck and even `ctrl-c` won't stop it. Similarly, segfaults in `get_next_line` take down the entire tester.

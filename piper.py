#!/usr/bin/env python3

from piper import __author__, __version_str__
from piper.vm import piper_exec


def repl():
    piper_exec(input("[Command]: "))


def main():
    print(f"piper v{__version_str__}, created by {__author__}\n")

    while True:
        repl()


if __name__ == "__main__":
    main()

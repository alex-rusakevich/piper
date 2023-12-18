#!/usr/bin/env python3

import argparse
import sys

from piper import __author__, __version_str__
from piper.vm import piper_exec


def repl():
    piper_exec(input("[Command]: "))


def main():
    if len(sys.argv) == 1:  # repl mode
        print(f"piper v{__version_str__}, created by {__author__}\n")

        while True:
            repl()
    else:  # args mode
        parser = argparse.ArgumentParser(
            description=f"piper language interpreter, created by {__author__}"
        )
        parser.add_argument("file_in", type=str, nargs="?", help=".ppr file path")
        parser.add_argument(
            "-v", "--version", action="store_true", help="show version and exit"
        )
        parser.add_argument(
            "-c",
            "--command",
            type=str,
            help="execute command in arg and exit",
        )
        args = parser.parse_args()

        if args.version:
            print(__version_str__)
            sys.exit(0)

        if not args.command and not args.file_in:
            print("No file or command specified, stopping...")
            sys.exit(1)

        if args.command and args.file_in:
            print(
                "Cannot use -c command and [file_in] argument at the same time, stopping..."
            )
            sys.exit(1)

        if args.command:
            piper_exec(args.command)
        elif args.file_in:
            with open(args.file_in, "r", encoding="utf-8") as f:
                piper_exec(f.read())


if __name__ == "__main__":
    main()

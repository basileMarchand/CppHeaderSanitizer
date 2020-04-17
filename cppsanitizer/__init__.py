from .selfContainedHeader import test_self_contained_header


import argparse
import asyncio
import logging
import pathlib as pl 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-c", "--compiler", type=str, default="g++")
    parser.add_argument("-l", "--link", type=str, default="")
    parser.add_argument("-r", "--regex", type=str, default="*.h*")
    parser.add_argument("-j", "--job", type=int, default=4)
    parser.add_argument("include", type=str)

    args = parser.parse_args()

    loglevel = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel,
        format="%(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )


    include_path = pl.Path(args.include).expanduser().absolute()

    compiler_opt = {"CXX": args.compiler,
                    "CXXFLAGS": f"-I{str(include_path)}",
                    "LDFLAGS":args.link
    }

    asyncio.run(test_self_contained_header(compiler_opt, args.regex, include_path, args.job))
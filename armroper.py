#!/usr/bin/python3.4

import argparse
from capstone import *
import sys
from services.rop import *
import getopt

def usage():
    print("usage: %s [-h help] [-d <depth>] [-m <mode>] <binary_file>\n" %(sys.argv[0]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename")
    parser.add_argument("-d", "--depth",type=int)
    parser.add_argument("-m", "--mode",  action="store_true")
    args = parser.parse_args()

    if args.depth:
        depth = args.depth
    else:
        depth = 5
    if args.mode:
       mode = args.mode
    else:
    	mode = "arm"
    if args.filename:
       filename = str(args.filename)
    else:
    	print("You must enter a file with --file or -f flag!")
    	sys.exit(1)
    
    R = Rop(filename)
    R.run(depth, mode)
    R.output() 

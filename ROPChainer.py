import argparse
import os
import sys
from GadgetFinder import GetGadgets


def type_file(filename):
    """
    file type which checks if the file exists.
    """
    if not os.path.isfile(filename):
        print(f"File {filename} doesn't exist!")
        sys.exit(1)
    return filename


def type_type(type):
    """
    Type type which checks if the type exists in the GetGadgets Class.
    """
    if type.upper() not in GetGadgets.filters.keys() and type.upper() != "ALL":
        print(f"Type {type} doesn't exist!")
        print(f"Use one of the following: {' '.join(GetGadgets.filters.keys())}")
        sys.exit(1)
    return type.upper()


def type_bad(badChars):
    """
    Bad characters type which checks if the format matches the one expected.
    """
    badchars_s = badChars.strip().split(" ")
    for b in badchars_s:
        if len(b) != 2:
            print(f"Please use the following format for bad characters: -b '00 0n 0a 2d'")
            sys.exit(1)
        try:
            int(b, 16)
        except ValueError:
            print(f"{b} isn't a valid hex value.")
            sys.exit(1)
    return badChars


def run(filename, type, fulloutput, badChars):
    """
    Main run function.
    """
    getGadgets = GetGadgets(filename, fulloutput)
    gadgets = getGadgets.find(type=type, bad=badChars.strip().split(" "))
    print("")
    for k in gadgets.keys():
        singleGadgetList = []
        print(f"{k}")
        for gadget in gadgets[k]:
            if gadget.split(':')[1] not in singleGadgetList:
                print(f"{gadget}", end='')
                singleGadgetList.append(gadget.split(':')[1])
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to quickly parse rp output files to easily find gadgets')
    parser.add_argument("-f", "--file", type=type_file, required=True, help="Filename of the rp output file to parse.")
    parser.add_argument("-t", "--type", type=type_type, required=False,
                        help=f"Type to search for, default=ALL ({' '.join(GetGadgets.filters.keys())})")
    parser.add_argument("-b", "--bad", type=type_bad, required=False,
                        help=f"Bad characters to filter out (format: '00 0a 0n 26')")
    parser.add_argument("-F", "--full", action="store_true", required=False,
                        help="Display gadgets with more instructions.")

    args = parser.parse_args()
    if args.type == None:
        args.type = "ALL"

    if args.bad == None:
        args.bad = ""

    run(args.file, args.type, args.full, args.bad)

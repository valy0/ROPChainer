import os
import sys
import argparse
import GadgetFinder
from print_utils import pretty_print_output, pretty_print


def type_file(filename):
    """
    file type which checks if the file exists.
    """
    return filename if os.path.isfile(filename) else None


def type_dir(dirpath):
    """
    directory type which checks if the directory exists.
    """
    return dirpath if os.path.isdir(dirpath) else None


def type_type(type):
    """
    Type type which checks if the type exists in the GetGadgets Class.
    """
    if type.upper() not in GadgetFinder.FILTERS.keys() and type.upper() != "ALL":
        print(f"Type {type} doesn't exist!")
        print(f"Use one of the following: {' '.join(GadgetFinder.FILTERS.keys())}")
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


def run(filename, dirpath, gadgets_type, fulloutput, badChars):
    """
    Main run function.
    """
    output = {}
    singleGadgetList = []
    files = [filename] if filename else [os.path.join(dirpath, f) for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]

    for file in files:
        file_name = os.path.basename(file)
        pretty_print('[+]', color='blue_green', end='')
        print(f' Processing {file_name}', )
        getGadgets = GadgetFinder.GetGadgets(file, fulloutput)
        gadgets = getGadgets.find(type=gadgets_type, bad=badChars.strip().split(" "))

        for i, (k, v) in enumerate(gadgets.items()):
            if output.get(k) is None:
                output[k] = []                
            
            for gadget in gadgets[k]:
                if gadget.split(':')[1] not in singleGadgetList:
                    # Do not include "   (1 found)\n"
                    output[k].append(f'{gadget[:-12]}   (Found at {file_name})')
                    singleGadgetList.append(gadget.split(':')[1])

    pretty_print_output(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to quickly parse rp output files to easily find gadgets')
    parser.add_argument("-d", "--dir", type=type_dir, required=False, help="Path of directory with one or multiple rp output files to parse.")
    parser.add_argument("-f", "--file", type=type_file, required=False, help="Filename of the rp output file to parse.")
    parser.add_argument("-t", "--type", type=type_type, required=False,
                        help=f"Type to search for, default=ALL ({' '.join(GadgetFinder.FILTERS.keys())})")
    parser.add_argument("-b", "--bad", type=type_bad, required=False,
                        help=f"Bad characters to filter out (format: '00 0a 0n 26')")
    parser.add_argument("-F", "--full", action="store_true", required=False,
                        help="Display gadgets with more instructions.")

    args = parser.parse_args()
    if args.type == None:
        args.type = "ALL"

    if args.bad == None:
        args.bad = ""

    if args.file is None and args.dir is None:
        print('Provide a valid file or directory path')
        sys.exit(1)

    run(args.file, args.dir, args.type, args.full, args.bad)

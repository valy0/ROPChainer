import re
from GadgetFinder import GetGadgets


_COLORS = {
    'red': '0;31;40',
    'orange': '0;33;40',
    'white_bold': '1;37;40',
    'orange_bold': '1;33;40',
    'blue': '1;34;40',
}

_INSTRUCTIONS = [i.lower() for i in GetGadgets.filters.keys()]
_INSTRUCTIONS.append('ret')



def colored_text(text, color):
    return f'\x1b[{_COLORS[color]}m{text}\x1b[0m'


def pretty_print(text, color, end='\n'):
    print(f'\x1b[{_COLORS[color]}m{text}\x1b[0m', end=end)


def pretty_print_gadget(gadget, color):
    # Remove "   (1 found)\n", make ':' bold white and ';' blue
    output = gadget[:-12].replace(';', colored_text(';', 'blue')).replace(':', colored_text(':', 'white_bold'))

    # Make address red
    address = re.search('0x.{8}:', gadget).group(0)[:-1]
    output = output.replace(address, colored_text(address, 'red'))

    # Make instructions bold orange
    for i in _INSTRUCTIONS:
        output = output.replace(i, colored_text(i, 'orange_bold'))

    print(output)


def pretty_print_output(output):
    for idx, (instruction, gadgets) in enumerate(output.items()):
        print_tree = idx < len(output) - 1
        start_char = '└' if idx == len(output) - 1 else '├'
        print(f'{start_char}── ', end='')
        pretty_print(instruction, color='orange_bold')

        for sub_idx, gadget in enumerate(gadgets):
            tree = '│' if print_tree else ' '
            start_char = '└' if sub_idx == len(gadgets) - 1 else '├'
            print(f'{tree}  {start_char}── ', end='')
            pretty_print_gadget(gadget, color='red')

        if print_tree:
            print('│')

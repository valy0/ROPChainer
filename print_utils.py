import re
import GadgetFinder


_COLORS = {
    'red': '0;31;40',
    'orange': '0;33;40',
    'white_bold': '1;37;40',
    'orange_bold': '1;33;40',
    'blue': '1;34;40',
    'purple': '2;35;40',
    'blue_green': '1;32;40',
}

_INSTRUCTIONS = [f' {i.lower()} ' for i in GadgetFinder.FILTERS.keys()]
_INSTRUCTIONS += [f'{i} ' for i in [
    'pushad', 'popad', 'retn', 'ret ', 'and', 'les', 'cmp', 'sal', 'dec', ' or',
    'psrad', 'leave', 'adc', 'imul ', 'idiv ', 'mul', 'div', 'rol', 'out', 'in',
    'enter', 'shl', 'shr', 'xlatb', 'clc', 'stc', 'dword', 'ptr', 'test', 'sbb', 
    'int', 'rc', 'cld', 'sar', 'ror', 'rcr', 'movsb', 'hlt', 'sete', 'std', 'salc',
    'setne', 'inc', 'neg', 'not', 'byte', 'lodsb', 'lock', 'lea', 'int1', 'into'
]]


def colored_text(text, color):
    return f'\x1b[{_COLORS[color]}m{text}\x1b[0m'


def pretty_print(text, color, end='\n'):
    print(f'\x1b[{_COLORS[color]}m{text}\x1b[0m', end=end)


def pretty_print_gadget(gadget, color):
    # Make ':' bold white and ';' blue
    output = gadget.replace(';', colored_text(';', 'blue')).replace(':', colored_text(':', 'white_bold'))

    # Make the "Found in suffix" purple
    address = re.search('\\(.+\\)', gadget).group(0)
    output = output.replace(address, colored_text(address, 'purple'))

    # Make instructions bold orange
    for i in _INSTRUCTIONS:
        output = output.replace(i, colored_text(i, 'orange_bold'))

    # Make address red
    address = re.search('0x.{8}:', gadget).group(0)[:-1]
    output = output.replace(address, colored_text(address, 'red'))

    print(output)


def pretty_print_output(output):
    for idx, (instruction, gadgets) in enumerate(output.items()):
        if len(gadgets) == 0:
            continue

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

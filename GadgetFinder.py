import re


class GetGadgets:
    """
    Simple Class that will use regex to find matching gadgets
    """
    filters = {
        "ADD": "add \w\w\w, \w\w\w ;",
        "SUB": "sub \w\w\w, \w\w\w ;",
        "MOV": "mov \w\w\w, \w\w\w ;",
        "SET": "mov \w\w\w, 0x\d+ ;",
        "XOR": "xor \w\w\w, \w\w\w ;",
        "XCHG": "xchg \w\w\w, \w\w\w ;",
        "POP": "pop \w\w\w ;",
        "PUSH": "push \w\w\w ; pop \w\w\w ;",
        "PPR": "pop \w\w\w ; pop \w\w\w ;",
        "DEREF": "mov (\w\w\w, dword \[\w\w\w\]|dword \[\w\w\w\], \w\w\w) ;",
        "INC": "inc \w\w\w",
        "DECR": "dec \w\w\w"
    }

    def __init__(self, file, fulloutput):
        self.file = file
        if fulloutput:
            for k in self.filters.keys():
                self.filters[k] = ".*: .* " + self.filters[k] + " .* ; ret"
        else:
            for k in self.filters.keys():
                self.filters[k] = ".*: " + self.filters[k] + " ret "

    def checkGadget(self, gadget, type="ALL"):
        """
        Check if a gadget matches the type given.
        """
        matchlist = []
        if type != "ALL":
            if re.match(self.filters[type], gadget):
                matchlist.append(type)
            return matchlist, gadget
        for r in self.filters.keys():
            if re.match(self.filters[r], gadget) and r not in matchlist:
                matchlist.append(r)
        return matchlist, gadget

    def containsBadChars(self, gadget, bad=None):
        """
        Check if the gadget address contains any of the supplied bad characters
        """
        if bad is None:
            return False
        else:
            for b in bad:
                addr = gadget.split(":")[0]
                if "0x" in addr:
                    for i in range(0, len(addr), 2):
                        if addr[i:i + 2] == b:
                            return True
        return False

    def find(self, type="ALL", bad=None):
        """
        find gadgets matching the type given.
        """
        gadgets = {}
        for gadget in open(self.file):
            if self.containsBadChars(gadget, bad):
                continue
            checkG = self.checkGadget(gadget, type)
            if checkG[0]:
                for k in checkG[0]:
                    if k in gadgets.keys():
                        gadgets[k].append(checkG[1])
                    else:
                        gadgets[k] = [checkG[1]]
        return gadgets

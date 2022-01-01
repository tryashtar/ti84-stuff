import os
import bisect
import xmltodict

here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "tokens.xml"), "r", encoding="utf8") as token_file:
    tokens = xmltodict.parse(token_file.read())

token_symbol = {}
symbol_token = {}
def listy(thing):
    if type(thing) is list:
        return thing
    return [thing]

def load_token(leading_bytes, data):
    code = leading_bytes + int(data["@byte"][1:],16).to_bytes(1, 'big')
    if "@string" in data:
        if "@group" not in data or data["@group"] in ['_default','Greek','Y-Vars','Drawing Commands','Accented Letters']:
            symbol = data["@string"]
            if symbol == "\\n":
                symbol = "\n"
            token_symbol[code] = symbol
            symbol_token[symbol] = code
    if "Token" in data:
        for subtoken in listy(data["Token"]):
            load_token(code, subtoken)
    if "Alt" in data:
        for alt in listy(data["Alt"]):
            symbol_token[alt["@string"]] = code

for token in tokens["Tokens"]["Token"]:
    load_token(bytes(), token)
symbol_list = list(symbol_token.keys())
symbol_list.sort()
ambiguous_symbols = {}
for s1 in symbol_list:
    if len(s1) > 0:
        ambiguous_symbols[s1] = []
        for s2 in symbol_list:
            if s2.endswith(s1) and len(s2) > len(s1):
                ambiguous_symbols[s1].append(s2)
print(ambiguous_symbols)

class Program:
    def __init__(self, name, comment, code, version=(0,0), archived=False):
        self.name = name
        self.comment = comment
        self.code = code
        self.archived = archived
        self.version = version
    def __init__(self, data):
        self.name = data[60:60+8].decode('ascii').rstrip(' \0')
        self.version = int(data[68])
        self.comment = data[11:11+42].decode('ascii').rstrip(' \0')
        self.archived = data[69] == 0x80
        self.code = ""
        pos = 72
        if data[55] == 13:
            pos += 2
        indents = 0
        in_if = False
        after_newline = True
        while pos<len(data)-2:
            (symbol, lg, token) = self.write_symbol(self.code, data, pos)
            if after_newline:
                after_newline = False
                itoken = int.from_bytes(token, 'little')
                if in_if and itoken != 0xCF:
                    self.code += "\t"
                if itoken in [0xD4, 0xD0]:
                    indents = max(0, indents-1)
                self.code += "\t" * indents
                if itoken in [0xD0, 0xD1, 0xD2, 0xD3, 0xCF]:
                    indents += 1
                in_if = itoken == 0xCE
            if symbol == "\n":
                after_newline = True
            self.code += symbol
            pos += lg
    def compile(self):
        data = bytes()
        data += "**TI83F*".encode('ascii')
        data += bytes([26, 10, 0])
        data += (self.comment.ljust(42, '\0')).encode('ascii')
        token_data = bytes()
        pos = 0
        while pos<len(self.code):
            word = self.parse_token(self.code, pos)
            if word is not None:
                token_data += symbol_token[word]
                pos += len(word)
            else:
                pos += 1
        data += (len(token_data)+19).to_bytes(2, 'little')
        section = bytes([13, 0])
        section += (len(token_data)+2).to_bytes(2, 'little')
        section += bytes([5])
        section += self.name.ljust(8, '\0').encode("ascii")
        section += bytes([self.version])
        section += bytes([0x80]) if self.archived else bytes([0x00])
        section += (len(token_data)+2).to_bytes(2, 'little')
        section += (len(token_data)).to_bytes(2, 'little')
        section += token_data
        data += section
        data += (sum(section) & 0xFFFF).to_bytes(2, 'little')
        return data
    def write_symbol(self, so_far, stream, position):
        symbol = None
        bc = 0
        while symbol is None:
            bc += 1
            byte_string = stream[position:position+bc]
            symbol = token_symbol.get(byte_string)
        potential = so_far + symbol
        for ambig in ambiguous_symbols[symbol]:
            if potential.endswith(ambig):
                symbol = "‗" + symbol
                break
        return (symbol, bc, byte_string)
    def parse_token(self, stream, position):
        current = position + 1
        too_far = False
        possible = symbol_list
        
        while True:
            word = stream[position:current]
            if len(word) == 0:
                return None
            if too_far and word in symbol_token:
                return word
            next_word = word[0:len(word)-1]+chr(ord(word[-1])+1)
            possible = possible[bisect.bisect_left(possible, word):bisect.bisect_left(possible, next_word)]
            if len(possible) == 1 and len(possible[0]) == len(word):
                return word
            if len(possible) == 0 or current > len(stream):
                too_far = True
            current += (-1 if too_far else 1)

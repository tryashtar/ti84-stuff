import xmltodict

with open("tokens.xml", "r", encoding="utf8") as token_file:
    tokens = xmltodict.parse(token_file.read())

token_symbol = {}
symbol_token = {}

for token in tokens["Tokens"]["Token"]:
    top_byte = int(token["@byte"][1:],16).to_bytes(1, 'big')
    if "@string" in token:
        symbol = token["@string"]
        if symbol == "\\n":
            symbol = "\n"
        token_symbol[top_byte] = symbol
        symbol_token[symbol] = top_byte
    else:
        for subtoken in token["Token"]:
            bottom_byte = int(subtoken["@byte"][1:],16).to_bytes(1, 'big')
            combined = top_byte + bottom_byte
            token_symbol[combined] = subtoken["@string"]
            symbol_token[subtoken["@string"]] = combined            

class Program:
    def __init__(self, name, comment, code, version=(0,0), archived=False):
        self.name = name
        self.comment = comment
        self.code = code
        self.archived = archived
        self.version = version
    def __init__(self, data):
        self.name = data[60:60+8].decode('ascii').rstrip('\0')
        v = data[68:70]
        self.version = (int(v[0]), int(v[1]))
        self.comment = data[11:11+42].decode('ascii').rstrip(' \0')
        self.code = ""
        pos = 72
        self.archived = data[55] == 13
        if self.archived:
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
        data += (self.comment.ljust(42, ' ')).encode('ascii')
        symbol = ""
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
        section += bytes(self.version)
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
        possible = list(filter(lambda x: len(x) > len(symbol) and x.endswith(symbol) and (so_far+symbol).endswith(x), symbol_token.keys()))
        if len(possible) > 0:
            symbol = "‗" + symbol
        return (symbol, bc, byte_string)
    def parse_token(self, stream, position):
        current = position + 1
        too_far = False
        possible = list(symbol_token.keys())
        while True:
            word = stream[position:current]
            if len(word) == 0:
                return None
            if too_far and word in symbol_token:
                return word
            possible = list(filter(lambda x: x.startswith(word), possible))
            if len(possible) == 1 and len(possible[0]) == len(word):
                return word
            if len(possible) == 0 or current > len(stream):
                too_far = True
            current += (-1 if too_far else 1)

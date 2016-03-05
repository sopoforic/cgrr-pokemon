# Classic Game Resource Reader (CGRR): Parse resources from classic games.
# Copyright (C) 2016  Tracy Poff
#
# This file is part of CGRR.
#
# CGRR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CGRR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CGRR.  If not, see <http://www.gnu.org/licenses/>.
""" Python Character Mapping Codec pokemon_rby_us.

Maps strings from the US version of Pokemon Red/Blue/Yellow to unicode, using
PUA codepoints from 0xe000-0xe0ff for symbols that cannot be mapped 1-1 to
suitable unicode characters.

"""

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,encoding_table)

    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input,self.errors,decoding_table)[0]

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():
    return codecs.CodecInfo(
        name='pokemon_rby_us',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


### Decoding Table

decoding_table = (
    '\x00'     #  0x00 -> NULL
    '\ue001'   #  0x01 -> UNDEFINED
    '\ue002'   #  0x02 -> UNDEFINED
    '\ue003'   #  0x03 -> UNDEFINED
    '\ue004'   #  0x04 -> UNDEFINED
    '\ue005'   #  0x05 -> UNDEFINED
    '\ue006'   #  0x06 -> UNDEFINED
    '\ue007'   #  0x07 -> UNDEFINED
    '\ue008'   #  0x08 -> UNDEFINED
    '\ue009'   #  0x09 -> UNDEFINED
    '\ue00a'   #  0x0A -> UNDEFINED
    '\ue00b'   #  0x0B -> UNDEFINED
    '\ue00c'   #  0x0C -> UNDEFINED
    '\ue00d'   #  0x0D -> UNDEFINED
    '\ue00e'   #  0x0E -> UNDEFINED
    '\ue00f'   #  0x0F -> UNDEFINED
    '\ue010'   #  0x10 -> UNDEFINED
    '\ue011'   #  0x11 -> UNDEFINED
    '\ue012'   #  0x12 -> UNDEFINED
    '\ue013'   #  0x13 -> UNDEFINED
    '\ue014'   #  0x14 -> UNDEFINED
    '\ue015'   #  0x15 -> UNDEFINED
    '\ue016'   #  0x16 -> UNDEFINED
    '\ue017'   #  0x17 -> UNDEFINED
    '\ue018'   #  0x18 -> UNDEFINED
    '\ue019'   #  0x19 -> UNDEFINED
    '\ue01a'   #  0x1A -> UNDEFINED
    '\ue01b'   #  0x1B -> UNDEFINED
    '\ue01c'   #  0x1C -> UNDEFINED
    '\ue01d'   #  0x1D -> UNDEFINED
    '\ue01e'   #  0x1E -> UNDEFINED
    '\ue01f'   #  0x1F -> UNDEFINED
    '\ue020'   #  0x20 -> UNDEFINED
    '\ue021'   #  0x21 -> UNDEFINED
    '\ue022'   #  0x22 -> UNDEFINED
    '\ue023'   #  0x23 -> UNDEFINED
    '\ue024'   #  0x24 -> UNDEFINED
    '\ue025'   #  0x25 -> UNDEFINED
    '\ue026'   #  0x26 -> UNDEFINED
    '\ue027'   #  0x27 -> UNDEFINED
    '\ue028'   #  0x28 -> UNDEFINED
    '\ue029'   #  0x29 -> UNDEFINED
    '\ue02a'   #  0x2A -> UNDEFINED
    '\ue02b'   #  0x2B -> UNDEFINED
    '\ue02c'   #  0x2C -> UNDEFINED
    '\ue02d'   #  0x2D -> UNDEFINED
    '\ue02e'   #  0x2E -> UNDEFINED
    '\ue02f'   #  0x2F -> UNDEFINED
    '\ue030'   #  0x30 -> UNDEFINED
    '\ue031'   #  0x31 -> UNDEFINED
    '\ue032'   #  0x32 -> UNDEFINED
    '\ue033'   #  0x33 -> UNDEFINED
    '\ue034'   #  0x34 -> UNDEFINED
    '\ue035'   #  0x35 -> UNDEFINED
    '\ue036'   #  0x36 -> UNDEFINED
    '\ue037'   #  0x37 -> UNDEFINED
    '\ue038'   #  0x38 -> UNDEFINED
    '\ue039'   #  0x39 -> UNDEFINED
    '\ue03a'   #  0x3A -> UNDEFINED
    '\ue03b'   #  0x3B -> UNDEFINED
    '\ue03c'   #  0x3C -> UNDEFINED
    '\ue03d'   #  0x3D -> UNDEFINED
    '\ue03e'   #  0x3E -> UNDEFINED
    '\ue03f'   #  0x3F -> UNDEFINED
    '\ue040'   #  0x40 -> UNDEFINED
    '\ue041'   #  0x41 -> UNDEFINED
    '\ue042'   #  0x42 -> UNDEFINED
    '\ue043'   #  0x43 -> UNDEFINED
    '\ue044'   #  0x44 -> UNDEFINED
    '\ue045'   #  0x45 -> UNDEFINED
    '\ue046'   #  0x46 -> UNDEFINED
    '\ue047'   #  0x47 -> UNDEFINED
    '\ue048'   #  0x48 -> 
    '\ue049'   #  0x49 -> 
    '\ue04a'   #  0x4A -> PKMN (staggered)
    '\ue04b'   #  0x4B -> 
    '\ue04c'   #  0x4C -> 
    '\ue04d'   #  0x4D -> 
    '\ue04e'   #  0x4E -> 
    '\ue04f'   #  0x4F -> 
    '\u0003'   #  0x50 -> 
    '\ue051'   #  0x51 -> 
    '\ue052'   #  0x52 -> 
    '\ue053'   #  0x53 -> 
    '\ue054'   #  0x54 -> POKé
    '\ue055'   #  0x55 -> 
    '\ue056'   #  0x56 -> ......
    '\ue057'   #  0x57 -> 
    '\ue058'   #  0x58 -> 
    '\ue059'   #  0x59 -> 
    '\ue05a'   #  0x5A -> 
    '\ue05b'   #  0x5B -> PC
    '\ue05c'   #  0x5C -> TM
    '\ue05d'   #  0x5D -> TRAINER
    '\ue05e'   #  0x5E -> ROCKET
    '\ue05f'   #  0x5F -> 
    '\ue060'   #  0x60 -> A
    '\ue061'   #  0x61 -> B
    '\ue062'   #  0x62 -> C
    '\ue063'   #  0x63 -> D
    '\ue064'   #  0x64 -> E
    '\ue065'   #  0x65 -> F
    '\ue066'   #  0x66 -> G
    '\ue067'   #  0x67 -> H
    '\ue068'   #  0x68 -> I
    '\ue069'   #  0x69 -> V
    '\ue06a'   #  0x6A -> S
    '\ue06b'   #  0x6B -> L
    '\ue06c'   #  0x6C -> M
    '\ue06d'   #  0x6D -> :
    'ぃ'        #  0x6E -> 
    'ぅ'        #  0x6F -> 
    '‘'        #  0x70 -> 
    '’'        #  0x71 -> 
    '“'        #  0x72 -> 
    '”'        #  0x73 -> 
    '・'        #  0x74 -> 
    '…'        #  0x75 -> 
    'ぁ'        #  0x76 -> 
    'ぇ'        #  0x77 -> 
    'ぉ'        #  0x78 -> 
    '\ue079'   #  0x79 -> 
    '='        #  0x7A -> 
    '\ue07b'   #  0x7B -> 
    '\ue07c'   #  0x7C -> ||
    '\ue07d'   #  0x7D -> 
    '\ue07e'   #  0x7E -> 
    ' '        #  0x7F -> 
    'A'        #  0x80 -> 
    'B'        #  0x81 -> 
    'C'        #  0x82 -> 
    'D'        #  0x83 -> 
    'E'        #  0x84 -> 
    'F'        #  0x85 -> 
    'G'        #  0x86 -> 
    'H'        #  0x87 -> 
    'I'        #  0x88 -> 
    'J'        #  0x89 -> 
    'K'        #  0x8A -> 
    'L'        #  0x8B -> 
    'M'        #  0x8C -> 
    'N'        #  0x8D -> 
    'O'        #  0x8E -> 
    'P'        #  0x8F -> 
    'Q'        #  0x90 -> 
    'R'        #  0x91 -> 
    'S'        #  0x92 -> 
    'T'        #  0x93 -> 
    'U'        #  0x94 -> 
    'V'        #  0x95 -> 
    'W'        #  0x96 -> 
    'X'        #  0x97 -> 
    'Y'        #  0x98 -> 
    'Z'        #  0x99 -> 
    '('        #  0x9A -> 
    ')'        #  0x9B -> 
    ':'        #  0x9C -> 
    ';'        #  0x9D -> 
    '['        #  0x9E -> 
    ']'        #  0x9F -> 
    'a'        #  0xA0 -> 
    'b'        #  0xA1 -> 
    'c'        #  0xA2 -> 
    'd'        #  0xA3 -> 
    'e'        #  0xA4 -> 
    'f'        #  0xA5 -> 
    'g'        #  0xA6 -> 
    'h'        #  0xA7 -> 
    'i'        #  0xA8 -> 
    'j'        #  0xA9 -> 
    'k'        #  0xAA -> 
    'l'        #  0xAB -> 
    'm'        #  0xAC -> 
    'n'        #  0xAD -> 
    'o'        #  0xAE -> 
    'p'        #  0xAF -> 
    'q'        #  0xB0 -> 
    'r'        #  0xB1 -> 
    's'        #  0xB2 -> 
    't'        #  0xB3 -> 
    'u'        #  0xB4 -> 
    'v'        #  0xB5 -> 
    'w'        #  0xB6 -> 
    'x'        #  0xB7 -> 
    'y'        #  0xB8 -> 
    'z'        #  0xB9 -> 
    'é'        #  0xBA -> 
    '\ue0bb'   #  0xBB -> 'd
    '\ue0bc'   #  0xBC -> 'l
    '\ue0bd'   #  0xBD -> 's
    '\ue0be'   #  0xBE -> 't
    '\ue0bf'   #  0xBF -> 'v
    '\ue0c0'   #  0xC0 -> UNDEFINED
    '\ue0c1'   #  0xC1 -> UNDEFINED
    '\ue0c2'   #  0xC2 -> UNDEFINED
    '\ue0c3'   #  0xC3 -> UNDEFINED
    '\ue0c4'   #  0xC4 -> UNDEFINED
    '\ue0c5'   #  0xC5 -> UNDEFINED
    '\ue0c6'   #  0xC6 -> UNDEFINED
    '\ue0c7'   #  0xC7 -> UNDEFINED
    '\ue0c8'   #  0xC8 -> UNDEFINED
    '\ue0c9'   #  0xC9 -> UNDEFINED
    '\ue0ca'   #  0xCA -> UNDEFINED
    '\ue0cb'   #  0xCB -> UNDEFINED
    '\ue0cc'   #  0xCC -> UNDEFINED
    '\ue0cd'   #  0xCD -> UNDEFINED
    '\ue0ce'   #  0xCE -> UNDEFINED
    '\ue0cf'   #  0xCF -> UNDEFINED
    '\ue0d0'   #  0xD0 -> UNDEFINED
    '\ue0d1'   #  0xD1 -> UNDEFINED
    '\ue0d2'   #  0xD2 -> UNDEFINED
    '\ue0d3'   #  0xD3 -> UNDEFINED
    '\ue0d4'   #  0xD4 -> UNDEFINED
    '\ue0d5'   #  0xD5 -> UNDEFINED
    '\ue0d6'   #  0xD6 -> UNDEFINED
    '\ue0d7'   #  0xD7 -> UNDEFINED
    '\ue0d8'   #  0xD8 -> UNDEFINED
    '\ue0d9'   #  0xD9 -> UNDEFINED
    '\ue0da'   #  0xDA -> UNDEFINED
    '\ue0db'   #  0xDB -> UNDEFINED
    '\ue0dc'   #  0xDC -> UNDEFINED
    '\ue0dd'   #  0xDD -> UNDEFINED
    '\ue0de'   #  0xDE -> UNDEFINED
    '\ue0df'   #  0xDF -> UNDEFINED
    '\''       #  0xE0 -> 
    '\ue0e1'   #  0xE1 -> PK
    '\ue0e2'   #  0xE2 -> MN
    '-'        #  0xE3 -> 
    '\ue0e4'   #  0xE4 -> 'r
    '\ue0e5'   #  0xE5 -> 'm
    '?'        #  0xE6 -> 
    '!'        #  0xE7 -> 
    '.'        #  0xE8 -> 
    'ァ'        #  0xE9 -> 
    'ゥ'        #  0xEA -> 
    'ェ'        #  0xEB -> 
    '▷'        #  0xEC -> 
    '▶'        #  0xED -> 
    '▼'        #  0xEE -> 
    '♂'        #  0xEF -> 
    '\ue0f0'   #  0xF0 -> POKEMON DOLLAR
    '×'        #  0xF1 -> 
    '.'        #  0xF2 -> 
    '/'        #  0xF3 -> 
    ','        #  0xF4 -> 
    '♀'        #  0xF5 -> 
    '0'        #  0xF6 -> 
    '1'        #  0xF7 -> 
    '2'        #  0xF8 -> 
    '3'        #  0xF9 -> 
    '4'        #  0xFA -> 
    '5'        #  0xFB -> 
    '6'        #  0xFC -> 
    '7'        #  0xFD -> 
    '8'        #  0xFE -> 
    '9'        #  0xFF -> 
)

### Encoding table
encoding_table=codecs.charmap_build(decoding_table)

codecs.register(lambda s: getregentry() if s == 'pokemon_rby_us' else None)
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

Maps strings from the US version of Pokemon Gold/Silver/Crystal to unicode,
using PUA codepoints from 0xe000-0xe0ff for symbols that cannot be mapped
1-1 to suitable unicode characters.

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
        name='pokemon_gsc_us',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


### Decoding Table

decoding_table = (
    '\ue100'   #  0x00 ->
    '\ue101'   #  0x01 -> B
    '\ue102'   #  0x02 -> C
    '\ue103'   #  0x03 -> D
    '\ue104'   #  0x04 -> E
    '\ue105'   #  0x05 -> F
    '\ue106'   #  0x06 -> G
    '\ue107'   #  0x07 -> H
    '\ue108'   #  0x08 -> I
    '\ue109'   #  0x09 -> J
    '\ue10a'   #  0x0A -> K
    '\ue10b'   #  0x0B -> L
    '\ue10c'   #  0x0C -> M
    '\ue10d'   #  0x0D -> N
    '\ue10e'   #  0x0E -> O
    '\ue10f'   #  0x0F -> P
    '\ue110'   #  0x10 -> Q
    '\ue111'   #  0x11 -> R
    '\ue112'   #  0x12 -> S
    '\ue113'   #  0x13 -> T
    '\ue114'   #  0x14 -> Player's name
    '\ue115'   #  0x15 -> 
    '\ue116'   #  0x16 -> 
    '\ue117'   #  0x17 -> X
    '\ue118'   #  0x18 -> Y
    '\ue119'   #  0x19 -> Z
    '\ue11a'   #  0x1A -> ()
    '\ue11b'   #  0x1B -> )
    '\ue11c'   #  0x1C -> :
    '\ue11d'   #  0x1D -> ;
    '\ue11e'   #  0x1E -> [
    '\ue11f'   #  0x1F -> 
    '\ue120'   #  0x20 -> q
    '\ue121'   #  0x21 -> r
    '\ue122'   #  0x22 -> 
    '\ue123'   #  0x23 -> 
    '\ue124'   #  0x24 -> POKé (staggered)
    '\ue125'   #  0x25 -> 
    '\ue126'   #  0x26 -> w
    '\ue127'   #  0x27 -> x
    '\ue128'   #  0x28 -> y
    '\ue129'   #  0x29 -> z
    '\ue12a'   #  0x2A -> 
    '\ue12b'   #  0x2B -> 
    '\ue12c'   #  0x2C -> 
    '\ue12d'   #  0x2D -> 
    '\ue12e'   #  0x2E -> 
    '\ue12f'   #  0x2F -> 
    '\ue130'   #  0x30 -> Ä
    '\ue131'   #  0x31 -> Ö
    '\ue132'   #  0x32 -> Ü
    '\ue133'   #  0x33 -> ä
    '\ue134'   #  0x34 -> ö
    '\ue135'   #  0x35 -> 
    '\ue136'   #  0x36 -> 
    '\ue137'   #  0x37 -> 
    '\ue138'   #  0x38 -> RED
    '\ue139'   #  0x39 -> GREEN
    '\ue13a'   #  0x3A -> 
    '\ue13b'   #  0x3B -> 
    '\ue13c'   #  0x3C -> 
    '\ue13d'   #  0x3D -> 
    '\ue13e'   #  0x3E -> 
    '\ue13f'   #  0x3F -> Opposing trainer's name
    '\ue140'   #  0x40 -> Z
    '\ue141'   #  0x41 -> (
    '\ue142'   #  0x42 -> )
    '\ue143'   #  0x43 -> ":"
    '\ue144'   #  0x44 -> 
    '\ue145'   #  0x45 -> 
    '\ue146'   #  0x46 -> 
    '\ue147'   #  0x47 -> 
    '\ue148'   #  0x48 -> 
    '\ue149'   #  0x49 -> MOM
    '\ue04a'   #  0x4A -> PKMN (staggered)
    '\ue14b'   #  0x4B -> 
    '\ue14c'   #  0x4C -> 
    '\ue14d'   #  0x4D -> 'r
    '\ue14e'   #  0x4E -> \n\n
    '\ue14f'   #  0x4F -> \n
    '\u0003'   #  0x50 -> 
    '\ue151'   #  0x51 -> Prompts player to press a button
    '\ue152'   #  0x52 -> Player's name
    '\ue153'   #  0x53 -> Rival's name
    '\ue054'   #  0x54 -> POKé
    '\ue155'   #  0x55 -> Prompts player to press a button
    '\ue056'   #  0x56 -> ......
    '\ue157'   #  0x57 -> End of dialogue
    '\ue158'   #  0x58 -> End of dialogue
    '\ue159'   #  0x59 -> inactive Pokémon's name in battle
    '\ue15a'   #  0x5A -> active Pokémon's name in battle
    '\ue05b'   #  0x5B -> PC
    '\ue05c'   #  0x5C -> TM
    '\ue05d'   #  0x5D -> TRAINER
    '\ue05e'   #  0x5E -> ROCKET
    '\ue15f'   #  0x5F -> . + \u0003
    '\ue160'   #  0x60 -> 
    '▲'        #  0x61 -> 
    '\ue162'   #  0x62 -> 
    '\ue163'   #  0x63 -> D
    '\ue164'   #  0x64 -> E
    '\ue165'   #  0x65 -> F
    '\ue166'   #  0x66 -> G
    '\ue167'   #  0x67 -> H
    '\ue168'   #  0x68 -> I
    '\ue169'   #  0x69 -> V
    '\ue16a'   #  0x6A -> S
    '\ue16b'   #  0x6B -> L
    '\ue16c'   #  0x6C -> M
    '\ue16d'   #  0x6D -> :
    'ぃ'        #  0x6E -> 
    'ぅ'        #  0x6F -> 
    '\ue170'   #  0x70 -> PO
    '\ue171'   #  0x71 -> Ké
    '“'        #  0x72 -> 
    '”'        #  0x73 -> 
    '・'        #  0x74 -> 
    '…'        #  0x75 -> 
    'ぁ'        #  0x76 -> 
    'ぇ'        #  0x77 -> 
    'ぉ'        #  0x78 -> 
    '\ue179'   #  0x79 -> 
    '\ue180'   #  0x7A -> 
    '\ue17b'   #  0x7B -> 
    '\ue07c'   #  0x7C -> ||
    '\ue17d'   #  0x7D -> 
    '\ue17e'   #  0x7E -> 
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
    '\ue1ba'   #  0xBA -> 
    '\ue1bb'   #  0xBB -> 
    '\ue1bc'   #  0xBC -> 
    '\ue1bd'   #  0xBD -> 
    '\ue1be'   #  0xBE -> 
    '\ue1bf'   #  0xBF -> 
    'Ä'        #  0xC0 -> 
    'Ö'        #  0xC1 -> 
    'Ü'        #  0xC2 -> 
    'ä'        #  0xC3 -> 
    'ö'        #  0xC4 -> 
    'ü'        #  0xC5 -> 
    '\ue1c6'   #  0xC6 -> 
    '\ue1c7'   #  0xC7 -> 
    '\ue1c8'   #  0xC8 -> 
    '\ue1c9'   #  0xC9 -> 
    '\ue1ca'   #  0xCA -> 
    '\ue1cb'   #  0xCB -> 
    '\ue1cc'   #  0xCC -> 
    '\ue1cd'   #  0xCD -> 
    '\ue1ce'   #  0xCE -> 
    '\ue1cf'   #  0xCF -> 
    '\ue1d0'   #  0xD0 -> 'd
    '\ue1d1'   #  0xD1 -> 'l
    '\ue1d2'   #  0xD2 -> 'm
    '\ue1d3'   #  0xD3 -> 'r
    '\ue1d4'   #  0xD4 -> 's
    '\ue1d5'   #  0xD5 -> 't
    '\ue1d6'   #  0xD6 -> 'v
    '\ue1d7'   #  0xD7 -> 
    '\ue1d8'   #  0xD8 -> 
    '\ue1d9'   #  0xD9 -> 
    '\ue1da'   #  0xDA -> 
    '\ue1db'   #  0xDB -> 
    '\ue1dc'   #  0xDC -> 
    '\ue1dd'   #  0xDD -> 
    '\ue1de'   #  0xDE -> 
    '←'        #  0xDF -> 
    '\''       #  0xE0 -> 
    '\ue0e1'   #  0xE1 -> PK
    '\ue0e2'   #  0xE2 -> MN
    '-'        #  0xE3 -> 
    '\ue1e4'   #  0xE4 -> 
    '\ue1e5'   #  0xE5 -> 
    '?'        #  0xE6 -> 
    '!'        #  0xE7 -> 
    '.'        #  0xE8 -> 
    '&'        #  0xE9 -> 
    'é'        #  0xEA -> 
    '→'        #  0xEB -> 
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

codecs.register(lambda s: getregentry() if s == 'pokemon_gsc_us' else None)
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
"""Parses Pokemon Red/Blue/Yellow files."""

import os
import struct
import datetime

try:
    from enum import IntEnum
except ImportError:
    from enum34 import IntEnum

from cgrr import FileReader

from .encodings import pokemon_rby_us
from .common import Pokemon, PokemonType, Move, Item

key = "pokemon_red_us_a"
title = "Pokémon Red Version (US)"
developer = "Game Freak, Inc."
description = "Pokémon Red Version (US)"

species_index = {
    1 : 112, 2 : 115, 3 : 32, 4 : 35, 5 : 21,
    6 : 100, 7 : 34,  8 : 80, 9 : 2,  10 : 103,
    11 : 108, 12 : 102, 13 : 88, 14 : 94, 15 : 29,
    16 : 31, 17 : 104, 18 : 111, 19 : 131, 20 : 59,
    21 : 151, 22 : 130, 23 : 90, 24 : 72,  25 : 92,
    26 : 123, 27 : 120, 28 : 9, 29 : 127, 30 : 114,
    31 : 0, 32 : 0, 33 : 58, 34 : 95, 35 : 22,
    36 : 16, 37 : 79, 38 : 64, 39 : 75, 40 : 113,
    41 : 67, 42 : 122, 43 : 106, 44 : 107, 45 : 24,
    46 : 47, 47 : 54, 48 : 96, 49 : 76, 50 : 0,
    51 : 126, 52 : 0, 53 : 125, 54 : 82, 55 : 109,
    56 : 0, 57 : 56, 58 : 86, 59 : 50, 60 : 128,
    61 : 0, 62 : 0, 63 : 0, 64 : 83, 65 : 48,
    66 : 149, 67 : 0, 68 : 0, 69 : 0, 70 : 84,
    71 : 60, 72 : 124, 73 : 146, 74 : 144, 75 : 145,
    76 : 132, 77 : 52, 78 : 98, 79 : 0, 80 : 0,
    81 : 0, 82 : 37, 83 : 38, 84 : 25, 85 : 26,
    86 : 0, 87 : 0, 88 : 147, 89 : 148, 90 : 140,
    91 : 141, 92 : 116, 93 : 117, 94 : 0, 95 : 0,
    96 : 27, 97 : 28, 98 : 138, 99 : 139, 100 : 39,
    101 : 40, 102 : 133, 103 : 136, 104 : 135, 105 : 134,
    106 : 66, 107 : 41, 108 : 23, 109 : 46, 110 : 61,
    111 : 62, 112 : 13, 113 : 14, 114 : 15, 115 : 0,
    116 : 85, 117 : 57, 118 : 51, 119 : 49, 120 : 87,
    121 : 0, 122 : 0, 123 : 10, 124 : 11, 125 : 12,
    126 : 68, 127 : 0, 128 : 55, 129 : 97, 130 : 42,
    131 : 150, 132 : 143, 133 : 129, 134 : 0, 135 : 0,
    136 : 89, 137 : 0, 138 : 99, 139 : 91, 140 : 0,
    141 : 101, 142 : 36, 143 : 110, 144 : 53, 145 : 105,
    146 : 0, 147 : 93, 148 : 63, 149 : 65, 150 : 17,
    151 : 18, 152 : 121, 153 : 1, 154 : 3, 155 : 73,
    156 : 0, 157 : 118, 158 : 119, 159 : 0, 160 : 0,
    161 : 0, 162 : 0, 163 : 77, 164 : 78, 165 : 19,
    166 : 20, 167 : 33, 168 : 30, 169 : 74, 170 : 137,
    171 : 142, 172 : 0, 173 : 81, 174 : 0, 175 : 0,
    176 : 4, 177 : 7, 178 : 5, 179 : 8, 180 : 6,
    181 : 0, 182 : 0, 183 : 0, 184 : 0, 185 : 43,
    186 : 44, 187 : 45, 188 : 69, 189 : 70, 190 : 71,
}

def rby_us_string_decode(b):
    return b.decode('pokemon_rby_us').split('\u0003')[0]

def rby_us_string_encode(s, max_len):
    b = s.encode('pokemon_rby_us')
    if len(b) < max_len:
        b += '\u0003'.encode('pokemon_rby_us')
    b += bytes(max_len - len(b))
    return b

def rby_us_string_list_encode(l, max_len):
    b = b''
    for s in l:
        b += rby_us_string_encode(s, max_len)
    return b

def parse_pokedex_list(b):
    return { Pokemon(i+1) : bool((b[i//8] >> (i % 8)) & 1) for i in range(len(b)*8)}

def unparse_pokedex_list(d):
    size = len(d)//8
    b = b''
    for i in range(size):
        n = 0
        for j in range(8):
            n += d[Pokemon(8*i + j + 1)] << j
        b += bytes([n])
    return b

item_list_entry_reader = FileReader(
    format = [
        ("item", "B"),
        ("count", "B")
    ],
    massage_in = {
        'item' : Item,
    },
    massage_out = {
        'item' : lambda i: i.value,
    },
    byte_order = ">"
)

def parse_item_list(b):
    if b[0] == 0:
        return []
    else:
        count = struct.unpack("<B", b[:1])[0]
        item_list = []
        for i in range(count):
            item_list.append(item_list_entry_reader.unpack(b[2*i + 1 : 2*i + 3]))
        return item_list

def unparse_item_list(l):
    if not l:
        return b'\0\xff'
    else:
        b = struct.pack('>B', len(l))
        for i in l:
            b += item_list_entry_reader.pack(i)
        b += b'\xff'
        return b

def parse_bcd(b):
    total = 0
    p = len(b)*2 - 1
    for i in range(p + 1):
        byte = b[i//2]
        right = bool(i % 2)
        if not right:
            total += 10**(p-i) * (byte >> 4)
        else:
            total += 10**(p-i) * (byte & 0xf)
    return total

def unparse_bcd(b, size):
    ds = [(b // 10**(size*2 - 1 - i)) % 10 for i in range(size*2)]
    digits = []
    for i in range(size):
        digits.extend([(ds[i*2] << 4) + ds[i*2 + 1]])
    return bytes(digits)

class BattleStyle(IntEnum):
    BATTLE_STYLE_SWITCH = 0
    BATTLE_STYLE_SET    = 1

class Sound(IntEnum):
    SOUND_MONO       = 0
    SOUND_STEREO     = 1 # Called Earphone1 in Yellow
    SOUND_EARPHONE_2 = 2
    SOUND_EARPHONE_3 = 3

class TextSpeed(IntEnum):
    TEXT_SPEED_FAST   = 1
    TEXT_SPEED_NORMAL = 3
    TEXT_SPEED_SLOW   = 5

def parse_options(b):
    return {
        'battle_effects' : b & 0x80 == 0,
        'battle_style'   : BattleStyle(b & 0x40),
        'sound'          : Sound(b & 0x30),
        'text_speed'     : TextSpeed(b & 0x07),
    }

def unparse_options(o):
    return (
          0x80 * (not o['battle_effects'])
        + 0x40 * o['battle_style'].value
        + 0x30 * o['sound'].value
        + o['text_speed'].value
    )

class Badge(IntEnum):
    BADGE_BOULDER = 1
    BADGE_CASCADE = 2
    BADGE_THUNDER = 4
    BADGE_RAINBOW = 8
    BADGE_SOUL    = 16
    BADGE_MARSH   = 32
    BADGE_VOLCANO = 64
    BADGE_EARTH   = 128

def parse_badges(b):
    return [Badge(b & 2**i) for i in range(8) if b & 2**i]

def unparse_badges(badges):
    return sum(b.value for b in badges)

def parse_current_pc_box(b):
    return {
        'top_bit'     : b & 0x80,
        'current_box' : (b & 0x0F) + 1
    }

def unparse_current_pc_box(d):
    return d['top_bit'] * 0x80 + d['current_box'] - 1

def parse_time_played(b):
    hours, minutes, seconds = struct.unpack('<HBB', b)
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

def unparse_time_played(td):
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    seconds = int(td.total_seconds() % 60)
    return struct.pack('<HBB', hours, minutes, seconds)

def parse_species(b):
    l = list(b[:-1])
    return [Pokemon(species_index[i]) for i in l if i in species_index]

def unparse_species(l):
    return bytes([s.value for s in l] + [0xff])

def parse_iv(b):
    return {
        'attack'  : b[0] >> 4,
        'defense' : b[0] & 0x0F,
        'speed'   : b[1] >> 4,
        'special' : b[1] & 0x0F,
    }

def unparse_iv(i):
    return bytes([(i['attack'] << 4) + i['defense'], (i['speed'] << 4) + i['special']])

def species_to_enum(i):
    return Pokemon(species_index[i])

def enum_to_species(e):
    return list(species_index.keys())[list(species_index.values()).index(e.value)]

class Status(IntEnum):
    ASLEEP    = 0x04
    POISONED  = 0x08
    BURNED    = 0x10
    FROZEN    = 0x20
    PARALYZED = 0x40

pokemon_full_reader = FileReader(
    format = [
        ("species", "B"),
        ("current_hp", "H"),
        ("level_in_box", "B"),
        ("status_condition", "B"),
        ("type_1", "B"),
        ("type_2", "B"),
        ("catch_rate", "B"),
        ("move_1", "B"),
        ("move_2", "B"),
        ("move_3", "B"),
        ("move_4", "B"),
        ("original_trainer_id", "H"),
        ("experience_points", "3s"),
        ("hp_ev", "H"),
        ("attack_ev", "H"),
        ("defense_ev", "H"),
        ("speed_ev", "H"),
        ("special_ev", "H"),
        ("iv", "2s"),
        ("move_1_pp", "B"),
        ("move_2_pp", "B"),
        ("move_3_pp", "B"),
        ("move_4_pp", "B"),
        ("level", "B"),
        ("maximum_hp", "H"),
        ("attack", "H"),
        ("defense", "H"),
        ("speed", "H"),
        ("special", "H"),
    ],
    massage_in = {
        'species'           : lambda i: Pokemon(species_index[i]),
        'status_condition'  : lambda s: [st for st in Status if (st.value & s)],
        'type_1'            : lambda i: PokemonType(i) if i in [e.value for e in PokemonType] else None,
        'type_2'            : lambda i: PokemonType(i) if i in [e.value for e in PokemonType] else None,
        'move_1'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'move_2'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'move_3'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'move_4'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'experience_points' : lambda b: (b[0] << 16) + (b[1] << 8) + b[2],
        'iv'                : parse_iv,
    },
    massage_out = {
        'species'           : lambda e: list(species_index.keys())[list(species_index.values()).index(e.value)],
        'status_condition'  : lambda s: sum(st.value for st in s),
        'type_1'            : lambda t: t.value if t else 0,
        'type_2'            : lambda t: t.value if t else 0,
        'move_1'            : lambda m: m.value if m else 0,
        'move_2'            : lambda m: m.value if m else 0,
        'move_3'            : lambda m: m.value if m else 0,
        'move_4'            : lambda m: m.value if m else 0,
        'experience_points' : lambda x: bytes([x >> 16, (x >> 8) & 0xFF, x & 0xFF]),
        'iv'                : unparse_iv,
    },
    byte_order = ">"
)

team_pokemon_reader = FileReader(
    format = [
        ("count", "B"),
        ("species", "7s"),
        ("pokemon", "264s"),
        ("ot_names", "66s"),
        ("names", "66s"),
    ],
    massage_in = {
        'species'  : parse_species,
        'ot_names' : lambda s: [rby_us_string_decode(s[i*11:(i+1)*11]) for i in range(6)],
        'names' : lambda s: [rby_us_string_decode(s[i*11:(i+1)*11]) for i in range(6)],
    },
    massage_out = {
        'species'  : unparse_species,
        'ot_names' : lambda l: rby_us_string_list_encode(l, 11),
        'names' : lambda l: rby_us_string_list_encode(l, 11),
    },
    byte_order = ">"
)

def parse_team_pokemon(b):
    size = 44
    d = team_pokemon_reader.unpack(b)
    d['pokemon'] = [pokemon_full_reader.unpack(d['pokemon'][size*i : size*(i+1)]) for i in range(d['count'])]
    for i in range(d['count']):
        d['pokemon'][i]['name'] = d['names'][i]
        d['pokemon'][i]['ot_name'] = d['ot_names'][i]
    return d

def unparse_team_pokemon(d):
    d = d.copy()
    b = b''
    if len(d['pokemon']) > 6:
        raise ValueError("At most 6 pokemon can be in the team. You have {}.".format(len(d['pokemon'])))
    d['count'] = len(d['pokemon'])
    d['names'] = [d['pokemon'][i]['name'] for i in range(d['count'])]
    d['ot_names'] = [d['pokemon'][i]['ot_name'] for i in range(d['count'])]
    d['species'] = [d['pokemon'][i]['species'] for i in range(d['count'])]
    for p in d['pokemon']:
        b += pokemon_full_reader.pack(p)
    b += bytes(264-len(b))
    d['pokemon'] = b
    return team_pokemon_reader.pack(d)

pokemon_brief_reader = FileReader(
    format = [
        ("species", "B"),
        ("current_hp", "H"),
        ("level_in_box", "B"),
        ("status_condition", "B"),
        ("type_1", "B"),
        ("type_2", "B"),
        ("catch_rate", "B"),
        ("move_1", "B"),
        ("move_2", "B"),
        ("move_3", "B"),
        ("move_4", "B"),
        ("original_trainer_id", "H"),
        ("experience_points", "3s"),
        ("hp_ev", "H"),
        ("attack_ev", "H"),
        ("defense_ev", "H"),
        ("speed_ev", "H"),
        ("special_ev", "H"),
        ("iv", "2s"),
        ("move_1_pp", "B"),
        ("move_2_pp", "B"),
        ("move_3_pp", "B"),
        ("move_4_pp", "B"),
    ],
    massage_in = {
        'species'           : lambda i: Pokemon(species_index[i]),
        'status_condition'  : lambda s: [st for st in Status if (st.value & s)],
        'type_1'            : lambda i: PokemonType(i) if i in [e.value for e in PokemonType] else None,
        'type_2'            : lambda i: PokemonType(i) if i in [e.value for e in PokemonType] else None,
        'move_1'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'move_2'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'move_3'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'move_4'            : lambda i: Move(i) if i in [e.value for e in Move] else None,
        'experience_points' : lambda b: (b[0] << 16) + (b[1] << 8) + b[2],
        'iv'                : parse_iv,
    },
    massage_out = {
        'species'           : lambda e: list(species_index.keys())[list(species_index.values()).index(e.value)],
        'status_condition'  : lambda s: sum(st.value for st in s),
        'type_1'            : lambda t: t.value if t else 0,
        'type_2'            : lambda t: t.value if t else 0,
        'move_1'            : lambda m: m.value if m else 0,
        'move_2'            : lambda m: m.value if m else 0,
        'move_3'            : lambda m: m.value if m else 0,
        'move_4'            : lambda m: m.value if m else 0,
        'experience_points' : lambda x: bytes([x >> 16, (x >> 8) & 0xFF, x & 0xFF]),
        'iv'                : unparse_iv,
    },
    byte_order = ">"
)

pc_box_reader = FileReader(
    format = [
        ("count", "B"),
        ("species", "21s"),
        ("pokemon", "660s"),
        ("ot_names", "220s"),
        ("names", "220s"),
    ],
    massage_in = {
        'species'  : parse_species,
        'ot_names' : lambda s: [rby_us_string_decode(s[i*11:(i+1)*11]) for i in range(20)],
        'names' : lambda s: [rby_us_string_decode(s[i*11:(i+1)*11]) for i in range(20)],
    },
    massage_out = {
        'species'  : unparse_species,
        'ot_names' : lambda l: rby_us_string_list_encode(l, 11),
        'names' : lambda l: rby_us_string_list_encode(l, 11),
    },
    byte_order = ">"
)

def parse_pc_box_pokemon(b):
    size = 33
    d = pc_box_reader.unpack(b)
    if d['count'] > 20:
        d['count'] = 0
    d['pokemon'] = [pokemon_brief_reader.unpack(d['pokemon'][size*i : size*(i+1)]) for i in range(d['count'])]
    d['names'] = d['names'][:d['count']]
    d['ot_names'] = d['ot_names'][:d['count']]
    d['species'] = d['species'][:d['count']]
    for i in range(d['count']):
        d['pokemon'][i]['name'] = d['names'][i]
        d['pokemon'][i]['ot_name'] = d['ot_names'][i]
    return d

def unparse_pc_box_pokemon(d):
    d = d.copy()
    b = b''
    if len(d['pokemon']) > 20:
        raise ValueError("At most 20 pokemon can be in a box. You have {}.".format(len(d['pokemon'])))
    d['count'] = len(d['pokemon'])
    d['names'] = [d['pokemon'][i]['name'] for i in range(d['count'])]
    d['ot_names'] = [d['pokemon'][i]['ot_name'] for i in range(d['count'])]
    d['species'] = [d['pokemon'][i]['species'] for i in range(d['count'])]
    for p in d['pokemon']:
        b += pokemon_full_reader.pack(p)
    b += bytes(1122-len(b))
    d['pokemon'] = b
    return pc_box_reader.pack(d)

save_file_reader = FileReader(
    format = [
        ("unknown1", "9624s"),            # 0x0000-0x2597
        ("player_name", "11s"),           # 0x2598-0x25A2
        ("pokedex_owned", "19s"),         # 0x25A3-0x25B5
        ("pokedex_seen", "19s"),          # 0x25B6-0x25C8
        ("pocket_item_list", "42s"),      # 0x25C9-0x25F2
        ("money", "3s"),                  # 0x25F3-0x25F5
        ("rival_name", "11s"),            # 0x25F6-0x2600
        ("options", "B"),                 # 0x2601
        ("badges", "B"),                  # 0x2602
        ("unknown2", "2s"),               # 0x2603-0x2604
        ("player_trainer_id", "H"),       # 0x2605-0x2606
        ("unknown3", "277s"),             # 0x2607-0x271B
        ("pikachu_friendship", "B"),      # 0x271C
        ("unknown4", "201s"),             # 0x271D-0x27E5
        ("pc_item_list", "102s"),         # 0x27E6-0x284B
        ("current_pc_box", "B"),          # 0x284C
        ("unknown5", "3s"),               # 0x284D-0x284F
        ("casino_coins", "2s"),           # 0x2850-0x2851
        ("unknown6", "1179s"),            # 0x2852-0x2CEC
        ("time_played", "4s"),            # 0x2CED-0x2CF0
        ("unknown7", "571s"),             # 0x2CF1-0x2F2B
        ("team_pokemon", "404s"),    # 0x2F2C-0x30BF
        ("current_box_pokemon", "1122s"), # 0x30C0-0x3521
        ("unknown8", "s"),                # 0x3522
        ("checksum", "B"),                # 0x3523
        ("unknown9", "2780s"),            # 0x3524-0x3FFF
        ("pc_box_1", "1122s"),            # 0x4000
        ("pc_box_2", "1122s"),            # 0x4462
        ("pc_box_3", "1122s"),            # 0x48C4
        ("pc_box_4", "1122s"),            # 0x4D26
        ("pc_box_5", "1122s"),            # 0x5188
        ("pc_box_6", "1122s"),            # 0x55EA-0x5A4B
        ("unknown10", "1460s"),           # 0x5A4C-0x5FFF
        ("pc_box_7", "1122s"),            # 0x6000
        ("pc_box_8", "1122s"),            # 0x6462
        ("pc_box_9", "1122s"),            # 0x68C4
        ("pc_box_10", "1122s"),           # 0x6D26
        ("pc_box_11", "1122s"),           # 0x7188
        ("pc_box_12", "1122s"),           # 0x75EA-0x7A4B
        ("unknown11", "1460s"),           # the rest of the file
    ],
    massage_in = {
        'player_name'         : rby_us_string_decode,
        'pokedex_owned'       : parse_pokedex_list,
        'pokedex_seen'        : parse_pokedex_list,
        'pocket_item_list'    : parse_item_list,
        'money'               : parse_bcd,
        'rival_name'          : rby_us_string_decode,
        'options'             : parse_options,
        'badges'              : parse_badges,
        'pc_item_list'        : parse_item_list,
        'current_pc_box'      : parse_current_pc_box,
        'casino_coins'        : parse_bcd,
        'time_played'         : parse_time_played,
        'team_pokemon'        : parse_team_pokemon,
        'current_box_pokemon' : parse_pc_box_pokemon,
        'pc_box_1'            : parse_pc_box_pokemon,
        'pc_box_2'            : parse_pc_box_pokemon,
        'pc_box_3'            : parse_pc_box_pokemon,
        'pc_box_4'            : parse_pc_box_pokemon,
        'pc_box_5'            : parse_pc_box_pokemon,
        'pc_box_6'            : parse_pc_box_pokemon,
        'pc_box_7'            : parse_pc_box_pokemon,
        'pc_box_8'            : parse_pc_box_pokemon,
        'pc_box_9'            : parse_pc_box_pokemon,
        'pc_box_10'           : parse_pc_box_pokemon,
        'pc_box_11'           : parse_pc_box_pokemon,
        'pc_box_12'           : parse_pc_box_pokemon,
    },
    massage_out = {
        'player_name'         : lambda s: rby_us_string_encode(s, 11),
        'pokedex_owned'       : unparse_pokedex_list,
        'pokedex_seen'        : unparse_pokedex_list,
        'pocket_item_list'    : unparse_item_list,
        'money'               : lambda m: unparse_bcd(m, 3),
        'rival_name'          : lambda s: rby_us_string_encode(s, 11),
        'options'             : unparse_options,
        'badges'              : unparse_badges,
        'pc_item_list'        : unparse_item_list,
        'current_pc_box'      : unparse_current_pc_box,
        'casino_coins'        : lambda c: unparse_bcd(c, 2),
        'time_played'         : unparse_time_played,
        'team_pokemon'        : unparse_team_pokemon,
        'current_box_pokemon' : unparse_pc_box_pokemon,
        'pc_box_1'            : unparse_pc_box_pokemon,
        'pc_box_2'            : unparse_pc_box_pokemon,
        'pc_box_3'            : unparse_pc_box_pokemon,
        'pc_box_4'            : unparse_pc_box_pokemon,
        'pc_box_5'            : unparse_pc_box_pokemon,
        'pc_box_6'            : unparse_pc_box_pokemon,
        'pc_box_7'            : unparse_pc_box_pokemon,
        'pc_box_8'            : unparse_pc_box_pokemon,
        'pc_box_9'            : unparse_pc_box_pokemon,
        'pc_box_10'           : unparse_pc_box_pokemon,
        'pc_box_11'           : unparse_pc_box_pokemon,
        'pc_box_12'           : unparse_pc_box_pokemon,
    },
    byte_order = ">"
)

def parse_rby_us_save(data):
    return save_file_reader.unpack(data)

def read_rby_us_save(path):
    with open(path, 'rb') as savefile:
        data = savefile.read(32768)
    return parse_rby_us_save(data)

def unparse_rby_us_save(s):
    b = save_file_reader.pack(s)
    checksum = (255 - sum(b[0x2598:0x3523])) & 255
    s['checksum'] = checksum
    return save_file_reader.pack(s)

def write_rby_us_save(s, path):
    data = unparse_rby_us_save(s)
    with open(path, 'wb') as f:
        f.write(data)

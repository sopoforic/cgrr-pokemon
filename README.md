# cgrr-pokemon

This package supports reading and writing to files related to the Pokémon games.
At present, only the US versions of the Generation 1 games (Red/Blue/Yellow) are
supported.

# Usage

Clone the repo into a folder called `pokemon` for these examples.

```
git clone https://github.com/sopoforic/cgrr-pokemon.git pokemon
```

We'll use a save file from Pokemon Red Version called `red.sav` as an example.

```
>>> from pokemon import pokemon_rby as pr
>>> save = pr.read_rby_us_save('red.sav')
>>> diglett = save['current_box_pokemon']['pokemon'][0]
>>> diglett
{'attack_ev': 0,
 'catch_rate': 255,
 'current_hp': 15,
 'defense_ev': 0,
 'experience_points': 5832,
 'hp_ev': 0,
 'iv': {'attack': 6, 'defense': 0, 'special': 2, 'speed': 3},
 'level_in_box': 18,
 'move_1': <Move.Scratch: 10>,
 'move_1_pp': 35,
 'move_2': <Move.Growl: 45>,
 'move_2_pp': 40,
 'move_3': None,
 'move_3_pp': 0,
 'move_4': None,
 'move_4_pp': 0,
 'name': 'DIGLETT',
 'original_trainer_id': 21523,
 'ot_name': 'RED',
 'special_ev': 0,
 'species': <Pokemon.Diglett: 50>,
 'speed_ev': 0,
 'status_condition': [<Status.PARALYZED: 64>],
 'type_1': <PokemonType.GROUND: 4>,
 'type_2': <PokemonType.GROUND: 4>}
```
 
DIGLETT is paralyzed! We can help...
 
```
>>> diglett['status_condition'] = []
>>> pr.write_rby_us_save(save, 'edited.sav')
```

Other information is available (and editable), too. Some more examples:

```
>>> save['player_name']
'RED'
>>> save['badges']
[<Badge.BADGE_BOULDER: 1>, <Badge.BADGE_CASCADE: 2>, <Badge.BADGE_THUNDER: 4>]
>>> save['money']
40101
>>> save['options']
{'battle_effects': True,
 'battle_style': <BattleStyle.BATTLE_STYLE_SWITCH: 0>,
 'sound': <Sound.SOUND_MONO: 0>,
 'text_speed': <TextSpeed.TEXT_SPEED_FAST: 1>}
>>> save['pocket_item_list']
[{'count': 3, 'item': <Item.Potion: 20>},
 {'count': 2, 'item': <Item.Parlyz_Heal: 15>},
 {'count': 2, 'item': <Item.Moon_Stone: 10>},
 {'count': 1, 'item': <Item.Helix_Fossil: 42>},
 {'count': 8, 'item': <Item.Antidote: 11>},
 {'count': 1, 'item': <Item.SS_Ticket: 63>},
 {'count': 7, 'item': <Item.Poké_Ball: 4>},
 {'count': 1, 'item': <Item.Bicycle: 6>},
 {'count': 1, 'item': <Item.Old_Rod: 76>},
 {'count': 1, 'item': <Item.Ether: 80>},
 {'count': 1, 'item': <Item.Max_Potion: 17>},
 {'count': 1, 'item': <Item.Max_Ether: 81>},
 {'count': 1, 'item': <Item.TM24_Thunderbolt: 224>},
 {'count': 1, 'item': <Item.HM05_Flash: 200>},
 {'count': 1, 'item': <Item.TM42_Dream_Eater: 242>},
 {'count': 1, 'item': <Item.TM30_Teleport: 230>}]
>>> save['pokedex_seen']
{<Pokemon.Bulbasaur: 1>: False,
 <Pokemon.Ivysaur: 2>: False,
 <Pokemon.Venusaur: 3>: False,
 <Pokemon.Charmander: 4>: True,
 <Pokemon.Charmeleon: 5>: True,
 <Pokemon.Charizard: 6>: False,
 <Pokemon.Squirtle: 7>: True,
 <Pokemon.Wartortle: 8>: True,
 <Pokemon.Blastoise: 9>: False,
 <Pokemon.Caterpie: 10>: True,
...
}
>>> save['time_played']
datetime.timedelta(0, 41467)
>>> print(save['time_played'])
11:31:07
```

# Requirements

* cgrr from https://github.com/sopoforic/cgrr
 * pip install git+git://github.com/sopoforic/cgrr.git

# License

This module is available under the GPL v3 or later. See the file COPYING for details.
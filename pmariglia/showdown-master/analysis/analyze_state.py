import pandas as pd
from showdown.engine.objects import State
from showdown.engine.objects import StateMutator
from showdown.engine.select_best_move import get_payoff_matrix
from showdown.decide import pick_safest
from showdown.engine.select_best_move import get_all_state_instructions

import logging
from config import logger

logger.setLevel(logging.DEBUG)

first = {'self': {'active': {'id': 'greninja', 'level': 100, 'hp': 285, 'maxhp': 285, 'ability': 'battlebond', 'item': 'choicespecs', 'baseStats': {'hp': 72, 'attack': 95, 'defense': 67, 'special-attack': 103, 'special-defense': 71, 'speed': 122}, 'attack': 203, 'defense': 171, 'special-attack': 305, 'special-defense': 178, 'speed': 377, 'attack_boost': -1, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'surf', 'disabled': False, 'current_pp': 24}, {'id': 'darkpulse', 'disabled': False, 'current_pp': 24}, {'id': 'icebeam', 'disabled': False, 'current_pp': 16}, {'id': 'watershuriken', 'disabled': False, 'current_pp': 32}], 'types': ['water', 'dark'], 'canMegaEvo': False}, 'reserve': {'mawile': {'id': 'mawile', 'level': 100, 'hp': 261, 'maxhp': 261, 'ability': 'intimidate', 'item': 'mawilite', 'baseStats': {'hp': 50, 'attack': 85, 'defense': 85, 'special-attack': 55, 'special-defense': 55, 'speed': 50}, 'attack': 295, 'defense': 206, 'special-attack': 131, 'special-defense': 146, 'speed': 180, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'suckerpunch', 'disabled': False, 'current_pp': 8}, {'id': 'playrough', 'disabled': False, 'current_pp': 16}, {'id': 'thunderpunch', 'disabled': False, 'current_pp': 24}, {'id': 'firefang', 'disabled': False, 'current_pp': 24}], 'types': ['steel', 'fairy'], 'canMegaEvo': False}, 'tornadustherian': {'id': 'tornadustherian', 'level': 100, 'hp': 299, 'maxhp': 299, 'ability': 'regenerator', 'item': 'fightiniumz', 'baseStats': {'hp': 79, 'attack': 100, 'defense': 80, 'special-attack': 110, 'special-defense': 90, 'speed': 121}, 'attack': 212, 'defense': 197, 'special-attack': 319, 'special-defense': 216, 'speed': 375, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'taunt', 'disabled': False, 'current_pp': 32}, {'id': 'hurricane', 'disabled': False, 'current_pp': 16}, {'id': 'focusblast', 'disabled': False, 'current_pp': 8}, {'id': 'defog', 'disabled': False, 'current_pp': 24}], 'types': ['flying'], 'canMegaEvo': False}, 'ferrothorn': {'id': 'ferrothorn', 'level': 100, 'hp': 352, 'maxhp': 352, 'ability': 'ironbarbs', 'item': 'leftovers', 'baseStats': {'hp': 74, 'attack': 94, 'defense': 131, 'special-attack': 54, 'special-defense': 116, 'speed': 20}, 'attack': 224, 'defense': 299, 'special-attack': 144, 'special-defense': 364, 'speed': 68, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'spikes', 'disabled': False, 'current_pp': 32}, {'id': 'leechseed', 'disabled': False, 'current_pp': 16}, {'id': 'knockoff', 'disabled': False, 'current_pp': 32}, {'id': 'gyroball', 'disabled': False, 'current_pp': 8}], 'types': ['grass', 'steel'], 'canMegaEvo': False}, 'heatran': {'id': 'heatran', 'level': 100, 'hp': 385, 'maxhp': 385, 'ability': 'flashfire', 'item': 'leftovers', 'baseStats': {'hp': 91, 'attack': 90, 'defense': 106, 'special-attack': 130, 'special-defense': 106, 'speed': 77}, 'attack': 194, 'defense': 248, 'special-attack': 296, 'special-defense': 332, 'speed': 201, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'taunt', 'disabled': False, 'current_pp': 32}, {'id': 'magmastorm', 'disabled': False, 'current_pp': 8}, {'id': 'earthpower', 'disabled': False, 'current_pp': 16}, {'id': 'toxic', 'disabled': False, 'current_pp': 16}], 'types': ['fire', 'steel'], 'canMegaEvo': False}, 'garchomp': {'id': 'garchomp', 'level': 100, 'hp': 379, 'maxhp': 379, 'ability': 'roughskin', 'item': 'rockyhelmet', 'baseStats': {'hp': 108, 'attack': 130, 'defense': 95, 'special-attack': 80, 'special-defense': 85, 'speed': 102}, 'attack': 296, 'defense': 317, 'special-attack': 176, 'special-defense': 206, 'speed': 282, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'stealthrock', 'disabled': False, 'current_pp': 32}, {'id': 'earthquake', 'disabled': False, 'current_pp': 16}, {'id': 'toxic', 'disabled': False, 'current_pp': 16}, {'id': 'roar', 'disabled': False, 'current_pp': 32}], 'types': ['dragon', 'ground'], 'canMegaEvo': False}}, 'side_conditions': {'toxic_count': 0}, 'trapped': False}, 'opponent': {'active': {'id': 'landorustherian', 'level': 100, 'hp': 319.0, 'maxhp': 319, 'ability': 'intimidate', 'item': 'choicescarf', 'baseStats': {'hp': 89, 'attack': 145, 'defense': 90, 'special-attack': 105, 'special-defense': 80, 'speed': 91}, 'attack': 389, 'defense': 216, 'special-attack': 223.63636363636363, 'special-defense': 197, 'speed': 309.1, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'earthquake', 'disabled': False, 'current_pp': 16}, {'id': 'stoneedge', 'disabled': False, 'current_pp': 16},  {'id': 'uturn', 'disabled': False, 'current_pp': 32}, {'id': 'stealthrock', 'disabled': False, 'current_pp': 32}, {'id': 'defog', 'disabled': False, 'current_pp': 24}], 'types': ['ground', 'flying'], 'canMegaEvo': False}, 'reserve': {'magearna': {'id': 'magearna', 'level': 100, 'hp': 363.0, 'maxhp': 363, 'ability': 'soulheart', 'item': 'assaultvest', 'baseStats': {'hp': 80, 'attack': 95, 'defense': 115, 'special-attack': 130, 'special-defense': 115, 'speed': 65}, 'attack': 226, 'defense': 266, 'special-attack': 325.6, 'special-defense': 322, 'speed': 159.09090909090907, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'fleurcannon', 'disabled': False, 'current_pp': 8}, {'id': 'voltswitch', 'disabled': False, 'current_pp': 32}, {'id': 'thunderbolt', 'disabled': False, 'current_pp': 24}, {'id': 'icebeam', 'disabled': False, 'current_pp': 16}], 'types': ['steel', 'fairy'], 'canMegaEvo': False}, 'gliscor': {'id': 'gliscor', 'level': 100, 'hp': 352.0, 'maxhp': 352, 'ability': 'poisonheal', 'item': 'toxicorb', 'baseStats': {'hp': 75, 'attack': 95, 'defense': 125, 'special-attack': 45, 'special-defense': 75, 'speed': 95}, 'attack': 226, 'defense': 299, 'special-attack': 114.54545454545453, 'special-defense': 211, 'speed': 279.40000000000003, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'earthquake', 'disabled': False, 'current_pp': 16}, {'id': 'roost', 'disabled': False, 'current_pp': 16}, {'id': 'toxic', 'disabled': False, 'current_pp': 16}, {'id': 'stealthrock', 'disabled': False, 'current_pp': 32}], 'types': ['ground', 'flying'], 'canMegaEvo': False}, 'clefable': {'id': 'clefable', 'level': 100, 'hp': 394.0, 'maxhp': 394, 'ability': 'magicguard', 'item': 'leftovers', 'baseStats': {'hp': 95, 'attack': 70, 'defense': 73, 'special-attack': 95, 'special-defense': 90, 'speed': 60}, 'attack': 160.0, 'defense': 269.5, 'special-attack': 226, 'special-defense': 217, 'speed': 156, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'moonblast', 'disabled': False, 'current_pp': 24}, {'id': 'softboiled', 'disabled': False, 'current_pp': 16}, {'id': 'wish', 'disabled': False, 'current_pp': 16}, {'id': 'calmmind', 'disabled': False, 'current_pp': 32}], 'types': ['fairy'], 'canMegaEvo': False}, 'tapubulu': {'id': 'tapubulu', 'level': 100, 'hp': 343.0, 'maxhp': 343, 'ability': 'grassysurge', 'item': 'leftovers', 'baseStats': {'hp': 70, 'attack': 130, 'defense': 115, 'special-attack': 85, 'special-defense': 95, 'speed': 75}, 'attack': 296, 'defense': 268, 'special-attack': 206.0, 'special-defense': 289, 'speed': 186, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'hornleech', 'disabled': False, 'current_pp': 16}, {'id': 'superpower', 'disabled': False, 'current_pp': 8}, {'id': 'woodhammer', 'disabled': False, 'current_pp': 24}, {'id': 'stoneedge', 'disabled': False, 'current_pp': 8}], 'types': ['grass', 'fairy'], 'canMegaEvo': False}, 'gyarados': {'id': 'gyarados', 'level': 100, 'hp': 331.0, 'maxhp': 331, 'ability': 'moxie', 'item': 'flyiniumz', 'baseStats': {'hp': 95, 'attack': 125, 'defense': 79, 'special-attack': 60, 'special-defense': 100, 'speed': 81}, 'attack': 349, 'defense': 194, 'special-attack': 141.8181818181818, 'special-defense': 237, 'speed': 287.1, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'waterfall', 'disabled': False, 'current_pp': 24}, {'id': 'dragondance', 'disabled': False, 'current_pp': 32}, {'id': 'earthquake', 'disabled': False, 'current_pp': 16}, {'id': 'bounce', 'disabled': False, 'current_pp': 8}], 'types': ['water', 'flying'], 'canMegaEvo': False}}, 'side_conditions': {'toxic_count': 0}, 'trapped': False}, 'weather': None, 'field': None, 'trickroom': False, 'forceSwitch': False, 'wait': False}
# second = {'self': {'active': {'id': 'audino', 'level': 81, 'hp': 299, 'maxhp': 299, 'ability': 'regenerator', 'baseStats': {'hp': 103, 'attack': 60, 'defense': 86, 'special-attack': 60, 'special-defense': 86, 'speed': 50}, 'attack': 144, 'defense': 186, 'special-attack': 144, 'special-defense': 186, 'speed': 128, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'healbell', 'disabled': False, 'current_pp': 8}, {'id': 'protect', 'disabled': False, 'current_pp': 16}, {'id': 'wish', 'disabled': False, 'current_pp': 16}, {'id': 'hypervoice', 'disabled': False, 'current_pp': 16}], 'types': ['normal']}, 'reserve': {'heatran': {'id': 'heatran', 'level': 75, 'hp': 0, 'maxhp': 260, 'ability': 'flashfire', 'baseStats': {'hp': 91, 'attack': 90, 'defense': 106, 'special-attack': 130, 'special-defense': 106, 'speed': 77}, 'attack': 179, 'defense': 203, 'special-attack': 239, 'special-defense': 203, 'speed': 159, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'roar', 'disabled': False, 'current_pp': 32}, {'id': 'stealthrock', 'disabled': False, 'current_pp': 32}, {'id': 'earthpower', 'disabled': False, 'current_pp': 16}, {'id': 'lavaplume', 'disabled': False, 'current_pp': 24}], 'types': ['fire', 'steel']}, 'omastar': {'id': 'omastar', 'level': 81, 'hp': 246, 'maxhp': 246, 'ability': 'swiftswim', 'baseStats': {'hp': 70, 'attack': 60, 'defense': 125, 'special-attack': 115, 'special-defense': 70, 'speed': 55}, 'attack': 144, 'defense': 249, 'special-attack': 233, 'special-defense': 160, 'speed': 136, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'scald', 'disabled': False, 'current_pp': 24}, {'id': 'shellsmash', 'disabled': False, 'current_pp': 24}, {'id': 'earthpower', 'disabled': False, 'current_pp': 16}, {'id': 'icebeam', 'disabled': False, 'current_pp': 16}], 'types': ['rock', 'water']}, 'alomomola': {'id': 'alomomola', 'level': 77, 'hp': 381, 'maxhp': 381, 'ability': 'regenerator', 'baseStats': {'hp': 165, 'attack': 75, 'defense': 80, 'special-attack': 40, 'special-defense': 45, 'speed': 65}, 'attack': 160, 'defense': 168, 'special-attack': 106, 'special-defense': 114, 'speed': 145, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'knockoff', 'disabled': False, 'current_pp': 32}, {'id': 'wish', 'disabled': False, 'current_pp': 16}, {'id': 'toxic', 'disabled': False, 'current_pp': 16}, {'id': 'scald', 'disabled': False, 'current_pp': 24}], 'types': ['water']}, 'hawlucha': {'id': 'hawlucha', 'level': 75, 'hp': 105, 'maxhp': 241, 'ability': 'unburden', 'baseStats': {'hp': 78, 'attack': 92, 'defense': 75, 'special-attack': 74, 'special-defense': 63, 'speed': 118}, 'attack': 182, 'defense': 156, 'special-attack': 155, 'special-defense': 138, 'speed': 221, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'swordsdance', 'disabled': False, 'current_pp': 32}, {'id': 'stoneedge', 'disabled': False, 'current_pp': 8}, {'id': 'roost', 'disabled': False, 'current_pp': 16}, {'id': 'highjumpkick', 'disabled': False, 'current_pp': 16}], 'types': ['fighting', 'flying']}, 'swalot': {'id': 'swalot', 'level': 83, 'hp': 129, 'maxhp': 302, 'ability': 'stickyhold', 'baseStats': {'hp': 100, 'attack': 73, 'defense': 83, 'special-attack': 73, 'special-defense': 83, 'speed': 55}, 'attack': 169, 'defense': 185, 'special-attack': 169, 'special-defense': 185, 'speed': 139, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'icebeam', 'disabled': False, 'current_pp': 16}, {'id': 'encore', 'disabled': False, 'current_pp': 8}, {'id': 'yawn', 'disabled': False, 'current_pp': 16}, {'id': 'sludgebomb', 'disabled': False, 'current_pp': 16}], 'types': ['poison']}}, 'side_conditions': {'stealthrock': 0, 'spikes': 0}, 'trapped': False}, 'opponent': {'active': {'id': 'zekrom', 'level': 73, 'hp': 202.16, 'maxhp': 266, 'ability': 'teravolt', 'baseStats': {'hp': 100, 'attack': 150, 'defense': 120, 'special-attack': 120, 'special-defense': 100, 'speed': 90}, 'attack': 261, 'defense': 218, 'special-attack': 218, 'special-defense': 188, 'speed': 174, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'boltstrike', 'disabled': False, 'current_pp': 8}, {'id': 'substitute', 'disabled': False, 'current_pp': 16}], 'types': ['dragon', 'electric']}, 'reserve': {'rotomfrost': {'id': 'rotomfrost', 'level': 83, 'hp': 199.29000000000002, 'maxhp': 219, 'ability': 'levitate', 'baseStats': {'hp': 50, 'attack': 65, 'defense': 107, 'special-attack': 105, 'special-defense': 107, 'speed': 86}, 'attack': 156, 'defense': 225, 'special-attack': 222, 'special-defense': 225, 'speed': 190, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'voltswitch', 'disabled': False, 'current_pp': 32}], 'types': ['electric', 'ice']}, 'bibarel': {'id': 'bibarel', 'level': 83, 'hp': 0, 'maxhp': 267, 'ability': None, 'baseStats': {'hp': 79, 'attack': 85, 'defense': 60, 'special-attack': 55, 'special-defense': 60, 'speed': 71}, 'attack': 189, 'defense': 147, 'special-attack': 139, 'special-defense': 147, 'speed': 166, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'return', 'disabled': False, 'current_pp': 32}], 'types': ['normal', 'water']}, 'passimian': {'id': 'passimian', 'level': 83, 'hp': 193.28, 'maxhp': 302, 'ability': None, 'baseStats': {'hp': 100, 'attack': 120, 'defense': 90, 'special-attack': 40, 'special-defense': 60, 'speed': 80}, 'attack': 247, 'defense': 197, 'special-attack': 114, 'special-defense': 147, 'speed': 180, 'attack_boost': 0, 'defense_boost': 0, 'special_attack_boost': 0, 'special_defense_boost': 0, 'speed_boost': 0, 'status': None, 'volatileStatus': [], 'moves': [{'id': 'uturn', 'disabled': False, 'current_pp': 32}], 'types': ['fighting']}}, 'side_conditions': {'stealthrock': 0, 'spikes': 0}, 'trapped': False}, 'weather': None, 'field': None, 'forceSwitch': False, 'wait': False}

state = State.from_dict(first)
mutator = StateMutator(state)

instruction = get_all_state_instructions(mutator, 'flareblitz', 'nastyplot')

scores = get_payoff_matrix(mutator, depth=2)

df = pd.Series(scores).unstack()
averages = df.mean(axis=1)

safest = pick_safest(scores)

pass
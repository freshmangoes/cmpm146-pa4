#!/usr/bin/env python
#

"""
// The do_turn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist.
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect

logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# Where the magic logic happens
def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # Checks
    largest_fleet_check = Check(have_largest_fleet)
    enemy_planet_check = Check(if_enemy_planet_available)
    neutral_planet_check = Check(if_neutral_planet_available)

    # Spread to weakest neutral
    spread_orig = Sequence(name='Spread Original')
    spread_orig_action = Action(spread_to_weakest_neutral_planet)
    spread_orig.child_nodes = [spread_orig_action]

    # Spread vanilla
    spread_vanilla_plan = Sequence(name='Spread Vanilla')
    spread_vanilla_action = Action(spread_vanilla)
    spread_vanilla_plan.child_nodes = [spread_vanilla_action]

    # Spread to high growth rate
    spread_hgr_plan = Sequence(name='Spread High Growth Rate')
    spread_hgr_action = Action(spread_to_highest_growth_rate)
    spread_hgr_plan.child_nodes = [spread_hgr_action]

    # Spread default
    spread_def_plan = Sequence(name='Spread Default')
    spread_def_action = Action(spread_default)
    spread_def_plan.child_nodes = [spread_def_action]

    # Attack Vanilla
    attack_plan = Sequence(name='Attack Vanilla')
    attack_action = Action(attack_vanilla)
    attack_plan.child_nodes = [attack_action]

    # Attack high growth rate
    attack_hgr_plan = Sequence(name='Attack High Growth Rate')
    attack_hgr_action = Action(attack_high_growth)
    attack_hgr_plan.child_nodes = [attack_hgr_action]

    # Attack-full
    attack_full = Sequence(name='Attack Full Sequence')
    attack_full.child_nodes = [largest_fleet_check, enemy_planet_check, attack_plan, attack_hgr_plan]

    # Spread-full
    spread_full = Sequence(name='Spread Full Sequence')
    spread_full.child_nodes = [neutral_planet_check, spread_def_plan, spread_hgr_plan, spread_vanilla_plan, spread_orig]

    root.child_nodes = [attack_full, spread_full, attack_action.copy(),
                        attack_hgr_action.copy(), spread_vanilla_action.copy(),
                        spread_orig_action.copy(), spread_def_action.copy(),
                        spread_hgr_action.copy()]
    logging.info('\n' + root.tree_to_string())
    return root


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                behavior_tree.execute(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")

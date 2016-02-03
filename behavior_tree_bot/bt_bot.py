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
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
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

    # Spread to closest
    spread_plan = Sequence(name='Spread2')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_closest_neutral)
    spread_plan.child_nodes = [neutral_planet_check, spread_action]

    # Attack 2
    attack_plan = Sequence(name='Attack2')
    largest_fleet_check = Check(have_largest_fleet)
    enemy_planet_check = Check(if_enemy_planet_available)
    attack_action = Action(attack_improved)
    attack_plan.child_nodes = [enemy_planet_check, largest_fleet_check, attack_action]

    # root.child_nodes = [spread_plan, attack_plan, attack_action.copy(), spread_action.copy()]
    root.child_nodes = [attack_plan, spread_plan, attack_action.copy(), spread_action.copy()]
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

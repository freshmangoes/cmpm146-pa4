import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import heapq

# logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)


def attack_improved(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:

        my_planet = next(my_planets)
        target_planet = next(target_planets)

        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return
    pass


def spread_to_closest_neutral(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    neutral_planets = [planet for planet in state.neutral_planets()
                       if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)
    target_planets = iter(neutral_planets)
    distance = 200
    # currdistance = 13

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        required_ships = target_planet.num_ships + 1
        while True:
            while my_planet is not None and target_planet is not None:
                currdistance = state.distance(my_planet.ID, target_planet.ID)
                if distance >= currdistance and my_planet.num_ships > required_ships:
                    distance = currdistance
                    curr_myplanet = my_planet
                    curr_targetplanet = target_planet
                    my_planet = next(my_planets)
                    target_planet = next(my_planets)
                else:
                    my_planet = next(my_planets)
                    target_planet = next(target_planets)
                # my_planet = next(my_planets)
                # target_planet = next(target_planets)

            issue_order(state, curr_myplanet.ID, curr_targetplanet.ID, required_ships)
            """if my_planet.num_ships > target_planet.num_ships:
                required_ships = target_planet.num_ships + 1
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)"""
    except StopIteration:
        return


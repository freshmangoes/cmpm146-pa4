import sys

sys.path.insert(0, '../')
from planet_wars import issue_order
import heapq


# Vanilla attack
def attack_vanilla(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    enemy_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID
                                for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)
    target_planets = iter(enemy_planets)
    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                             state.distance(my_planet.ID, target_planet.ID) \
                             * target_planet.growth_rate + 1
            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return
    pass


# Prioritizes higher growth rate planets
def attack_high_growth(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    enemy_planets = [planet for planet in state.enemy_planets()
                    if not any(fleet.destination_planet == planet.ID
                    for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.growth_rate)
    enemy_planets.reverse()
    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = state.distance(my_planet.ID, target_planet.ID) * \
                             target_planet.growth_rate + target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return


def spread_to_weakest_neutral_planet(state):
    if len(state.my_fleets()) >= 1:
        return False
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet or not weakest_planet:
        return False
    else:
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


# Prioritizes highest growth rate planets
def spread_to_highest_growth_rate(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    neutral_planets = [planet for planet in state.neutral_planets()
                       if not any(fleet.destination_planet == planet.ID
                       for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.growth_rate)
    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        required_ships = target_planet.num_ships + 1
        while True:
            if my_planet.num_ships > target_planet.num_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return


def spread_default(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    neutral_planets = [planet for planet in state.neutral_planets()
                       if not any(fleet.destination_planet == planet.ID
                                  for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)
    target_planets = iter(neutral_planets)
    distance = 200

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        required_ships = target_planet.num_ships + 1
        while True:
            while my_planet is not None and target_planet is not None:
                curr_dist = state.distance(my_planet.ID, target_planet.ID)
                if distance >= curr_dist and my_planet.num_ships > required_ships:
                    distance = curr_dist
                    tmp_my_planet = my_planet
                    tmp_target_planet = target_planet
                    required_ships = tmp_target_planet.num_ships + 1
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            issue_order(state, tmp_my_planet.ID, tmp_target_planet.ID, required_ships)
    except StopIteration:
        return


def spread_vanilla(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return





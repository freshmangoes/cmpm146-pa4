import sys

sys.path.insert(0, '../')
from planet_wars import issue_order
import heapq


def attack_improved(state):
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


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    # For any planet that doesn't have a fleet in flight to it
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

            # if my_planet.num_ships > target_planet.num_ships:
            #     required_ships = target_planet.num_ships + 1
            #     issue_order(state, my_planet.ID, target_planet.ID, required_ships)
            #     my_planet = next(my_planets)
            #     target_planet = next(target_planets)
            # else:
            #     my_planet = next(my_planets)
    except StopIteration:
        return

import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)

    dist_to_weakest = state.distance(strongest_planet.ID, weakest_planet.ID)

    required_ships = weakest_planet.num_ships + dist_to_weakest * weakest_planet.growth_rate + 1

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        # return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)

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


def spread_to_closest_neutral(state):

    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    neutral_planets = [planet for planet in state.neutral_planets()
                       if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)
    # target_planets = iter(sorted(neutral_planets, key = lambda p: p.num_ships))
    target_planets = iter(neutral_planets)
    # strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    # closest_planet = min(state.neutral_planets(), key=lambda c: state.distance(strongest_planet.ID, c.ID))

    try:
        # my_planet = max(my_planets, key=lambda p: p.num_ships, default=None)
        my_planet = next(my_planets)
        target_planet = next(target_planets)

        while True:
            if my_planet.num_ships > target_planet.num_ships:
                required_ships = target_planet.num_ships + 1
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return



    # if len(state.my_fleets()) >= 1:
    #     return False
    # strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    # closest_planet = min(state.neutral_planets(), key=lambda c: state.distance(strongest_planet.ID, c.ID))
    #
    # required_ships = closest_planet.num_ships + 1
    #
    # if not strongest_planet or not closest_planet:
    #     return False
    # else:
    #     return issue_order(state, strongest_planet.ID, closest_planet.ID, required_ships)
    pass


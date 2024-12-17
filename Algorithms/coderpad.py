### 2048-bonacci
from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

Di = Direction


class The2048Bonacci():

    def __init__(self, game_area):
        self.game_area = game_area
        self.width = len(self.game_area[0])
        self.height = len(self.game_area)
        self.fibonacci = [1, 1]

    def _init_fibonacci(self):
        max_val = max(
            max(fib_val for fib_val in line)
            for line in self.game_area
        )
        while self.fibonacci[-1] < max_val:
            self.fibonacci.append(self.fibonacci[-1] + self.fibonacci[-2])
        if self.fibonacci[-1] > max_val:
            raise Exception(
                f"This value is not in the Fibonacci sequence: {max_val}"
            )
        self.fibonacci.append(self.fibonacci[-1] + self.fibonacci[-2])

    def get_tile(self, x, y):
        return self.game_area[y][x]

    def set_tile(self, x, y, fib_value):
        self.game_area[y][x] = fib_value

    def _iterate_on_line_coords(self, pushing_direction):
        if pushing_direction in (Di.DOWN, Di.UP):
            coord_ys = list(range(self.height))
            if pushing_direction == Di.UP:
                coord_ys = coord_ys[::-1]
            for coord_x in range(self.width):
                line_coords = [
                    (coord_x, coord_y) for coord_y in coord_ys
                ]
                yield line_coords
        else:
            coord_xs = list(range(self.width))
            if pushing_direction == Di.LEFT:
                coord_xs = coord_xs[::-1]
            for coord_y in range(self.height):
                line_coords = [
                    (coord_x, coord_y) for coord_x in coord_xs
                ]
                yield line_coords

    def _do_fibonacci_fusing(self, fibo_vals):
        nb_total_vals = len(fibo_vals)
        fibo_vals = list(filter(None, fibo_vals))
        processed_fibo_vals = []

        if fibo_vals:
            prev_val = fibo_vals[-1]
            for cur_val in fibo_vals[-2::-1]:
                if prev_val != 0:
                    if prev_val + cur_val in self.fibonacci:
                        prev_val = prev_val + cur_val
                        cur_val = 0
                    processed_fibo_vals.insert(0, prev_val)
                prev_val = cur_val
            if prev_val != 0:
                processed_fibo_vals.insert(0, prev_val)

        missing_zeros = [0] * (nb_total_vals - len(processed_fibo_vals))
        return  missing_zeros + processed_fibo_vals

    def process_push(self, pushing_direction):
        self._init_fibonacci()
        for line_coords in self._iterate_on_line_coords(pushing_direction):
            fibo_vals = [
                self.get_tile(*coord) for coord in line_coords
            ]
            fused_fibo_vals = self._do_fibonacci_fusing(fibo_vals)
            for (x, y), fibo_val in zip(line_coords, fused_fibo_vals):
                self.set_tile(x, y, fibo_val)

    def get_description(self):
        str_lines = []
        for line in self.game_area:
            str_line = " ".join(
                [
                    f"{fib_val:2d}" for fib_val in line
                ]
            )
            str_lines.append(str_line)
        return "\n".join(str_lines)


### All these types of plates
class PlateIndexer():

    def __init__(self, plates):
        self.stackstart = {}
        for idx, plate in enumerate(plates):
            if plate not in self.stackstart:
                self.stackstart[plate] = idx
        self.stacksize = len(plates)

    def get_insertion_details(self, plate1, plate2=None):
        """
        Returns a tuple.
         - The first element is an integer: the index where to add the plates.
         - A boolean, telling if plate_1 and plate_2
           must be reversed before insertion.
        """
        if plate2 is None:  # Manage single-plate insertion
            self.stacksize += 1
            insertion_index = self.stackstart[plate1]
            for plate_type in self.stackstart:
                if self.stackstart[plate_type] > insertion_index:
                    self.stackstart[plate_type] += 1
            return insertion_index, False

        self.stacksize += 2
        should_invert = self.stackstart[plate1] > self.stackstart[plate2]
        # Find which plate is in the highest group between plate1 and plate2
        highest_group = max(plate1, plate2, key=lambda x:self.stackstart[x])

        insertion_index = self.stackstart[highest_group]
        # Move every group above the insertion point by +2
        for plate_type in self.stackstart:
            if self.stackstart[plate_type] > insertion_index:
                self.stackstart[plate_type] += 2

        # If we have 2 different plates, the bigger group is moved by +1
        if plate1 != plate2:
            self.stackstart[highest_group] += 1

        return insertion_index, should_invert

    def reconstruct_plate_pile(self):
        curr_idx = 0
        curr_plate = None
        result = []
        for plate, idx in self.stackstart.items():
            result.extend([curr_plate] * (idx - curr_idx))
            curr_plate = plate
            curr_idx = idx
        result.extend([curr_plate] * (self.stacksize - curr_idx))
        return result


### Inventory optimization
    
CUT_TYPE_X = 0
CUT_TYPE_Y = 1


class LootItem():

    def __init__(self, name, value, width, height):
        self.name = name
        self.value = value
        self.width = width
        self.height = height


class Treasure():

    def __init__(self, loot_items):
        self.loot_items = loot_items

    def get_best_loot(self, width, height):
        sized_loot_items = [
            loot_item for loot_item in self.loot_items
            if loot_item.width == width and loot_item.height == height
        ]
        if not sized_loot_items:
            return None
        return max(sized_loot_items, key=lambda l_ob:l_ob.value)


class RPGInventory():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.occupied_squares = [
            [False] * self.width for y in range(self.height)
        ]
        self.loot_items = []
        self.total_value = 0

    def add_loot_item(self, loot_item, x, y):
        for x_cursor in range(x, x + loot_item.width):
            for y_cursor in range(y, y + loot_item.height):
                if self.occupied_squares[y_cursor][x_cursor]:
                    raise Exception(
                        "Trying to add a loot item in an occupied square"
                    )
                self.occupied_squares[y_cursor][x_cursor] = True
        self.loot_items.append(
            (loot_item, x, y)
        )
        self.total_value += loot_item.value

    def add_rpg_inventory(self, rpg_inventory, rpg_x, rpg_y):
        for loot_item, l_ob_x, l_ob_y in rpg_inventory.loot_items:
            self.add_loot_item(
                loot_item,
                rpg_x + l_ob_x,
                rpg_y + l_ob_y,
            )

    def get_str_description(self):
        lines = []
        for loot_item, l_ob_x, l_ob_y in self.loot_items:
            lines.append(f" - {loot_item.name} at ({l_ob_x}, {l_ob_y})")
        lines.append(f"Total value : {self.total_value}")
        return "\n".join(lines)


def iter_on_rect_cuttings(width, height):
    for x in range(1, width // 2 + 1):
        yield [
            (x, height), (width - x, height), CUT_TYPE_X
        ]
    for y in range(1, height // 2 + 1):
        yield [
            (width, y), (width, height - y), CUT_TYPE_Y
        ]


def get_next_rpg_inventory(width, height, best_rpg_inventories, treasure):
    candidates = []
    for dimension_1, dimension_2, cut_type in iter_on_rect_cuttings(width, height):
        rpg_inv_1 = best_rpg_inventories[dimension_1]
        rpg_inv_2 = best_rpg_inventories[dimension_2]
        candidates.append(
            (
                rpg_inv_1.total_value + rpg_inv_2.total_value,
                (rpg_inv_1, rpg_inv_2, cut_type),
            )
        )

    loot_item_big = treasure.get_best_loot(width, height)
    if loot_item_big is not None:
        rpg_inv_big = RPGInventory(width, height)
        rpg_inv_big.add_loot_item(loot_item_big, 0, 0)
        candidates.append(
            (
                rpg_inv_big.total_value,
                (rpg_inv_big, ),
            )
        )
    if not candidates:
        return RPGInventory(width, height)

    best_candidate = max(candidates, key=lambda c:c[0])
    best_next_rpg_inv_info = best_candidate[1]
    if len(best_next_rpg_inv_info) == 1:
        return best_next_rpg_inv_info[0]
    else:
        best_next_rpg_inv = RPGInventory(width, height)
        rpg_inv_1, rpg_inv_2, cut_type = best_next_rpg_inv_info
        best_next_rpg_inv.add_rpg_inventory(rpg_inv_1, 0, 0)
        if cut_type == CUT_TYPE_X:
            offset_x = rpg_inv_1.width
            offset_y = 0
        else:
            offset_x = 0
            offset_y = rpg_inv_1.height
        best_next_rpg_inv.add_rpg_inventory(rpg_inv_2, offset_x, offset_y)
        return best_next_rpg_inv


def get_best_rpg_inventory(width, height, treasure):
    best_rpg_inventories = {}
    for cur_w in range(1, width + 1):
        for cur_h in range(1, height + 1):
            best_next_rpg_inventory = get_next_rpg_inventory(
                cur_w,
                cur_h,
                best_rpg_inventories,
                treasure,
            )
            best_rpg_inventories[(cur_w, cur_h)] = best_next_rpg_inventory
    return best_rpg_inventories[(width, height)]


### The cat, the blind grandfather and the pile of books
books = '''Harry Potter and the Prisoner of Azkaban
Gone With the Wind
Frankenstein or The Modern Prometheus
Band of Brothers
The Caves of Steel
The Grapes of Wrath
Ubik'''.splitlines()

for book_index in reversed(range(1, len(books))):
    if books[book_index-1].lower() > books[book_index].lower():
        print(book_index + 1)
        break
else:
    print(0)
    

### Unpaint road lines   
def analyze_paint_logs(coords):
    painted = [False for _ in range(max(coords) + 1)] # Add 1 to guarantee unpainted last cell

    # Naive painting algorithm
    for coord_i in range(0, len(coords), 2):
        start = coords[coord_i]
        end = coords[coord_i + 1]
        for paint_idx in range(start, end):
            painted[paint_idx] = True

    previous_painted = False
    interval_start = None
    result = []
    for i in range(len(painted)):
        if painted[i] and not previous_painted:
            # Found new interval start
            interval_start = i
        if not painted[i] and previous_painted:
            # Found current interval end
            result.extend([interval_start, i])

        # Remember previous cell state
        previous_painted = painted[i]

    return tuple(result)


### 
from enum import Enum

class TilePosError(LookupError): pass

class Direction(Enum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7

ALL_DIRS = [Direction(d) for d in range(8)]
CARDINAL_DIRS = ALL_DIRS[::2]
DIAGONAL_DIRS = ALL_DIRS[1::2]


class Tile():

    def __init__(self, char_data=" "):
        self.char_data = char_data
        self.adjacencies = [None] * 8

    def get_adjacent(self, direction):
        """
        This function works with numbers, from 0 to 7,
        and also with the Enum Direction.
        """
        adj_tile = self.adjacencies[
            Direction(direction).value
        ]
        if adj_tile is None:
            raise TilePosError()
        return adj_tile

    def set_adjacencies(self, board_owner, x, y):
        direction_offset_coords = (
            (Direction.UP, 0, -1),
            (Direction.UP_RIGHT, 1, -1),
            (Direction.RIGHT, 1, 0),
            (Direction.DOWN_RIGHT, 1, 1),
            (Direction.DOWN, 0, 1),
            (Direction.DOWN_LEFT, -1, 1),
            (Direction.LEFT, -1, 0),
            (Direction.UP_LEFT, -1, -1),
        )
        for direc, offset_x, offset_y in direction_offset_coords:
            try:
                adj_tile = board_owner.get_tile(x + offset_x, y + offset_y)
            except TilePosError:
                pass
            else:
                self.adjacencies[direc.value] = adj_tile


class Board():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._tiles = [
            [Tile() for _ in range(self.width)]
            for __ in range(self.height)
        ]
        for y in range(self.height):
            for x in range(self.width):
                tile = self._tiles[y][x]
                tile.set_adjacencies(self, x, y)

    def get_tile(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise TilePosError()
        return  self._tiles[y][x]

    def render(self):
        str_rendered_board = []
        for y in range(self.height):
            line = "".join(
                [tile.char_data for tile in self._tiles[y]]
            )
            str_rendered_board.append(line)
        return "\n".join(str_rendered_board)

    def __getitem__(self, key):
        """
        Overriding the operator square brackets [].
        This is not always possible in every language,
        but we have the fortune to be able to do it in python.
        """
        x, y = key
        return self.get_tile(x, y)    
    
    
    
    
import random
import math

PLANET_FOOD = 0
PLANET_METAL = 1

class Planet():

    def __init__(self, p_type, name, coordinates):
        self.p_type = p_type
        self.name = name
        self.coordinates = coordinates
        self.distances = {}
        self.trade_routed_planets = []

    def calculate_distances(self, universe):
        s_x, s_y, s_z = self.coordinates
        for other_planet in universe.planets:
            if other_planet.p_type != self.p_type:
                o_x, o_y, o_z = other_planet.coordinates
                square_dist = (o_x - s_x)**2 + (o_y - s_y)**2 + (o_z - s_z)**2
                dist = math.sqrt(square_dist)
                self.distances[other_planet] = dist

    def is_linked(self):
        return bool(self.trade_routed_planets)


class Universe():

    def __init__(self, planets):
        self.planets = planets
        for planet in self.planets:
            planet.calculate_distances(self)
        self.planets_food = [
            planet
            for planet in self.planets
            if planet.p_type == PLANET_FOOD
        ]

    def establish_trade_route(self, planet_1, planet_2):
        if planet_1.p_type ==  planet_2.p_type:
            raise Exception(
                "Trade route between two planets of same type is useless."
            )
        if (
            planet_2 in planet_1.trade_routed_planets
            or planet_1 in planet_2.trade_routed_planets
        ):
            raise Exception(
                "There is already a trade route between these two planets."
            )
        planet_1.trade_routed_planets.append(planet_2)
        planet_2.trade_routed_planets.append(planet_1)

    def remove_trade_route(self, planet_1, planet_2):
        if (
            planet_2 not in planet_1.trade_routed_planets
            or planet_1 not in planet_2.trade_routed_planets
        ):
            raise Exception(
                "Trying to remove a trade route that do not exist."
            )
        planet_1.trade_routed_planets.remove(planet_2)
        planet_2.trade_routed_planets.remove(planet_1)

    def solve_greedy_from_nothing(self):
        # List of tuples : (planet_food, planet_metal, distance)
        all_distances_food_metal = []
        for planet_food in self.planets_food:
            for planet_metal, dist in planet_food.distances.items():
                all_distances_food_metal.append(
                    (planet_food, planet_metal, dist)
                )
        all_distances_food_metal.sort(key=lambda p_p_d:p_p_d[2])

        for planet_food, planet_metal, dist in all_distances_food_metal:
            if not planet_food.is_linked() or not planet_metal.is_linked():
                self.establish_trade_route(planet_food, planet_metal)

    def do_local_heuristic(self, p_food_1, p_metal_1, p_food_2, p_metal_2):
        """
        A link is supposed to exist between p_food_1 & p_metal_1,
        and between p_food_2 & p_metal_2. (This function does not check it)
        The function removes any other links between the 4 planets,
        as they are useless.

        Then the function tests if the solution is better with
        a link between p_food_1 & p_metal_2, and also p_food_2 & p_metal_1.
        If yes, the function removes the previous links and adds the new ones.

        The function returns True if any trade route has been added or removed.
        """
        if p_food_1 == p_food_2 or p_metal_1 == p_metal_2:
            # There are not really 4 planets.
            # There are 3, with one of them in two parameters.
            # We can't do anything. Good bye !
            return False

        changed_something = False
        if p_metal_2 in p_food_1.trade_routed_planets:
            print(
                "debug: Removing trade route between",
                f"{p_food_1.name} and {p_metal_2.name}",
            )
            self.remove_trade_route(p_food_1, p_metal_2)
            changed_something = True
        if p_metal_1 in p_food_2.trade_routed_planets:
            print(
                "debug: Removing trade route between",
                f"{p_food_2.name} and {p_metal_1.name}",
            )
            self.remove_trade_route(p_food_2, p_metal_1)
            changed_something = True

        current_dist = p_food_1.distances[p_metal_1] + p_food_2.distances[p_metal_2]
        possible_dist = p_food_1.distances[p_metal_2] + p_food_2.distances[p_metal_1]
        if possible_dist < current_dist:
            print(
                "debug. Swapping routes between",
                f"{p_food_1.name} - {p_metal_1.name},",
                f"{p_food_2.name} - {p_metal_2.name}",
            )
            self.remove_trade_route(p_food_1, p_metal_1)
            self.remove_trade_route(p_food_2, p_metal_2)
            self.establish_trade_route(p_food_1, p_metal_2)
            self.establish_trade_route(p_food_2, p_metal_1)
            changed_something = True

        return changed_something

    def do_one_global_heuristic(self):
        for index_p_food_1, p_food_1 in enumerate(self.planets_food):
            for p_food_2 in self.planets_food[index_p_food_1+1:]:
                for p_metal_1 in p_food_1.trade_routed_planets:
                    for p_metal_2 in p_food_2.trade_routed_planets:
                        if self.do_local_heuristic(
                            p_food_1, p_metal_1, p_food_2, p_metal_2
                        ):
                            return True
        return False

    def do_global_random_heuristic(
        self,
        nb_consecutive_tries_max=10,
        nb_modif_max=100
    ):
        nb_consecutive_tries = 0
        nb_modif = 0
        while (
            nb_consecutive_tries < nb_consecutive_tries_max
            and nb_modif < nb_modif_max
        ):
            p_food_1, p_food_2 = random.sample(self.planets_food, 2)
            p_metal_1 = random.choice(p_food_1.trade_routed_planets)
            p_metal_2 = random.choice(p_food_2.trade_routed_planets)

            if self.do_local_heuristic(
                p_food_1, p_metal_1, p_food_2, p_metal_2
            ):
                nb_consecutive_tries = 0
                nb_modif += 1
            else:
                nb_consecutive_tries += 1
        return nb_modif

    def do_global_systematic_heuristic(self, nb_modif_max=100):
        for _ in range(nb_modif_max):
            if self.do_one_global_heuristic() == False:
                print("debug. It looks like we optimized everything. Bye !")
                break

    def check_solution(self):
        for planet in self.planets:
            if not planet.is_linked():
                raise Exception(f"The planet {planet.name} is not linked.")

    def print_solution(self):
        sum_dist = 0
        for planet_food in self.planets_food:
            for planet_metal in planet_food.trade_routed_planets:
                dist = planet_food.distances[planet_metal]
                print(f" - {planet_food.name}-{planet_metal.name} : {dist}")
                sum_dist += dist
        print("Total distance:", sum_dist)

def generate_random_planets(p_type, planet_qty):
    planet_prefix = "F" if p_type == PLANET_FOOD else "M"
    return [
        Planet(
            p_type,
            f"{planet_prefix}{index:03}",
            (
                random.randint(0, 5000),
                random.randint(0, 5000),
                random.randint(0, 5000)
            ),
        )
        for index in range(planet_qty)
    ]

def main():
    nominal_planets = (
        Planet(PLANET_FOOD, "F001", (50, 50, 50)),
        Planet(PLANET_FOOD, "F002", (50, 150, 50)),
        Planet(PLANET_METAL, "M003", (50, 50, 90)),
        Planet(PLANET_FOOD, "F101", (1000, 0, 0)),
        Planet(PLANET_FOOD, "F102", (1000, 10, 0)),
        Planet(PLANET_METAL, "M103", (1000, 0, 70)),
        Planet(PLANET_METAL, "M104", (1000, 10, 70)),
        Planet(PLANET_FOOD, "F201", (0, 0, 2000)),
        Planet(PLANET_FOOD, "F202", (30, -100, 2000)),
        Planet(PLANET_METAL, "M203", (30, 0, 2000)),
        Planet(PLANET_METAL, "M204", (0, 100, 2000)),
    )
    random_planets_food = generate_random_planets(PLANET_FOOD, 50)
    random_planets_metal =  generate_random_planets(PLANET_METAL, 50)
    # Replace this line with `planets = nominal_planets`
    # if you want to do a simple and reproductible test.
    planets = random_planets_food + random_planets_metal

    universe = Universe(planets)
    universe.solve_greedy_from_nothing()
    universe.check_solution()
    universe.print_solution()
    print("-" * 10)
    print("Doing random heuristic.")
    # Tests show that random heuristics could be more efficient.
    # Anyway, we keep it here. It may be useful with bigger universes.
    nb_modif_made = universe.do_global_random_heuristic()
    print("-" * 10)
    print("Doing systematic heuristic.")
    if nb_modif_made < 100:
        universe.do_global_systematic_heuristic(100 - nb_modif_made)
    print("-" * 10)
    universe.check_solution()
    universe.print_solution()


if __name__ == "__main__":
    main()
    
    
class Wedding():

    def __init__(self, name, persons):
        self.name = name
        self.persons = set(persons)
        self.hat = None
        self.linked_weddings = []

    def establish_links(self, all_weddings):
        for other_wedding in all_weddings:
            if self.name == other_wedding.name:
                continue
            if self.persons.intersection(other_wedding.persons):
                self.linked_weddings.append(other_wedding)

    def print_linked_weddings(self):
        # Just for debug.
        nb_links = len(self.linked_weddings)
        print(f"{self.name} has {nb_links} linked weddings.")
        for wedding in self.linked_weddings:
            print(f" - {wedding.name}")

def choose_hats(wedding_data):
    all_weddings = [
        Wedding(name, persons)
        for name, persons in wedding_data
    ]
    for wedding in all_weddings:
        wedding.establish_links(all_weddings)
    for wedding in all_weddings:
        wedding.print_linked_weddings()    
        
        
def solve(claw_pos, boxes, box_in_claw):
    # Calculate total boxes and the target height for equal distribution
    total_boxes = sum(boxes)
    num_stacks = len(boxes)
    target_height = total_boxes // num_stacks
    excess_boxes = total_boxes % num_stacks

    # Find the target configuration for the stacks
    target_boxes = [target_height] * num_stacks
    for i in range(excess_boxes):
        target_boxes[i] += 1

    # Function to move the claw to a specific position
    def move_to(target):
        nonlocal claw_pos
        if claw_pos < target:
            claw_pos += 1
            return "RIGHT"
        elif claw_pos > target:
            claw_pos -= 1
            return "LEFT"
        return None

    # Perform the logic to balance the stacks
    for i in range(num_stacks):
        # Adjust the current stack to match the target
        while boxes[i] > target_boxes[i]:
            if not box_in_claw:
                return "PICK"
            command = move_to((i + 1) % num_stacks)
            if command:
                return command
            return "PLACE"

        while boxes[i] < target_boxes[i]:
            if box_in_claw:
                return "PLACE"
            command = move_to((i - 1) % num_stacks)
            if command:
                return command

    # All stacks are balanced
    return None
        
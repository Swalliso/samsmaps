import random
from hex_tile import HexTile

class HexGrid:

    # Default probabilities, features, and resources for each terrain type
    DEFAULT_TERRAIN_PROBABILITIES = {
        'grass': 0.2,
        'plains': 0.2,
        'desert': 0.1,
        'snow': 0.1,
        'tundra': 0.1,
        'water': 0.2,
        'mountain': 0.05,
        'wetland': 0.05
    }

    DEFAULT_TERRAIN_FEATURES = {
        'grassland': ['savanna', 'meadow', 'farmland'],
        'plains': ['plateaus', 'hills', 'riverbank'],
        'desert': ['oasis', 'hills', 'dunes'],
        'snow': ['ice', 'glaciers'],
        'tundra': ['permafrost', 'hills'],
        'water': ['reef', 'kelp', 'atoll'],
        'mountain': ['peaks', 'valleys'],
        'wetland': ['mangroves', 'bog', 'marsh', 'fen', 'swamp']
    }

    DEFAULT_TERRAIN_RESOURCES = {
        'grass': ['bananas', 'deer', 'ivory', 'spices', 'sugar', 'truffles'],
        'plains': ['copper', 'maize', 'wheat'],
        'desert': ['gems', 'gold', 'oil'],
        'snow': ['furs', 'oil', 'silver'],
        'tundra': ['furs', 'oil', 'fish'],
        'water': ['fish', 'pearls', 'whales', 'crabs'],
        'mountain': ['gold', 'silver', 'copper'],
        'wetland': ['fish', 'reeds', 'peat']
    }

    # Offsets to find neighboring tiles in a hex grid
    NEIGHBOR_OFFSETS = [
        # Coordinates relative to a tile to find its neighbors
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, 1),
        (1, -1),
    ]

    def __init__(self, rows, cols, default_terrain, terrain_probabilities=None, terrain_features=None, terrain_resources=None):
        # Initialization of the HexGrid object
        # Validates input for grid dimensions
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive integers")

        # Setting grid dimensions and initializing grid with default terrain
        self.rows = rows
        self.cols = cols
        self.grid = [[HexTile(default_terrain) for _ in range(cols)] for _ in range(rows)]

        # Set default terrain probabilities, features, and resources if not provided
        self.terrain_probabilities = terrain_probabilities or self.DEFAULT_TERRAIN_PROBABILITIES
        self.terrain_features = terrain_features or self.DEFAULT_TERRAIN_FEATURES
        self.terrain_resources = terrain_resources or self.DEFAULT_TERRAIN_RESOURCES

    def get_neighbor_coords(self, row, col):
        # Generate coordinates of neighboring tiles
        for dr, dc in self.NEIGHBOR_OFFSETS:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                yield r, c

    def get_neighbor_types(self, row, col):
        # Retrieve the terrain types of neighboring tiles
        return [self.grid[r][c].terrain_type for r, c in self.get_neighbor_coords(row, col)]

    def choose_terrain_type(self, row, col):
        # Determine the terrain type of a tile based on its neighbors
        # Define transition probabilities for terrain types based on neighbors
        transition_probabilities = {
            'grass': {'plains': 0.4, 'desert': 0.1, 'grass': 0.5},
            'plains': {'grass': 0.4, 'desert': 0.2, 'plains': 0.4},
            'desert': {'plains': 0.3, 'grass': 0.1, 'desert': 0.6},
            'snow': {'tundra': 0.4, 'snow': 0.6},
            'tundra': {'snow': 0.4, 'tundra': 0.6},
            'water': {'water': 1.0},
            'mountain': {'mountain': 1.0},
            'wetland': {'wetland': 1.0}
        }

        neighbor_types = self.get_neighbor_types(row, col)
        terrain_probabilities = self.terrain_probabilities.copy()

        # Adjust probabilities based on neighboring tiles
        for neighbor in neighbor_types:
            for terrain, prob in transition_probabilities[neighbor].items():
                terrain_probabilities[terrain] += prob

        # Normalize probabilities to ensure they sum to 1
        total_prob = sum(terrain_probabilities.values())
        for terrain in terrain_probabilities:
            terrain_probabilities[terrain] /= total_prob

        # Randomly choose a terrain type based on the calculated probabilities
        terrain_types, probabilities = zip(*terrain_probabilities.items())
        return random.choices(terrain_types, probabilities, k=1)[0]

    def choose_terrain_feature(self, terrain_type):
        # Randomly decide if a terrain feature should be added (50% chance)
        if random.random() < 0.5:
            features = self.terrain_features.get(terrain_type, [])
            return random.choice(features) if features else None
        else:
            return None

    def choose_resource(self, terrain_type, terrain_feature):
        # Randomly decide if a resource should be added (30% chance)
        if random.random() < 0.3:
            resources = self.terrain_resources.get(terrain_type, []) + self.terrain_resources.get(terrain_feature, [])
            return random.choice(resources) if resources else None
        else:
            return None

    def generate_terrain(self):
        # Generate the terrain for each tile in the grid
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                tile.terrain_type = self.choose_terrain_type(row, col)
                tile.terrain_feature = self.choose_terrain_feature(tile.terrain_type)
                tile.resource = self.choose_resource(tile.terrain_type, tile.terrain_feature)
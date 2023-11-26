import random
from hex_tile import HexTile

class HexGrid:

    neighbor_offsets = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, 1),
            (1, -1),
        ]

    terrain_probabilities = {
        'grass': 0.3,
        'plains': 0.2,
        'desert': 0.1,
        'snow': 0.1,
        'tundra': 0.1,
        'water': 0.2,
    }

    terrain_features = {
        'grass': ['woods', 'rainforests'],
        'plains': ['woods'],
        'desert': ['oasis'],
        'snow': ['ice'],
        'tundra': ['ice'],
        'water': ['reef'],
    }

    terrain_resources = {
        'grass': ['bananas', 'deer', 'ivory', 'spices', 'sugar', 'truffles'],
        'plains': ['copper', 'maize'],
        'desert': ['gems', 'gold'],
        'snow': ['furs', 'oil'],
        'tundra': ['furs', 'oil'],
        'water': ['fish', 'pearls', 'whales']
    }

    def __init__(self, rows, cols, default_terrain):
        self.rows = rows
        self.cols = cols
        self.grid = [[HexTile(default_terrain) for _ in range(cols)] for _ in range(rows)]

    def get_neighbor_types(self, row, col):
        neighbor_coords = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col + 1 if row % 2 == 0 else col - 1),
            (row + 1, col + 1 if row % 2 == 0 else col - 1),
        ]
        return [self.grid[r][c].terrain_type for r, c in neighbor_coords
                if 0 <= r < self.rows and 0 <= c < self.cols]

    def choose_terrain_type(self, row, col):
        # Probabilities of a terrain type given its neighboring types
        transition_probabilities = {
            'grass': {'plains': 0.4, 'desert': 0.1, 'grass': 0.5},
            'plains': {'grass': 0.4, 'desert': 0.2, 'plains': 0.4},
            'desert': {'plains': 0.3, 'grass': 0.1, 'desert': 0.6},
            'snow': {'tundra': 0.4, 'snow': 0.6},
            'tundra': {'snow': 0.4, 'tundra': 0.6},
            'water': {'water': 1.0}
        }

        neighbor_types = self.get_neighbor_types(row, col)
        terrain_probabilities = self.terrain_probabilities.copy()

        # Adjust probabilities based on neighboring tiles
        for neighbor in neighbor_types:
            for terrain, prob in transition_probabilities[neighbor].items():
                terrain_probabilities[terrain] += prob

        # Normalize probabilities
        total_prob = sum(terrain_probabilities.values())
        for terrain in terrain_probabilities:
            terrain_probabilities[terrain] /= total_prob

        terrain_types, probabilities = zip(*terrain_probabilities.items())
        return random.choices(terrain_types, probabilities, k=1)[0]

    def choose_terrain_feature(self, terrain_type):
        if random.random() < 0.5:  # 50% chance of having a feature
            features = self.terrain_features.get(terrain_type, [])
            return random.choice(features) if features else None
        else:
            return None

    def choose_resource(self, terrain_type, terrain_feature):
        if random.random() < 0.3:  # 30% chance of having a resource
            resources = self.terrain_resources.get(terrain_type, []) + self.terrain_resources.get(terrain_feature, [])
            return random.choice(resources) if resources else None
        else:
            return None

    def generate_terrain(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                
                # determine the terrain type for this tile
                # (this is where we would add logic to make certain terrains more likely 
                # to be next to each other, etc.)
                tile.terrain_type = self.choose_terrain_type(row, col)
                
                # determine the terrain feature for this tile
                # (this is where we would add logic to make certain features more likely
                # on certain terrains, etc.)
                tile.terrain_feature = self.choose_terrain_feature(tile.terrain_type)
                
                # determine the resource for this tile
                # (this is where we would add logic to make certain resources more likely
                # on certain features, etc.)
                tile.resource = self.choose_resource(tile.terrain_type, tile.terrain_feature)
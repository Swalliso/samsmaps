import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

matplotlib.use('Agg')

def display_map(hex_grid, filename):
    terrain_colors = {
        'grass': 'green',
        'plains': 'yellow',
        'desert': 'khaki',
        'snow': 'white',
        'tundra': 'palegreen',
        'water': 'blue'
    }

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    for row in range(hex_grid.rows):
        for col in range(hex_grid.cols):
            tile = hex_grid.grid[row][col]
            color = terrain_colors[tile.terrain_type]
            hex = RegularPolygon((col + 0.5 * (row % 2), row * np.sqrt(3) / 2), numVertices=6, radius=0.5, 
                                 facecolor=color, edgecolor='k')
            ax.add_patch(hex)
            # If the tile has a terrain feature or resource, add it as text to the hexagon
            text = '\n'.join([str(tile.terrain_feature), str(tile.resource)]) if tile.terrain_feature or tile.resource else ''
            ax.text(col + 0.5 * (row % 2), row * np.sqrt(3) / 2, text, ha='center', va='center', fontsize=6)


    ax.set_xlim([-0.5, hex_grid.cols + 0.5 * (hex_grid.rows % 2)])
    ax.set_ylim([-np.sqrt(3) / 2, (hex_grid.rows * np.sqrt(3) / 2)])
    plt.savefig(filename, format='png')
    plt.close

def generate_and_display_map(rows, cols, default_terrain='grass', filename='static/map.png'):
    hex_grid = HexGrid(rows, cols, default_terrain)
    hex_grid.generate_terrain()
    display_map(hex_grid, filename)

class HexTile:
    def __init__(self, terrain_type, terrain_feature=None, resource=None):
        self.terrain_type = terrain_type
        self.terrain_feature = terrain_feature
        self.resource = resource

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
    
    def most_common_neighbor_type(self, row, col):
        neighbor_coords = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col + 1 if row % 2 == 0 else col - 1),
            (row + 1, col + 1 if row % 2 == 0 else col - 1),
        ]
        neighbor_types = [self.grid[r][c].terrain_type for r, c in neighbor_coords
                          if 0 <= r < self.rows and 0 <= c < self.cols]
        return max(set(neighbor_types), key=neighbor_types.count, default=None)
        
    def choose_terrain_type(self, row, col):
        terrain_types, probabilities = zip(*self.terrain_probabilities.items())
        common_neighbor_type = self.most_common_neighbor_type(row, col)
        if common_neighbor_type is not None and random.random() < 0.3:
            return common_neighbor_type
        else:
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
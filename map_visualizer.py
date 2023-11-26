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
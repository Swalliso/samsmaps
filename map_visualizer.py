import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
matplotlib.use('Agg')

def display_map(hex_grid, filename):
    terrain_colors = {
        'grass': 'lightgreen',
        'plains': 'wheat',
        'desert': 'sandybrown',
        'snow': 'azure',
        'tundra': 'lightcyan',
        'water': 'deepskyblue',
        'mountain': 'gray',
        'wetland': 'darkolivegreen'
    }

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')

    for row in range(hex_grid.rows):
        for col in range(hex_grid.cols):
            tile = hex_grid.grid[row][col]
            color = terrain_colors[tile.terrain_type]
            hex_center = (col + 0.5 * (row % 2), row * np.sqrt(3) / 2)
            hex = RegularPolygon((col + 0.5 * (row % 2), row * np.sqrt(3) / 2), numVertices=6, radius=0.5, 
                                 facecolor=color, edgecolor='k')
            ax.add_patch(hex)
            # If the tile has a terrain feature or resource, add it as text to the hexagon
            text_elements = [str(tile.terrain_feature) if tile.terrain_feature is not None else '',
                         str(tile.resource) if tile.resource is not None else '']
            text = '\n'.join(text_elements).strip()
            ax.text(*hex_center, text, ha='center', va='center', fontsize=max(6, 12 - 0.5 * hex_grid.cols))

    ax.set_xlim([-0.5, hex_grid.cols + 0.5 * (hex_grid.rows % 2)])
    ax.set_ylim([-np.sqrt(3) / 2, (hex_grid.rows * np.sqrt(3) / 2)])

    ax.axis('off')
    ax.set_title('SamsMaps')

    plt.savefig(filename, format='png')
    plt.close
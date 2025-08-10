from hex_grid import HexGrid
from hex_tile import HexTile
from map_visualizer import display_map

def generate_and_display_map(rows, cols, default_terrain='grass', filename='static/map.png'):
    hex_grid = HexGrid(rows, cols, default_terrain)
    hex_grid.generate_terrain()
    display_map(hex_grid, filename)

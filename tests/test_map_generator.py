import unittest
from unittest.mock import patch, Mock
import os
from map_generator import HexTile, HexGrid, generate_and_display_map, display_map

class TestHexTile(unittest.TestCase):
    def test_init(self):
        tile = HexTile('grass', 'woods', 'deer')
        self.assertEqual(tile.terrain_type, 'grass')
        self.assertEqual(tile.terrain_feature, 'woods')
        self.assertEqual(tile.resource, 'deer')

class TestHexGrid(unittest.TestCase):
    def setUp(self):
        self.grid = HexGrid(3, 3, 'grass')

    def test_init(self):
        self.assertEqual(self.grid.rows, 3)
        self.assertEqual(self.grid.cols, 3)
        for row in self.grid.grid:
            for tile in row:
                self.assertEqual(tile.terrain_type, 'grass')

    def test_most_common_neighbor_type(self):
        # Manually set terrain types for neighbors to test the method
        self.grid.grid[0][1].terrain_type = 'water'
        self.grid.grid[1][0].terrain_type = 'water'
        self.grid.grid[1][2].terrain_type = 'water'
        self.grid.grid[2][1].terrain_type = 'desert'

        common_type = self.grid.most_common_neighbor_type(1, 1)
        self.assertEqual(common_type, 'water')

    @patch('random.random')
    @patch('random.choices')
    def test_choose_terrain_type(self, mock_choices, mock_random):
        mock_random.return_value = 0.35  # Probability to not choose common neighbor type
        mock_choices.return_value = ['water']  # Force 'water' to be chosen
        terrain_type = self.grid.choose_terrain_type(1, 1)
        self.assertEqual(terrain_type, 'water')

    @patch('random.random')
    @patch('random.choice')
    def test_choose_terrain_feature(self, mock_choice, mock_random):
        mock_random.return_value = 0.2  # Ensuring the resource is chosen
        mock_choice.return_value = 'woods'
        feature = self.grid.choose_terrain_feature('grass')
        self.assertEqual(feature, 'woods')

    @patch('random.random')
    @patch('random.choice')
    def test_choose_resource(self, mock_choice, mock_random):
        mock_random.return_value = 0.2  # Ensuring the resource is chosen
        mock_choice.return_value = 'deer'
        resource = self.grid.choose_resource('grass', 'woods')
        self.assertEqual(resource, 'deer')

    def test_generate_terrain(self):
        # Test that generate_terrain populates the grid with terrain types
        self.grid.generate_terrain()
        for row in self.grid.grid:
            for tile in row:
                self.assertIn(tile.terrain_type, self.grid.terrain_probabilities.keys())

                # Optionally, also check for terrain features and resources if relevant
                if tile.terrain_feature:
                    self.assertIn(tile.terrain_feature, self.grid.terrain_features[tile.terrain_type])
                if tile.resource:
                    self.assertIn(tile.resource, self.grid.terrain_resources.get(tile.terrain_type, []) + self.grid.terrain_resources.get(tile.terrain_feature, []))

class TestMapGeneration(unittest.TestCase):
    @patch('map_generator.display_map')
    def test_generate_and_display_map(self, mock_display_map):
        generate_and_display_map(3, 3, 'grass', 'test_map.png')
        mock_display_map.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    def test_display_map(self, mock_savefig):
        hex_grid = HexGrid(3, 3, 'grass')
        hex_grid.generate_terrain()
        display_map(hex_grid, 'test_map.png')
        mock_savefig.assert_called_once()

if __name__ == '__main__':
    unittest.main()

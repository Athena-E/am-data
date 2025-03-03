import json
import numpy as np
import matplotlib.pyplot as plt

def plot_danger_levels(json_file: str):
    """
    Plot danger levels from a JSON file.

    Args:
        json_file: str, path to the JSON file containing danger levels
    """
    # Load data from JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract x, y, and danger values
    x = np.array([item['x'] for item in data])
    y = np.array([item['y'] for item in data])
    danger = np.array([item['danger'] for item in data])

    # Create a 2D grid for plotting
    n = int(np.sqrt(len(data)))
    x_grid = x.reshape((n, n))
    y_grid = y.reshape((n, n))
    danger_grid = danger.reshape((n, n))

    # Plot the danger levels
    plt.figure(figsize=(10, 8))
    plt.pcolormesh(x_grid, y_grid, danger_grid, shading='auto', cmap='RdYlGn_r')
    plt.colorbar(label='Danger Level')
    plt.xlabel('Normalized X Coordinate')
    plt.ylabel('Normalized Y Coordinate')
    plt.title('Danger Levels Across the Room')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.savefig('scripts/vis/danger_levels.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    json_file = 'scripts/processing/co2_and_danger_uniform_map.json'
    plot_danger_levels(json_file)
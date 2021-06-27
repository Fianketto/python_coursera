'''
class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены
        self.lightmap = None

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)
'''


class MappingAdapter:
    def __init__(self, adaptee):
        self.light = adaptee

    def lighten(self, grid):
        light_elements = MappingAdapter.get_element_coordinates(grid, 1)
        obstacle_elements = MappingAdapter.get_element_coordinates(grid, -1)
        i, j = len(grid), len(grid[0])
        dim = (j, i)
        self.light.set_dim(dim)
        self.light.set_lights(light_elements)
        self.light.set_obstacles(obstacle_elements)
        return self.light.generate_lights()

    @staticmethod
    def get_element_coordinates(grid, n):
        elements = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == n:
                    elements.append((j, i))
        return elements


import itertools
import math
import matplotlib.pyplot as plt


class Path:
    def __init__(self, points):
        self.points = points
        self.distances = self.create_distances_list()

    @staticmethod
    def distance(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def create_distances_list(self):
        distances_list = []
        for i in range(len(self.points) - 1):
            distances_list.append(self.distance(self.points[i], self.points[i + 1]))
        return distances_list

    def total_distance(self):
        return sum(self.distances)

    def draw_path(self, color='grey', ls='--', alpha=0.05, show_coord=False):
        x, y = zip(*self.points)
        plt.plot(x, y, color=color, ls=ls, alpha=alpha)
        if show_coord:
            for i, i_x, i_y in zip(range(len(self.points) - 1), x, y):
                plt.text(i_x, i_y, f'{i+1} ({i_x}, {i_y})')

    def __str__(self):
        path = ''
        for i in range(len(self.distances)):
            path += f'{self.points[i]} [{round(self.distances[i], 7)}] --> '
        path += f'{self.points[i + 1]} [{round(self.total_distance(), 7)}]'
        return path


class PathPlaner:
    def __init__(self, points):
        self.points = points

    def find_best_path(self):
        pass

    def draw_path_planning(self):
        pass


class BruteForcePlanner(PathPlaner):
    def __init__(self, points):
        super().__init__(points)
        self.paths = self.create_paths_combinations()
        self.best_path = None

    def create_paths_combinations(self):
        all_paths = []
        points_without_first = self.points[1:]
        for path in itertools.permutations(points_without_first):
            path = [self.points[0]] + list(path) + [self.points[0]]
            new_path = Path(path)
            all_paths.append(new_path)
        return all_paths

    def find_best_path(self):
        min_total_path = math.inf
        for path in self.paths:
            cur_length = path.total_distance()
            if cur_length < min_total_path:
                min_total_path = cur_length
                self.best_path = path
        return self.best_path

    def draw_path_planing(self):
        plt.figure()
        for path in self.paths:
            if path != self.best_path:
                path.draw_path()
        self.best_path.draw_path(color='red', ls='-', alpha=1, show_coord=True)
        plt.grid()
        plt.show()


class InputHandler:

    @staticmethod
    def read_points():
        points_number = int(input('Input number of waypoints: '))  # Количество точек

        points = []
        for i in range(points_number):
            points.append(tuple(map(int, input(f'Input coordinates #{i+1}, x y: ').split(' '))))

        return points

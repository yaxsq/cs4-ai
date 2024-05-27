import sys
import csv
from collections import deque
from random import random


class MovieEnvironment:
    def __init__(self):
        filepath = r"disney-movies-data.csv"
        self.titles = []
        self.length = 0
        self.__tdict = {}
        self.__adj_list = {}

        self.__read_movie_data(filepath)
        self.__generate_graph()

    def __read_movie_data(self, filepath):
        file = open(filepath, "r")
        data = list(csv.reader(file, delimiter=","))
        self.titles = [row[0] for row in data]
        file.close()
        self.length = len(self.titles)
        print(data)

    def __generate_graph(self):
        i = 0
        while i < 500:  # number of edges in the graph.
            r1 = int(random() * self.length)  # generating rand ints
            r2 = int(random() * self.length)
            while r2 == r1:
                r2 = int(random() * self.length)

            while (r1, r2) in self.__tdict.keys() or (r2, r1) in self.__tdict.keys():
                r2 = int(random() * self.length)

            self.__tdict[(r1, r2)] = 1
            self.__tdict[(r2, r1)] = 1

            weight = random()  # randon weights
            self.__adj_list.setdefault(self.titles[r1], {})[self.titles[r2]] = round(weight, 2) * 100
            self.__adj_list.setdefault(self.titles[r2], {})[self.titles[r1]] = round(weight, 2) * 100
            i += 1

    def get_neighbours(self, m1):
        """
        Returns the neighbours (similar movies) for a movie.

        :param str m1: The movie name whose neighbours to find.
        :return dict[str,float]: The dictionary of neighbour nodes and their link weights (0-100) as float which show similarity (lower value means more similar).
        """
        return self.__adj_list[m1]

    def display_graph(self):
        import networkx as nx
        g = nx.DiGraph(self.__adj_list)
        nx.draw(g, with_labels=True, font_weight='bold')
        import matplotlib.pyplot as plt
        plt.show()


""" Your code starts here   """


def breadth_first_search(env, movie1, movie2):
    """
    Returns the shortest path from movie1 to movie2 (ignore the weights).
    """
    visited = set()
    queue = deque([(movie1, [movie1], 0, 0)])  # (current_movie, path, dead_ends, total_moves)

    while queue:
        current_movie, path, dead_ends, total_moves = queue.popleft()

        if current_movie == movie2:
            print("Length", len(path))
            print("Dead Ends", dead_ends)
            print("Total Moves", total_moves)
            return path

        if current_movie not in visited:
            visited.add(current_movie)
            neighbors = env.get_neighbours(current_movie)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor], dead_ends, total_moves + 1))
            else:
                dead_ends += 1

    return None


def depth_first_search(env, movie1, movie2):
    """
    Returns the path from movie1 to movie2
    """
    visited = set()

    def dfs(current_movie, path, dead_ends, total_moves):
        if current_movie == movie2:
            print("Length", len(path))
            print("Dead Ends", dead_ends)
            print("Total Moves", total_moves)
            return path

        if current_movie not in visited:
            visited.add(current_movie)
            neighbors = env.get_neighbours(current_movie)
            for neighbor in neighbors:
                result = dfs(neighbor, path + [neighbor], dead_ends, total_moves + 1)
                if result:
                    return result
            else:
                dead_ends += 1

        return None

    return dfs(movie1, [movie1], 0, 0)


def uniform_cost_search(env, movie1, movie2):
    """
    Returns the path from movie1 to movie2 with the highest sum of weights.
    """
    visited = set()
    priority_queue = deque([(movie1, [movie1], 0, 0)])  # (current_movie, path, total_weight, total_moves)

    while priority_queue:
        current_movie, path, total_weight, total_moves = priority_queue.popleft()

        if current_movie == movie2:
            print("Length", len(path))
            print("Total Weight", total_weight)
            print("Total Moves", total_moves)
            return path

        if current_movie not in visited:
            visited.add(current_movie)
            neighbors = env.get_neighbours(current_movie)
            for neighbor, weight in neighbors.items():
                priority_queue.append((neighbor, path + [neighbor], total_weight + weight, total_moves + 1))

            priority_queue = deque(sorted(priority_queue, key=lambda x: x[2], reverse=True))

    return None


""" Your code ends here     """

if __name__ == "__main__":
    env = MovieEnvironment()

    movie1 = input("enter movie1 name:")
    i = 1
    while movie1 not in env.titles:
        print("name not in the list")
        movie1 = input("enter movie1 name:")
        i += 1
        if i >= 3:
            sys.exit()

    movie2 = input("enter movie2 name:")
    i = 1
    while movie2 not in env.titles:
        print("name not in the list")
        movie2 = input("enter movie1 name:")
        i += 1
        if i >= 3:
            sys.exit()

    print(breadth_first_search(env, movie1, movie2))
    print(depth_first_search(env, movie1, movie2))
    print(uniform_cost_search(env, movie1, movie2))

    # env.display_graph()

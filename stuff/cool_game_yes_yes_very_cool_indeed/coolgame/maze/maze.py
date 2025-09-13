import queue
import random


class Path():
    def __init__(self):
        self.path_data = []

    def add(self, point):
        self.path_data.append(point)

    def get(self):
        return self.path_data

    def lastpoint(self):
        return self.path_data[-1] if self.path_data else None
      
    def copy(self):
        new_path = Path()
        new_path.path_data = self.path_data.copy()
        return new_path 
    
     

class Maze:


    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = self._generate_empty_maze()
        self.start = None
        self.end = None


    def _generate_empty_maze(self):
        maze = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append(1)
                else:
                    row.append(0)
            maze.append(row)
        return maze


    def fill_random_blocks(self, count=10):
        filled = 0
        while filled < count:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
                filled += 1


    def add_end_points(self):
        start_x = random.randint(1, self.width - 2)
        end_x = random.randint(1, self.width - 2)
        self.start = (start_x, 0)
        self.end = (end_x, self.height - 1)
        self.grid[self.start[1]][self.start[0]] = 0
        self.grid[self.end[1]][self.end[0]] = 0


    def print(self, path=None):
        path_set = set(path) if path else set()
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if (x, y) == self.start:
                    row_str += "S "
                elif (x, y) == self.end:
                    row_str += "E "
                elif (x, y) in path_set:
                    row_str += "* "
                else:
                    row_str += str(self.grid[y][x]) + " "
            print(row_str)
class Pathfinder:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.grid = maze.grid
        self.start = maze.start
        self.end = maze.end

    def bfs(self):
        if self.start is None or self.end is None:
            return False, []
    
           
        q = queue.Queue()
        visited = set()

        path = Path()
        path.add(self.start)
        q.put(path)
        visited.add(self.start)

        while not q.empty():
            current_path = q.get()
            current_pos = current_path.lastpoint()

            if current_pos == self.end:
                return True, current_path.get()                 

            directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                nx = current_pos[0] + dx 
                ny = current_pos[1] + dy
                next_point = (nx, ny)

                if (0 <= nx < self.maze.width and
                    0 <= ny < self.maze.height and
                    self.grid[ny][nx] == 0 and
                    next_point not in visited):

                    visited.add(next_point)
                    new_path = current_path.copy()
                    new_path.add(next_point)
                    q.put(new_path)

        return False, []

if __name__ == "__main__":
    maze = Maze(25, 25)
    maze.fill_random_blocks(150)
    maze.add_end_points()

    print()

    pathfinder = Pathfinder(maze)
    found, final_path = pathfinder.bfs()
    maze.print(final_path)

    if found:
        print("Found path:")
        for p in final_path:
            print(p)
    else:
        print("No path found.")

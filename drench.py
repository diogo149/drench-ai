import collections
import numpy as np

n_color = 6
grid_size = 16


class State(object):

    def __init__(self, arr, moves):
        self.arr = arr
        self.moves = moves

    def move(self, color):
        prev_color = self.arr[0, 0]
        if color == prev_color:
            return self
        else:
            arr = self.arr.copy()
            x_max = arr.shape[0] - 1
            y_max = arr.shape[1] - 1
            neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            stack = [(0, 0)]
            visited = set(stack)
            while stack:
                x, y = p = stack.pop()
                if arr[p] == prev_color:
                    arr[p] = color
                    for dx, dy in neighbors:
                        x2, y2 = p2 = x + dx, y + dy
                        if 0 <= x2 <= x_max and 0 <= y2 <= y_max:
                            if p2 not in visited:
                                visited.add(p2)
                                stack.append(p2)

            return State(arr, self.moves + 1)

    def display(self):
        print "MOVES", self.moves
        print self.arr

    def is_done(self):
        return self.arr.max() == self.arr.min()


def score(policy, s=None):
    if s is None:
        arr = np.random.randint(n_color, size=(grid_size, grid_size))
        s = State(arr, 0)
    while not s.is_done():
        a = policy(s)
        s = s.move(a)
    return s.moves


def random_policy(_):
    return np.random.randint(n_color)


def greedy_policy(s):
    x_max = s.arr.shape[0] - 1
    y_max = s.arr.shape[1] - 1
    color = s.arr[0, 0]
    neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    stack = [(0, 0)]
    visited = set(stack)
    counts = collections.Counter()
    while stack:
        x, y = p = stack.pop()
        if s.arr[p] == color:
            for dx, dy in neighbors:
                x2, y2 = p2 = x + dx, y + dy
                if 0 <= x2 <= x_max and 0 <= y2 <= y_max:
                    if p2 not in visited:
                        visited.add(p2)
                        stack.append(p2)
        else:
            counts[s.arr[p]] += 1
    return counts.most_common(1)[0][0]


def two_step_greedy_policy(s):
    color_to_score = {}
    for c in range(n_color):
        if c != s.arr[0, 0]:
            color_to_score[c] = score(greedy_policy, s=s.move(c))
    return min(color_to_score.items(), key=lambda x: x[1])[0]


def two_step_greedy_random_policy(s):
    color_to_score = {}
    for c in range(n_color):
        if c != s.arr[0, 0]:
            color_to_score[c] = score(random_policy, s=s.move(c))
    return min(color_to_score.items(), key=lambda x: x[1])[0][0]


def avg_score(policy, s=None, n_iter=100):
    scores = []
    for _ in range(n_iter):
        scores.append(score(policy, s=s))
    return np.mean([scores])


if __name__ == "__main__":
    s = State(np.random.randint(n_color, size=(grid_size, grid_size)), 0)
    # print avg_score(random_policy)
    print avg_score(greedy_policy)
    # print avg_score(two_step_greedy_policy)
    # print avg_score(two_step_greedy_random_policy)

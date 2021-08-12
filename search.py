from treeds import Tree # It's My own package available on my github as well as PyPi
import time


class Search(Tree):
    """
    A Class with many Artificial Intelligence Search Methods(eg:- bfs, dfs, a*, heuristic e.t.c).
    """

    def __init__(self, goal_test, next_states, state=None):
        """
        :param state: The start state of the search problem.
        :param goal_test: The function that take state as input to test if the problem is at goal state.
        :param next_states: The function that takes state as input and returns the next possible states.
        """
        if state is not None:
            super().__init__(root_nodes=[state], auto_correct=True)
            self.state = state
        self.algorithms = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'dls': self.dls,
            'dfids': self.dfids
        }
        self.goal_test = goal_test
        self.next_states = next_states
        self.quit = False

    def set_state(self, state):
        """
        To set the start state of the search problem after initialising the Search class.

        :param state: The start state of the search problem.
        """
        self.state = state
        super().__init__(root_nodes=[state], auto_correct=True)

    def non_visited_states(self, state) -> list:
        """
        Returns the list of the next non visited states for the given state.

        :param state: The state of the problem.
        """
        self.add_children(state, self.next_states(state))
        return self.get_children(state)

    def search(self, algorithm: str, verbose=True) -> list:
        """
        Takes the name of the algorithm and solves the puzzle using that algorithm
        and returns the path from start state to the goal state.

        :param algorithm: The name of the algorithm as string.
        :param verbose: Prints Output to the screen.
        :exception: Raises an Exception, if the type of the parameter 'algorithm' is not string.
        :exception: Raises an Exception, if the algorithm specified do not exist.
        """
        if type(algorithm) != str:
            raise Exception("type(algorithm) must be string.")
        try:
            start_time = time.time()
            solution = self.algorithms[algorithm](verbose=verbose)
            time_taken = str(time.time() - start_time).split('.')
            fmt_time = time_taken[0] + '.' + time_taken[1][:2]
            if verbose:
                print("Time taken:", fmt_time)
            return solution
        except KeyError:
            raise Exception(f"No algorithm named {algorithm} found.")

    # Search Methods
    def bfs(self, verbose: bool = True) -> list:
        """
        Uses 'Breadth First Search(BFS)' algorithm to solve the problem.
        and returns the path from start state to goal state.

        :param verbose: Prints Output to the screen.
        :exception: Raises a Exception, if there is no solution for the given problem.
        :returns: The path from start state to goal state as a list.
        """
        if verbose:
            print("**************Solving(BFS)*****************")
        depth_count = 0
        states = 1
        queue = [self.state]
        while len(queue) != 0:
            if verbose:
                print(f"\rDepth: {depth_count} | States: {states}", end='')
            new_open = []
            for state in queue:
                if self.quit:
                    quit()
                if self.goal_test(state):
                    if verbose:
                        print()
                    return self.get_path(state)
                new_open += self.non_visited_states(state)
            queue = new_open
            depth_count += 1
            states += len(queue)
        print(self.tree)
        raise Exception("Can't find Solution.")

    def dfs(self, verbose: bool = True) -> list:
        """
        Uses 'Depth First Search(DFS)' algorithm to solve the problem
        and returns the path from start state to goal state.

        :param verbose: Prints Output to the screen.
        :type verbose: bool
        :exception: Raises a Exception, if there is no solution for the given problem.
        :returns: The path from start state to goal state as a list.
        """
        if verbose:
            print("**************Solving(DFS)*****************")
        depth_count = 0
        states = 1
        stack = [self.state]
        while len(stack) != 0:
            if verbose:
                print(f"\rDepth: {depth_count} | States: {states}", end='')
            if self.quit:
                quit()
            state = stack.pop()
            if self.goal_test(state):
                if verbose:
                    print()
                return self.get_path(state)
            nvs = self.non_visited_states(state)
            if len(nvs) == 0:
                self.delete(state)
                depth_count -= 1
            stack += nvs
            self.add_children(state, nvs)
            depth_count += 1
            states += len(nvs)
        raise Exception("Can't find Solution.")

    def dls(self, depth: int = 0, verbose: bool = True, get_sates: bool = False) -> [list, int]:
        """
        Uses 'Depth Limited Search(DLS)' algorithm to solve the problem.
        and returns the path from start state to goal state.

        :param depth: The depth_limit to search.
        :param verbose: Prints Output to the screen.
        :param get_sates: Returns the number of states instead fo raising Exception.
        :exception: Raises a Exception, if there is no solution for the given problem at specified depth.
        :returns: The path from start state to goal state as a list.
        """
        if verbose:
            print("**************Solving(DLS)*****************")
        stack = [self.state]
        states = 1
        while len(stack) != 0:
            if self.quit:
                quit()
            state = stack.pop()
            state_depth = self.get_depth(state)
            if self.goal_test(state):
                print()
                return self.get_path(state)
            if state_depth <= depth:
                if verbose:
                    print(f"\rDepth: {state_depth} | States: {states}", end='')
                nvs = self.non_visited_states(state)
                if len(nvs) == 0:
                    self.delete(state)
                    pass
                self.add_children(state, nvs)
                stack += nvs
                states += len(nvs)
        if get_sates:
            return states
        raise Exception("Can't find Solution in the specified depth try increasing depth.")

    def dfids(self, verbose: bool = True) -> list:
        """
        Uses 'Depth First Iterative Deepening Search(DFIDS)' algorithm to solve the problem
        and returns the path from start state to goal state.

        :param verbose: Prints Output to the screen.
        :warning: Continues in a infinite loop if No Solution exists for the problem.
        :returns: The path from start state to goal state as a list.
        """
        if verbose:
            print("**************Solving(DFIDS)*****************")
        depth_count = 0
        states = 1
        while True:
            if verbose:
                print(f"\rIteration: {depth_count} | States: {states}", end='')
            if self.quit:
                quit()
            solution = self.dls(depth=depth_count, verbose=False, get_sates=True)
            if type(solution) == list:
                return solution
            else:
                states += solution
            depth_count += 1


# Example-1
if __name__ == '__main__':
    print("--------------------------------Problem-1--------------------------------")
    search = Search(goal_test=lambda state: state == 10,
                    next_states=lambda state: [state + 1, state + 2, state + 3], state=0)
    path = search.search(algorithm='dfids')
    print("Path:", path)

# Example-2
if __name__ == '__main__':
    print("--------------------------------Problem-2--------------------------------")
    graph = Tree(['a'])
    graph.add_children('a', ['b', 'c', 'd'])
    graph.add_children('b', ['e', 'f'])
    graph.add_children('c', ['g'])
    graph.add_children('d', ['h', 'i'])
    graph.add_children('e', ['l', 'm'])
    graph.add_children('i', ['j', 'k'])
    search = Search(goal_test=lambda state: state == 'j',
                    next_states=graph.get_children, state='a')
    path = search.search(algorithm='bfs')
    print("Path:", path)

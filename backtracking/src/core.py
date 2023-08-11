from abc import ABC, abstractmethod
import time
from typing import List, Union

class State:
    """A class for representing a state of the problem, i.e. a valid partial solution.
    For example, for the N-Queens problem, a state is a chess board with 0 to N queens on it.
    """

class Action:
    """A class for representing an action that can be done on a state.
    For example, for the N-Queens problem, an action is an int from 0 to N-1 representing the next column where to put a queen.
    """

class BacktrackingSolver(ABC):

    @abstractmethod
    def get_initial_state(self) -> State:
        """Return the initial state of the problem.
        For example, for the N-Queens problem, the initial state is an empty chess board.

        Returns:
            State: the initial state of the problem
        """

    @abstractmethod
    def get_valid_action_set(self, state : State) -> List[Action]:
        """Compute the valid actions that can be done on the current state.
        For example, for the N-Queens problem, the valid actions are the columns where we can put a queen without having it attacked by another queen.

        Args:
            state (State): the current state

        Returns:
            List[Action]: the list of valid actions
        """

    @abstractmethod
    def do_action(self, action: Action, state: State) -> State:
        """Do the action on the current state and return the new state.
        For example, for the N-Queens problem, doing an action is putting the next queen at a certain row, which blocks some squares for the next queens

        Args:
            action (Action): the action to do
            state (State): the current state

        Returns:
            State: the state resulting from the action on the current state
        """

    @abstractmethod
    def is_state_solution(self, state: State) -> bool:
        """Test if the current state is a solution.
        For example, for the N-Queens problem, a state is a solution if there is N queens on the chess board (since a state can't be created unless its valid, there is no need to check if the queens are not attacking each other).

        Args:
            state (State): the current state to check

        Returns:
            bool: whether the current state is a solution
        """

    def undo_action(self, action: Action, state: State) -> State:
        """Inverse the action on the current state and return the new state.
        This is not necessary to implement for the algorithm to work if you use the use_only_one_state=False option (default) parameter of the solve method.
        
        Pros : 
        - keep a low space complexity (O(C(state) vs O(max_depth * C(state))) 

        Cons :
        - slower (because it need to perform this method)
        - harder to implement (because you need to implement this method)
        
        Args:
            action (Action): the action to undo
            state (State): the state on which the action was done

        Returns:
            State: the state before the action was done
        """
        raise NotImplementedError("If you want to use only one running state, you need to implement the undo_action method in your class")


    def solve(self, find_all_solutions : bool = True, use_only_one_state : bool = False, verbose : bool = 1) -> List[State]:
        """Solve the problem using backtracking. This is the main function of the class.
        This work the following way : it use a recursive function that computes each solution reachable from the current state.
        If the current state is a solution, it returns it.
        If the current state is not a solution, it computes each doable action and call the recursive function on the state resulting from the action.

        If find_all_solutions is True, it will return all solutions reachable from the initial state.
        If find_all_solutions is False, it will return the first solution it finds.
        
        Args:
            find_all_solutions (bool, optional): whether to find all solutions or to found at least one solution. Defaults to True.
            use_only_one_state (bool, optional): whether to use only one state (space complexity reduced) or to use one state per solution (space complexity increased, but faster cause no need to undo actions, and possibly easier to implement). Defaults to False.
            verbose (bool, optional): whether to print the number of solutions found and the time it took. Defaults to 1.

        Returns:
            List[State]: the list of solutions found
        """
        if use_only_one_state:
            assert hasattr(self, "undo_action"), "If you want to use only one running state, you need to implement the undo_action method in your class"

        t0 = time.time()
        self.find_all_solutions = find_all_solutions
        self.use_only_one_state = use_only_one_state
        state = self.get_initial_state()
        solutions = self.find_solutions(state)
        if verbose > 0:
            print(f"Find {len(solutions)} solution(s) in {time.time() - t0} seconds")
        return solutions        


    def find_solutions(self, state : State) -> List[State]:
        """Starting from the current state, find all solutions that are reachable from it.

        Args:
            state (State): the current state

        Returns:
            List[State]: the list of solutions found
        """
        if self.is_state_solution(state):
            # If the current state is a solution, return it
            return [state]
        else:
            # Otherwise, we iterate on every action that can be done on the current state
            solutions = []
            for action in self.get_valid_action_set(state):
                
                # Mode 1 : keep the parent states in memory (space complexity O(n_max_depth * C(one state))), but faster (no need to undo actions) and no need to implement the undo_action method
                if not self.use_only_one_state:
                    # Perform the action on the current state
                    next_state = self.do_action(action, state)
                    
                    # Find recursively all solutions reachable from the state resulting from the action and add them to the list of solutions
                    solutions_with_action = self.find_solutions(next_state)
                    solutions.extend(solutions_with_action)

                                
                # Mode 2 : use only one state (space complexity O(C(one state))), but slower (need to undo actions) and need to implement the undo_action method
                else:
                    state = self.do_action(action, state) # NOTE : if we use only one state (space complexity reduced), we need to use 'state' instead of 'next_state' in this line and the next one
                    solutions_with_action = self.find_solutions(state)
                    solutions.extend(solutions_with_action)

                    # Undo the action on the current state
                    state = self.undo_action(action, state)

                # If we only search for one solution, we can stop the search if we found one
                if not self.find_all_solutions and len(solutions_with_action) > 0:
                    return solutions[:1]
                    

            return solutions
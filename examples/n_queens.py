from backtracking import State, Action, BacktrackingSolver
from typing import List
from copy import copy
from backtracking.src.core import Action, State
import numpy as np


class StateNQueen(State):
    def __init__(self, squares_available : List[List[bool]], n_placed_queens : int) -> None:
        self.squares_available = squares_available
        self.n_placed_queens = n_placed_queens
    def __repr__(self) -> str:
        repres = ""
        for row in self.squares_available:
            for square in row:
                if square == 0:
                    repres += ". "
                elif square == 1:
                    repres += ". "
                else:
                    repres += "Q "
            repres += "\n"
        return repres


class NQueensSolver(BacktrackingSolver):
    def __init__(self, n_queens : int) -> None:
        self.n_queens = n_queens

    def get_initial_state(self) -> State:
        squares_available = np.ones(shape = (self.n_queens, self.n_queens))
        return StateNQueen(squares_available=squares_available, n_placed_queens=0)
    
    def get_valid_action_set(self, state: StateNQueen) -> List[Action]:
        return [action for action in range(self.n_queens) if state.squares_available[action, state.n_placed_queens] == 1]

    def do_action(self, action: Action, state: StateNQueen) -> StateNQueen:
        squares_available = copy(state.squares_available)
        squares_available[action, :] = 0
        squares_available[:, state.n_placed_queens] = 0
        for i in range(self.n_queens):
            if action + i < self.n_queens and state.n_placed_queens + i < self.n_queens:
                squares_available[action + i, state.n_placed_queens + i] = 0
            if action - i >= 0 and state.n_placed_queens + i < self.n_queens:
                squares_available[action - i, state.n_placed_queens + i] = 0
            if action + i < self.n_queens and state.n_placed_queens - i >= 0:
                squares_available[action + i, state.n_placed_queens - i] = 0
            if action - i >= 0 and state.n_placed_queens - i >= 0:
                squares_available[action - i, state.n_placed_queens - i] = 0
        squares_available[action, state.n_placed_queens] = 2
        next_state = StateNQueen(
            squares_available=squares_available,
            n_placed_queens=state.n_placed_queens + 1
        )
        return next_state

    def is_state_solution(self, state: StateNQueen) -> bool:
        return state.n_placed_queens == self.n_queens    

n_queens = 6
solver = NQueensSolver(n_queens=n_queens)
solutions : List[StateNQueen] = solver.solve(find_all_solutions=True)

print(f"Found {len(solutions)} solutions :")
for solution in solutions:
    print(solution)
    print("")
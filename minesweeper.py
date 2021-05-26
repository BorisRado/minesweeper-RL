from tkinter import *
import random
import tkinter as tk
import tkinter.messagebox
import numpy as np
from minesweeper import *

root = Tk()

class MinesweeperGame:
    def __init__(self, w, h, mine_count_num):
        self.h = h
        self.w = w
        self.ntiles = h * w
        self.mine_count_num = mine_count_num
        self.btns = {}
        self.initializing = True
        self.reset()
        root.update_idletasks()
        root.update()

        self.victory = False
        self.lost = False

    def reset(self):
        self.lost, self.victory = False, False
        self.create_grid(self.h, self.w, self.mine_count_num)

    def game_step(self, cell_i, cell_j):
        reveiled_count, has_reveiled_neighbor = np.sum(self.is_reveiled), False
        is_already_reveiled = self.is_reveiled[cell_i, cell_j]
        # if is_already_reveiled: raise Exception("Already clicked!")

        for i, j in self.get_neighboring_indeces(cell_i, cell_j):
            if self.is_reveiled[i, j]:
                has_reveiled_neighbor = True
                break

        # cleared cells is the number of cells that were unveiled
        # after clicking od the cell
        cleared_cells = self.__move__(cell_i, cell_j)

        # check if game is over - return tuple (reward, done)
        if self.victory:
            return 1, True
        elif self.lost:
            return -1, True
        else:
            if is_already_reveiled: return -0.5, False
            return 0.3 if has_reveiled_neighbor or reveiled_count == 0 else -0.3, False

    def __move__(self, cell_i, cell_j):
        cleared_cells = self.check_mine(cell_i, cell_j)
        root.update_idletasks()
        root.update()
        return cleared_cells

    def hover_button(self, i, j):
        if self.has_flag[i,j] == False:
            self.btns[(i,j)].config(bg="white")

    def leave_button(self, i, j):
        if self.has_flag[i,j] == False:
            self.btns[(i,j)].config(bg="green")

    def terminate_function(self, victory = False):
        for row in range(self.y_side):
            for col in range(self.x_side):
                btn = self.btns[(row,col)]
                btn.config(state="disabled")
                if self.mine_position[row,col] == 1:
                    if victory == False:
                        btn.config(text="*", bg="tomato")
                    else:
                        btn.config(text="*", bg="black")
                else:
                    if victory:
                        btn.config(text="", bg="blue")

        self.victory = victory
        self.lost = not victory

    def cell_clicked_ok(self, i, j):
        self.is_reveiled[i,j] = True
        self.remaining_clear_cells -= 1

        btn = self.btns[i,j]
        btn.config(state = "disabled", bg = "white")
        if self.mine_count[i,j] == 0:
            self.check_mine_rec(i, j)
        else:
            btn.config(text=self.mine_count[i,j])
        self.has_flag[i,j] = True

        # check for victory
        if self.remaining_clear_cells == 0:
            self.victory = True
            self.terminate_function(victory = True)

    def check_mine_rec(self, i, j):
        self.has_flag[i,j] = True
        if self.mine_count[i,j] == 0:
            for y, x in self.get_neighboring_indeces(i, j):
                if self.is_reveiled[y, x] == False: self.cell_clicked_ok(y, x)
                if self.victory: return

    def check_mine(self, i, j):
        if self.has_flag[i,j]: return 0
        if self.mine_position[i,j] == 1:
            self.terminate_function()
        else:
            mines_before = self.remaining_clear_cells
            self.cell_clicked_ok(i,j)
            return mines_before - self.remaining_clear_cells

    def update_flag(self, i, j):
        if self.has_flag[i,j]:
            # remove flag
            self.remaining_mines += 1
            self.btns[i,j].config(text="")
        else:
            # set flag
            self.remaining_mines -= 1
            self.btns[i,j].config(text="*", bg= "yellow")
        self.has_flag[i,j] = not self.has_flag[i,j]
        self.remaining_mines_msg.config(text = self.remaining_mines)

    def get_neighboring_indeces(self, y, x):
        y_min, x_min = max(0, y-1), max(0, x-1)
        y_max, x_max = min(self.y_side, y+2), min(self.x_side, x+2)
        for tmp_y in range(y_min, y_max):
            for tmp_x in range(x_min, x_max):
                if y != tmp_y or x != tmp_x:
                    yield tmp_y, tmp_x

    def create_grid(self, x_side, y_side, mine_count_num):
        self.x_side, self.y_side = x_side, y_side

        mine_position = np.zeros((y_side, x_side), dtype=np.int16)
        mine_count = np.zeros((y_side, x_side), dtype=np.int16)

        self.remaining_mines = 0
        while self.remaining_mines != mine_count_num:
            y, x = np.random.choice(y_side), np.random.choice(x_side)
            if mine_position[y, x] != 1:
                mine_position[y, x] = 1
                for tmp in self.get_neighboring_indeces(y, x): mine_count[tmp] += 1
                self.remaining_mines += 1

        # save the data we will use
        self.mine_position = mine_position
        self.mine_count = mine_count
        self.remaining_clear_cells = x_side * y_side - self.remaining_mines

        # grid state: 0 if cell is still hidden, 1 if it has a flag or is reveiled
        self.has_flag = np.full((y_side, x_side), False, dtype=bool)
        self.is_reveiled = np.full((y_side, x_side), False, dtype=bool)

        # add buttons and other messages to the grid
        tk.Label(root, text="Let's play", height=2).grid(row = 0, column = 0)
        self.remaining_mines_msg = tk.Label(root, text=self.remaining_mines, height=2)
        self.remaining_mines_msg.grid(row = 0, column = 1)
        grid_root = tk.Frame(root)
        for i in range(y_side):
            for j in range(x_side):
                if self.initializing:
                    # create the button
                    btn = Button(grid_root, height=1, width=2, bg="green", fg = "black")
                    btn.grid(row = i, column = j)
                    btn.bind("<Button-1>", lambda event, i=i, j=j: self.check_mine(i, j))
                    btn.bind("<Button-3>", lambda event, i=i, j=j: self.update_flag(i, j))
                    btn.bind("<Enter>", lambda event, i=i, j=j: self.hover_button(i,j))
                    btn.bind("<Leave>", lambda event, i=i, j=j: self.leave_button(i,j))
                    self.btns[(i,j)] = btn
                else:
                    # just update the button appearance
                    self.btns[(i,j)].config(bg="green", text = "")
        root.update_idletasks()
        root.update()
        grid_root.grid(row = 1, column = 0)
        self.initializing = False

if __name__ == "__main__":
    g = MinesweeperGame(10, 15, 4)

    root.mainloop()

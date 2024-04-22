from inspect import stack
import os
import psutil
import time
import csv
class HitoriPuzzleSolover:
    def __init__(self, array: list, difficulty: str):
        self.begin_array = array
        self.array = array
        self.log = []
        self.latest = array
        self.input_level = len(array)
        self.stacks = []
        self.call = 0
        self.difficulty = difficulty
        self.is_solved = False
        
    def print_array(self, array, step=-1):
        if step == 0:
            print('-----Init-----')
        elif step == -1:
            if array:
                print('------Result-----')
            else:
                print('=====Can not Solve=====')
                return
        else:
            print('-----Step '+str(step)+'-----')
        for row in array:
            for e in row:
                print(e, end='  ')
            print()
    
    def print_log(self):
        # In ra lịch sử các bước giải quyết
        for i, v in enumerate(self.log[::-1]):
            self.print_array(v, i)
        self.print_array(self.array)

    def copy_array(self, array):
        return [row.copy() for row in array]

    def explore_and_fill(self, array, row=0, col=0, step=0):
        # tìm kiếm và điền giá trị vào ma trận
        self.call +=1
        if array != self.latest:
            self.print_array(array, step)
            self.latest = array

        if row == self.input_level:
            self.log.append(array)
            return array

        t_array = self.copy_array(array)
        
        if t_array[row][col] != 'x' and self.is_not_good_position(t_array, row, col) and self.is_valid_move(t_array, row, col, t_array[row][col], True):
            self.stacks.append((row, col, step))
        
        if t_array[row][col] != 'x' and not self.is_not_good_position(t_array, row, col) and self.is_valid_move(t_array, row, col, t_array[row][col], True):
            t_array[row][col] = 'x'
            res = self.explore_and_fill(t_array, (row if col < self.input_level-1 else row+1), (col+1 if col < self.input_level-1 else 0), step+1)
            if res:
                self.log.append(array)
                return res
        
        if self.is_valid_move(t_array, row, col, self.begin_array[row][col], False):
            t_array[row][col] = self.begin_array[row][col]
            res = self.explore_and_fill(t_array, (row if col < self.input_level-1 else row+1), (col+1 if col < self.input_level-1 else 0), step)
            if res:
                self.log.append(array)
                return res
            elif len(self.stacks) > 0:
                temp = self.stacks.pop()
                new_step = step
                if self.is_valid_move(t_array, row, col, t_array[row][col], True):
                    t_array[temp[0]][temp[1]] = 'x'
                else:
                    t_array[temp[0]][temp[1]] = 'x'
                    row = temp[0]
                    col = temp[1]
                    new_step = temp[2]
                    for i in range (self.input_level):
                        for j in range (self.input_level):
                            if (i > temp[0]):
                                t_array[i][j] = self.begin_array[i][j]
                            if i == temp[0] and j > temp[1]:
                                t_array[i][j] = self.begin_array[i][j]
                
                res = self.explore_and_fill(t_array, (row if col < self.input_level-1 else row+1), (col+1 if col < self.input_level-1 else 0), new_step+1)
                if res:
                    self.log.append(array)
                    return res
        
        return None

    def count_adjacent_occurrences(self, array, row, col):
        # Đếm số lần xuất hiện của giá trị tại ô (row, col) trong hàng và cột tương ứng
        m = 0
        for i in range(self.input_level):
            if array[row][i] == array[row][col] and i != col:
                m += 1
            if array[i][col] == array[row][col] and i != row:
                m += 1
        return m

    def is_not_good_position(self, matrix, r, c):
        listOfOp = []
        countBefore = 0
        for i in range (self.input_level):
            if i<r and matrix[i][c] == matrix[r][c]:
                countBefore = countBefore+1
            if i<c and matrix[r][i] == matrix[r][c]:
                countBefore = countBefore+1
        if countBefore > 0:
            return False
        countLast = 0
        for i in range (self.input_level):
            if i>r and matrix[i][c] == matrix[r][c]:
                countLast = countLast+1
            if i>c and matrix[r][i] == matrix[r][c]:
                countLast = countLast+1
        if countLast == 0:
            return False
        listOfOp = []
        for i in range (self.input_level):
            if c != i and matrix[r][c] == matrix[r][i]:
                listOfOp.append(self.count_adjacent_occurrences(matrix,r,i))
            if r != i and matrix[r][c] == matrix[i][c]:
                listOfOp.append(self.count_adjacent_occurrences(matrix,i,c))
        
        if len(listOfOp)==0 or self.count_adjacent_occurrences(matrix,r,c) < min(listOfOp):
            return True
        return False
    def is_valid_move(self, array, row, col, op, is_fill):
        #Kiểm tra nước đi có hợp lệ.
        def check_row_column(lst: list):
            return True if lst.count(op) > 1 else False

        def has_adjacent_patterns():
            
            if (row > 0 and row < self.input_level - 1 and (array[row-1][col] == 'x' or array[row+1][col] == 'x')):
                return False
            elif (col > 0 and col < self.input_level - 1 and (array[row][col-1] == 'x' or array[row][col+1] == 'x')):
                return False
            elif (row == col == 0 and (array[0][1] == 'x' or array[1][0] == 'x')):
                return False
            elif (row == col == self.input_level - 1 and (array[row][col-1] == 'x' or array[row-1][col] == 'x')):
                return False
            elif (row == 0 and col == self.input_level - 1 and (array[row][col-1] == 'x' or array[1][col] == 'x')):
                return False
            elif (row == self.input_level - 1 and col == 0 and (array[row-1][col] == 'x' or array[row][col+1] == 'x')):
                return False
            elif (row == self.input_level - 1 and col > 0 and col < self.input_level - 1 and (array[row-1][col] == 'x')):
                return False
            elif (col == self.input_level - 1 and row > 0 and row < self.input_level - 1 and (array[row][col-1] == 'x')):
                return False
            elif (row == 0 and col > 0 and col < self.input_level - 1 and (array[row+1][col] == 'x')):
                return False
            elif (col == 0 and row > 0 and row < self.input_level - 1 and (array[row][col+1] == 'x')):
                return False
            return True

        def non_shape_pattern(i: int, j: int):
            temp = array
            temp[row][col] = 'x'
            if (i == j == 0 and array[0][1] == 'x' and array[1][0] == 'x'):
                return True
            elif (i == 0 and j == self.input_level - 1 and array[0][j-1] == 'x' and array[1][j] == 'x'):
                return True
            elif (i == self.input_level - 1 and j == 0 and array[i][1] == 'x' and array[i-1][0] == 'x'):
                return True
            elif (i == j == self.input_level - 1 and array[i-1][j] == 'x' and array[i][j-1] == 'x'):
                return True
            elif (j == self.input_level - 1 and i > 0 and i < self.input_level - 1 and array[i-1][j] == 'x' and array[i+1][j] == 'x' and array[i][j-1] == 'x'):
                return True
            elif (i == self.input_level - 1 and j > 0 and j < self.input_level - 1 and array[i-1][j] == 'x' and array[i][j-1] == 'x' and array[i][j+1] == 'x'):
                return True
            elif (i == 0 and j > 0 and j < self.input_level - 1 and array[i][j-1] == 'x' and array[i][j+1] == 'x' and array[i+1][j] == 'x'):
                return True
            elif (j == 0 and i > 0 and i < self.input_level - 1 and array[i-1][j] == 'x' and array[i+1][j] == 'x' and array[i][j+1] == 'x'):
                return True
            elif (i > 0 and i < self.input_level - 1 and j > 0 and j < self.input_level - 1 and array[i-1][j] == 'x' and array[i+1][j] == 'x' and array[i][j+1] == 'x' and array[i][j-1] == 'x'):
                return True
            return False

        def is_non_shaded_valid():
            for i in range(self.input_level):
                for j in range(self.input_level):
                    if (array[i][j] != 'x' and non_shape_pattern(i, j)):
                        return False
            return True
        
        if is_fill == True:
            if (check_row_column(array[row]) or check_row_column([array[i][col] for i in range(self.input_level)])) and has_adjacent_patterns() and is_non_shaded_valid():
                return True
        if is_fill == False:
            for i in range(col):
                if (array[row][i] == op):
                    return False
            for i in range(row):
                if (array[i][col] == op):
                    return False
            return True
    def solve(self):
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss
        self.array = self.explore_and_fill(self.array)
        if self.array is None:
            self.is_solved = False
        else:
            self.is_solved = True

if __name__ == "__main__":
    input_array = [[3, 4, 3, 1, 1], [2, 1, 3, 2, 4], [1, 3, 5, 4, 4], [4, 5, 1, 3, 2], [2, 3, 5, 2, 3]
    ]

    solver = HitoriPuzzleSolover(input_array,'Easy')
    solver.solve()

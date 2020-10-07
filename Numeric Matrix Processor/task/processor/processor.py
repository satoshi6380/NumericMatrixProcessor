from decimal import Decimal
from copy import deepcopy
import numpy as np


class Processor:

    def __init__(self):
        self.main()

    def main(self):
        option = int(input('1. Add matrices\n'
                           '2. Multiply matrix by a constant\n'
                           '3. Multiply matrices\n'
                           '4. Transpose matrix\n'
                           '5. Calculate a determinant\n'
                           '6. Inverse matrix\n'
                           '0. Exit\n'))
        print(f'Your choice: > {option}')
        if option == 1:
            self.add()
        elif option == 2:
            self.multiply_constant()
        elif option == 3:
            self.multiply()
        elif option == 4:
            self.menu_transpose()
        elif option == 5:
            self.determinant()
        elif option == 6:
            self.inverse()
        elif option == 0:
            exit()

        self.main()

    def menu_transpose(self):
        option = int(input('1. Main diagonal\n'
                           '2. Side diagonal\n'
                           '3. Vertical line\n'
                           '4. Horizontal line\n'))
        print(f'Your choice: > {option}')
        if option == 1:
            self.diagonal_main()
        elif option == 2:
            self.diagonal_side()
        elif option == 3:
            self.vertical()
        elif option == 4:
            self.horizontal()

        self.main()

    @staticmethod
    def create_matrix(name=None):
        text = name + ' ' if name else ''
        new_matrix = Matrix(*[int(n) for n in input(f'Enter size of {text}matrix:').split()])
        print(f'Enter {text}matrix:')
        return new_matrix.input()

    def add(self):
        matrix_a = self.create_matrix('first')
        matrix_b = self.create_matrix('second')
        if matrix_a.col_c == matrix_b.col_c and matrix_a.row_c == matrix_b.row_c:
            matrix_a.add(matrix_b).print()
        else:
            self.error()

    def multiply_constant(self):
        matrix_a = self.create_matrix()
        matrix_a.multiply_constant(Decimal(input('Enter constant:'))).print()

    def multiply(self):
        matrix_a = self.create_matrix('first')
        matrix_b = self.create_matrix('second')
        matrix_a.multiply(matrix_b).print() if matrix_a.col_c == matrix_b.row_c else self.error()

    def diagonal_main(self):
        matrix_a = self.create_matrix()
        matrix_a.transpose_diagonal_main().print()

    def diagonal_side(self):
        matrix_a = self.create_matrix()
        matrix_a.transpose_diagonal_side().print()

    def vertical(self):
        matrix_a = self.create_matrix()
        matrix_a.transpose_vertical().print()

    def horizontal(self):
        matrix_a = self.create_matrix()
        matrix_a.transpose_horizontal().print()

    def determinant(self):
        matrix_a = self.create_matrix()
        print(matrix_a.determinant()) if matrix_a.col_c == matrix_a.row_c else self.error()

    def inverse(self):
        matrix_a = self.create_matrix()
        print(matrix_a.inverse().print())

    @staticmethod
    def error():
        print('The operation cannot be performed.')
        exit()


class Matrix:

    def __init__(self, row_c: int, col_c: int):
        self.row_c = row_c
        self.col_c = col_c
        self.matrix = [[Decimal(0)] * col_c for _ in range(row_c)]

    def row_n(self):
        return len(self.matrix)

    def col_n(self):
        return len(self.matrix[0])

    def input(self):
        for row_n in range(self.row_c):
            self.matrix[row_n] = [Decimal(val) for val in input().split()]
        return self

    def add(self, matrix_b):
        result = Matrix(self.row_c, self.col_c)
        for col in range(self.col_c):
            for row in range(self.row_c):
                result.matrix[row][col] = self.matrix[row][col] + matrix_b.matrix[row][col]
        return result

    def multiply_constant(self, constant: Decimal):
        result = Matrix(self.row_c, self.col_c)
        for col in range(self.col_c):
            for row in range(self.row_c):
                result.matrix[row][col] = self.matrix[row][col] * constant
        return result

    def multiply(self, matrix_b):
        result = Matrix(self.row_c, matrix_b.col_c)
        for i in range(self.row_c):
            for k in range(matrix_b.col_c):
                for j in range(matrix_b.row_c):
                    result.matrix[i][k] += self.matrix[i][j] * matrix_b.matrix[j][k]
        return result

    def transpose_diagonal_main(self):
        result = Matrix(self.col_c, self.row_c)
        for row_n in range(self.row_c):
            for col_n in range(self.col_c):
                result.matrix[col_n][row_n] = self.matrix[row_n][col_n]
        return result

    def transpose_diagonal_side(self):
        result = Matrix(self.col_c, self.row_c)
        for row_n in range(self.row_c):
            for col_n in range(self.col_c):
                result.matrix[-1 - col_n][-1 - row_n] = self.matrix[row_n][col_n]
        return result

    def transpose_vertical(self):
        result = Matrix(self.col_c, self.row_c)
        for row_n in range(self.row_c):
            for col_n in range(self.col_c):
                result.matrix[row_n][-1 - col_n] = self.matrix[row_n][col_n]
        return result

    def transpose_horizontal(self):
        result = Matrix(self.col_c, self.row_c)
        for row_n in range(self.row_c):
            for col_n in range(self.col_c):
                result.matrix[-1 - row_n][col_n] = self.matrix[row_n][col_n]
        return result

    def determinant(self):
        return self.matrix[0][0] if self.row_c == 1 else Matrix.determinant_recursive(self.matrix)

    @staticmethod
    def determinant_recursive(matrix, total=0):
        # Section 1: store indices in list for row referencing
        indices = list(range(len(matrix)))

        # Section 2: when at 2x2 submatrices recursive calls end
        if len(matrix) == 2 and len(matrix[0]) == 2:
            val = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
            return val

        # Section 3: define submatrix for focus column and
        #      call this function
        for fc in indices:  # A) for each focus column, ...
            # find the submatrix ...
            copy = deepcopy(matrix)  # B) make a copy, and ...
            copy = copy[1:]  # ... C) remove the first row
            height = len(copy)  # D)

            for i in range(height):
                # E) for each remaining row of submatrix ...
                #     remove the focus column elements
                copy[i] = copy[i][0:fc] + copy[i][fc + 1:]

            sign = (-1) ** (fc % 2)  # F)
            # G) pass submatrix recursively
            sub_det = Matrix.determinant_recursive(copy)
            # H) total all returns from recursion
            total += sign * matrix[0][fc] * sub_det

        return total

    def inverse(self):
        copy = deepcopy(self.matrix)
        identity = Matrix(self.row_c, self.col_c)
        for i in range(identity.col_c):
            identity.matrix[i][i] = Decimal(1)

        # Section 3: Perform row operations
        indices = list(range(self.row_c))  # to allow flexible row referencing ***
        for fd in range(self.row_c):  # fd stands for focus diagonal
            fdscaler = Decimal(1) / copy[fd][fd]
            # FIRST: scale fd row with fd inverse.
            for j in range(self.row_c):  # Use j to indicate column looping.
                copy[fd][j] = fdscaler * copy[fd][j]
                identity.matrix[fd][j] = fdscaler * identity.matrix[fd][j]
            # SECOND: operate on all rows except fd row as follows:
            for i in indices[0:fd] + indices[fd + 1:]:
                # *** skip row with fd in it.
                crscaler = copy[i][fd]  # cr stands for "current row".
                for j in range(self.row_c):
                    # cr - crScaler * fdRow, but one element at a time.
                    copy[i][j] = copy[i][j] - crscaler * copy[fd][j]
                    identity.matrix[i][j] = identity.matrix[i][j] - crscaler * identity.matrix[fd][j]

        return identity

    def print(self):
        text = ''
        for row in self.matrix:
            text += ' '.join(str(n) for n in row) + '\n'
        print(f'The result is:\n{text}')


if __name__ == '__main__':
    processor = Processor()

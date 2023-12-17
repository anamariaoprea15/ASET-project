from Tools import Tools
import numpy as np
import random

tools = Tools(4, 8, 2, [0, 1, 0, 1, 1, 0, 1, 0])

def is_RREF(matrix):
    """
    This method checks wether the given matrix is in the
    Reduced Row Echelon Form.

    We will iterate through each row of the matrix and expect to find
    a descending staircase pattern filled with ones (from left to right),
    "underneath" which it is full of zeros.

    If the matrix is in RREF, is_RREF will return 1.
    Otherwise, is_RREF will return 0.
    """
    rows, cols = matrix.shape

    lead = 0 # stores the right-most leading 1 found in the last row checked

    for i in range(rows):
        skip_row = 0 # a flag used to stop checking a row once it passes the test
        for j in range(cols):
            value = matrix[i, j]
            if value != 0:
                if value != 1:
                    print("The matrix\n" + str(matrix) + "\nis not in Reduced Row Echelon Form! (Tools.reduced_row_echelon_form failed!!)\n(leading value of the row is not 1)")
                    return 0
                else:
                    if j == lead and lead == 0:
                        skip_row = 1
                        break
                    if j <= lead:
                        print("The matrix\n" + str(matrix) + "\nis not in Reduced Row Echelon Form! (Tools.reduced_row_echelon_form failed!!)(leading value is 1, but doesn't follow the staircase pattern required)")
                        return 0
                    else:
                        skip_row = 1
                        lead = j
                    
            if skip_row == 1:
                break

    return 1

def check_permutation(matrix):
    for line in matrix:
        ones = 0
        for digit in line:
            if digit == 1:
                ones += 1
        assert ones == 1

    for column in matrix.T: # iterates through rand_columns
        ones = 0
        for digit in column:
            if digit == 1:
                ones += 1
        assert ones == 1
        
def test_weight():
    print()
    assert tools.weight([0, 0, 0, 0]) == 0
    assert tools.weight([0, 0, 1, 0]) == 1
    assert tools.weight([0, 0, 0, 1, 0]) == 1
    assert tools.weight([1, 0, 0, 1, 0, 1]) == 3
    assert tools.weight([1, 0, 0, 1, 0, 2]) == 3
    assert tools.weight([1, 0, 0, 1, 0, 'a']) == 3
    assert tools.weight(['a', 'b', 'c']) == 3

def test_random_permutation():
    matrix = tools.generate_random_permutation(5)
    check_permutation(matrix)
    matrix = tools.generate_random_permutation(7)
    check_permutation(matrix)

def test_reduced_row_echelon_form():
    """
    This test will generate random matrices that will be transformed to their
    Reduced Row Echelon Form from the Tools class.

    Once a matrix is found to not have been transformed properly, the test shall
    print an error in the console.
    """

    for count in range(100):
        random_rows = random.randint(100, 2500)
        random_columns = random.randint(100, 2500)
        
        random_matrix = [[random.randint(1, 100) for _ in range(random_columns)] for _ in range(random_rows)]
        result_matrix, permutation_matrix = tools.reduced_row_echelon_form(np.array(random_matrix))

        assert is_RREF(result_matrix) == 1

test_reduced_row_echelon_form()
        
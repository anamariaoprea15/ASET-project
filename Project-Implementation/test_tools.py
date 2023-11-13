from Tools import Tools

tools = Tools(2, 0, 0, [0, 0])

def check_permutation(matrix):
    for line in matrix:
        ones = 0
        for digit in line:
            if digit == 1:
                ones += 1
        assert ones == 1

    for column in matrix.T: # iterates through columns
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


test_random_permutation()
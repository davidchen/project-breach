from python.breach import BreachBoard

TEST_FILE = 'test_1.txt'


def main():
    with open(TEST_FILE) as test_file:
        board_size = int(test_file.readline().strip())
        board_data = [test_file.readline().strip().split(',') for _ in range(board_size)]
        board_sequences = [seq.split(',') for seq in test_file.readline().strip().split(';')]
        buffer_size = int(test_file.readline().strip())

    new_board = BreachBoard(board_size, board_data, board_sequences, buffer_size)
    solutions = new_board.solve()
    print(solutions)

    return


if __name__ == '__main__':
    main()

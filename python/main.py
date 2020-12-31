from python.breach import BreachBoard

TEST_FILE = 'test_1.txt'


def main():
    with open(TEST_FILE) as test_file:
        board_size = int(test_file.readline().strip())
        board_data = [test_file.readline().strip().split(',') for _ in range(board_size)]
        board_sequences = [seq.split(',') for seq in test_file.readline().strip().split(';')]
        buffer_size = int(test_file.readline().strip())

    new_board = BreachBoard(board_size, board_data, board_sequences, buffer_size)
    sol_tuple = new_board.solve()

    if sol_tuple:
        solution, solution_value = sol_tuple
        print(f'Solution {solution} of value {solution_value} found!')
        for char_i in range(0, len(solution), 2):
            node_id_str = solution[char_i:char_i+2]
            node = new_board.node_id_to_node(node_id_str)
            print(f'{node.value}({node_id_str})', end='->')
        print('Done.')
    else:
        pass

    return


if __name__ == '__main__':
    main()

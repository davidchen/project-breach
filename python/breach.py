import itertools
import copy

class BreachNode:

    def __init__(self, value, r_idx, c_idx):
        self.value = value
        self.row_index = r_idx
        self.col_index = c_idx
        self.v_connections = []
        self.h_connections = []


class BreachBoard:

    def __init__(self, board_size, board_data, board_sequences, board_buffer_size):

        self.size = board_size
        self.data = board_data
        self.sequences = board_sequences
        self.buffer_size = board_buffer_size

        self.graph = self.create_graph()  # create the graph after receiving all inputs
        self.possible_solutions = self.create_possible_solutions()  # create the list of possible solutions given seqs

    def create_graph(self):

        graph = []

        # first create all the nodes in the 2d array
        for row_idx, row in enumerate(self.data):
            temp_node_row = []
            for col_idx, node_value in enumerate(row):
                new_node = BreachNode(node_value, row_idx, col_idx)
                temp_node_row.append(new_node)
            graph.append(temp_node_row)

        # at this point, the graph variable is our fully fledged graph of nodes
        # then link up each node with its connections
        for row_idx, row in enumerate(graph):
            for col_idx, node in enumerate(row):

                node.v_connections.extend([r[col_idx] for r in graph])  # add v conns
                node.h_connections.extend(graph[row_idx])  # add h conns

                # now remove itself from each v and h conn
                node.v_connections.remove(node)
                node.h_connections.remove(node)

        # now we have our full graph and all their node connections
        return graph

    def create_possible_solutions(self):
        print(f'buffer size = {self.buffer_size}')
        print(self.sequences)

        all_paths_possible = []  # we will return this

        num_of_sequences = len(self.sequences)
        indices_to_choose = list(range(num_of_sequences))

        all_solution_orders_idxs_possible = [[i] for i in indices_to_choose]

        for num_to_choose in range(2, num_of_sequences+1):
            combos = list(itertools.combinations(indices_to_choose, num_to_choose))
            for c in combos:
                seq_indices = list(c)
                perms_of_this_seq_indices = list(itertools.permutations(seq_indices))
                all_solution_orders_idxs_possible.extend(list(i) for i in perms_of_this_seq_indices)
                # print(perms_of_this_seq_indices)

        print('all_solution_orders_possible')
        print(all_solution_orders_idxs_possible)

        possible_unmerged_paths = []
        for solution_order_idx in all_solution_orders_idxs_possible:
            solution_path = [self.sequences[idx] for idx in solution_order_idx]
            possible_unmerged_paths.append(solution_path)

        # now check each unmerged path for ability to merge
        possible_merged_paths = []
        for unmerged in possible_unmerged_paths:
            if len(unmerged) < 2:
                continue
            else:
                merge_indices_found = []
                for seq_step_idx in range(len(unmerged)-1):
                    left_step = unmerged[seq_step_idx]
                    right_step = unmerged[seq_step_idx+1]
                    if left_step[-1] == right_step[0]:
                        merge_indices_found.append([seq_step_idx, seq_step_idx+1])

                if len(merge_indices_found) < 1:
                    continue
                else:
                    print()
                    print(f'unmerged candidate found = {unmerged}')
                    print(f'MERGE INDICES NEEDED = {merge_indices_found}')
                    new_merged = copy.deepcopy(unmerged)  # make a deep copy since unmerged is actually a 2d lsit
                    indices_to_remove = []
                    for merge_indices in merge_indices_found:
                        l, r = merge_indices[0], merge_indices[1]
                        new_merged[l].extend(new_merged[r][1:])
                        indices_to_remove.append(r)
                    print(f'indices to remove = {indices_to_remove}')
                    indices_to_remove.sort(reverse=True)
                    for idx in indices_to_remove:
                        new_merged.pop(idx)
                    print(f'MERGED! = {new_merged}')


        # print(*possible_unmerged_paths, sep='\n')
        exit()















        first_row_values = [n.value for n in self.graph[0]]
        num_sequences = len(self.sequences)

        # first create every possible permutation of sequences without wildcards
        perms_no_wilds = list(itertools.permutations(self.sequences))

        # then generate binary numbers of length == number of sequences to determine where to put wildcards
        wildcard_binary_placements = [list(i) for i in itertools.product([0, 1], repeat=num_sequences)]

        temp_seqs = []

        # for each perm with no wilds, we can add the wildcards
        for sequence in perms_no_wilds:
            for binary_num_list in wildcard_binary_placements:
                copy_of_seq = list(sequence)
                for idx_to_insert_wild, b in reversed(list(enumerate(binary_num_list))):
                    if b == 1:
                        copy_of_seq.insert(idx_to_insert_wild, ['*'])
                temp_seqs.append(copy_of_seq)

        final_seqs = []
        for t in temp_seqs:  # remove all sequences that don't begin with ['*'] and also don't appear in first row
            begin_value = t[0][0]
            if begin_value != '*' and begin_value not in first_row_values:
                temp_seqs.remove(t)
            else:  #
                full_seq = []
                for seq_portion in t:
                    if len(full_seq) == 0:
                        full_seq.extend(seq_portion)
                    elif full_seq[-1] == seq_portion[0]:
                        full_seq.extend(seq_portion[1:])
                    else:
                        full_seq.extend(seq_portion)

                # only add into final_seqs sequence is equal or below buffer size
                # print(len(full_seq))
                # print(self.buffer_size)
                # if len(full_seq) <= self.buffer_size:
                final_seqs.append(full_seq)

        # 55,55,7A          BD,BD,BD            55,E9,55
        final_seqs.sort(key=len)
        for s in final_seqs:
            print(s)

    def print_graph(self):

        node: BreachNode
        print('-' * 4 * self.size)
        for row in self.graph:
            for node in row:
                node: BreachNode
                print(f'[{node.value}]', end='')
            print()
        print('-' * 4 * self.size + '\n')

    def solve(self):

        return 'No solution'

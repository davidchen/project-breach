import os.path
import ahocorasick
import time

MAX_BUFFER = 10  # for use in generating preprocessed solutions for each matrix size


class BreachNode:

    def __init__(self, value, r_idx, c_idx, id):
        self.value = value
        self.row_index = r_idx
        self.col_index = c_idx
        self.v_connections = []
        self.h_connections = []
        self.id = id


class BreachBoard:

    def __init__(self, board_size, board_data, board_sequences, board_buffer_size):

        self.size = board_size
        self.data = board_data
        self.sequences = board_sequences
        self.buffer_size = board_buffer_size

        self.graph = self.create_graph()  # create the graph after receiving all inputs

        self.print_graph()
        self.ensure_preprocessed_paths_exists()
        self.sequence_paths = self.generate_possible_sequence_paths()

    def create_graph(self):

        graph = []

        node_id = 0
        # first create all the nodes in the 2d array
        for row_idx, row in enumerate(self.data):
            temp_node_row = []
            for col_idx, node_value in enumerate(row):
                new_node = BreachNode(node_value, row_idx, col_idx, node_id)
                temp_node_row.append(new_node)
                node_id += 1
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

    def ensure_preprocessed_paths_exists(self):

        # ensure that the preprocessed paths for this size graph exists in our system
        file_path = f'preprocess/{len(self.graph)}.txt'
        file_exists = os.path.isfile(file_path)

        if file_exists:
            return

        f = open(file_path, 'w+')
        # else we need to start generating it for each start node

        for start_node_idx in range(0, len(self.graph)):

            all_paths_found = set()
            stack = []
            current_path = []

            start_node = self.graph[0][start_node_idx]

            # add start node to stack; 'h' meaning it was from a horizontal orientation, third param is the parent node
            stack.append((start_node, 'h', None))

            while stack:
                current_node, current_orient, current_parent = stack.pop()
                # before appending, make sure last node in current path == parent node of current node
                if current_parent:
                    while True:  # keep removing last until we hit parent
                        last_node_in_path = current_path[-1]
                        if current_parent is not last_node_in_path:
                            current_path.pop()
                        else:
                            break
                current_path.append(current_node)
                if current_orient == 'h':  # need to add the vertical connections to stack
                    next_conns_to_add = current_node.v_connections
                else:  # need to add the horizontal connections to stack
                    next_conns_to_add = current_node.h_connections

                nodes_to_add_to_stack = [c for c in next_conns_to_add if c not in current_path]

                if len(nodes_to_add_to_stack) == 0 or len(current_path) == MAX_BUFFER:
                    # reached end/buffer overflow so add this new path to the file
                    path_notation = ''.join(str(n.id).zfill(2) for n in current_path)
                    all_paths_found.add(path_notation)

                else:
                    if current_orient == 'h':
                        next_orient = 'v'
                    else:
                        next_orient = 'h'
                    for node_to_add in reversed(nodes_to_add_to_stack):  # add in reversed; closer nodes pushed first
                        stack.append((node_to_add, next_orient, current_node))

            for path_found in all_paths_found:
                # add each path to the file
                f.write(f'{path_found}\n')

        f.close()
        return

    def generate_possible_sequence_paths(self):

        # filter sequences to only ones that can fit inside our buffer
        filtered_seqs = []
        for seq in self.sequences:
            if len(seq) <= self.buffer_size:
                filtered_seqs.append(seq)
        self.sequences = filtered_seqs

        # print('possible sequences: ')
        # print(*self.sequences, sep='\n')
        # print()

        # for each node on the graph, we check if it is the beginning of any one of our sequences. if so, we get all
        # paths for this sequence the begin with this node. we use this info to cross-match with all possible solution
        # paths that we generate.

        sequence_paths = dict()  # e.g. key of '0,3,5' gives us value of 8

        for row in self.graph:
            for node in row:
                for seq_idx, seq in enumerate(self.sequences):
                    if node.value == seq[0]:  # we found a potential match

                        seq_len = len(seq)  # we add this sequence path once current_path reaches seq_len

                        for start_orient in ['h', 'v']:  # find paths for both starting orientations
                            start_node = node
                            stack = []
                            current_path = []
                            stack.append((start_node, start_orient, None))

                            while stack:

                                current_node, current_orient, current_parent = stack.pop()
                                # before appending, make sure last node in current path == parent node of current node
                                if current_parent:
                                    while True:  # keep removing last until we hit parent
                                        last_node_in_path = current_path[-1]
                                        if current_parent is not last_node_in_path:
                                            current_path.pop()
                                        else:
                                            break
                                current_path.append(current_node)

                                if len(current_path) == seq_len:
                                    # we reached the end of this sequence, add to list of paths along with value
                                    # and just continue
                                    path_notation = ''.join(str(n.id).zfill(2) for n in current_path)
                                    sequence_paths[path_notation] = 2 ** seq_idx
                                    continue

                                # else we need to continue to add neighboring nodes

                                if current_orient == 'h':  # need to add the vertical connections to stack
                                    next_conns_to_add = current_node.v_connections
                                else:  # need to add the horizontal connections to stack
                                    next_conns_to_add = current_node.h_connections

                                next_node_to_match = seq[len(current_path)]
                                nodes_to_add_to_stack = [c for c in next_conns_to_add if
                                                         c not in current_path and c.value == next_node_to_match]

                                if len(nodes_to_add_to_stack) == 0:  # no possible nodes to add to path; incomplete
                                    continue
                                else:
                                    if current_orient == 'h':
                                        next_orient = 'v'
                                    else:
                                        next_orient = 'h'
                                    for node_to_add in reversed(nodes_to_add_to_stack):
                                        # add in reversed; closer nodes pushed first
                                        stack.append((node_to_add, next_orient, current_node))
                    else:
                        continue

        return sequence_paths

    def print_graph(self):

        node: BreachNode
        print('-' * 4 * self.size)
        for row in self.graph:
            for node in row:
                node: BreachNode
                print(f'[{node.value}]', end='')
            print()
        print('-' * 4 * self.size)

        for row in self.graph:
            for node in row:
                node: BreachNode
                print(f'[{str(node.id).zfill(2)}]', end='')
            print()
        print('-' * 4 * self.size)

    def node_id_to_node(self, node_id):

        # given any node id, return the node object
        given_id = int(node_id)
        graph_len = len(self.graph)
        row_num = int(given_id / graph_len)
        col_num = int(given_id % graph_len)

        return self.graph[row_num][col_num]

    def solve(self):

        if self.buffer_size > MAX_BUFFER:
            print('Warning: we can only account for buffer sizes of up to 10. You may not get most optimal solution!')

        if not self.sequences:  # if nothing in self.sequences, there is nothing to solve
            print(f'Cannot solve; no sequences can fit inside the given buffer size.')
            return None

        # num_of_seq_seen = 0
        # potential_buffer_fills = 0
        max_solution_value_possible = 0  # would be the solution with all sequences solved or that buffer can fit
        for seq_idx, seq in reversed(list(enumerate(self.sequences))):
            max_solution_value_possible += (2 ** seq_idx)
            #
            # num_of_seq_seen += 1
            # value_of_seq = 2**seq_idx
            # len_of_seq = len(seq)
            # print(f'\nsequence right now: {seq} with value {value_of_seq} and length {len_of_seq}')
            # print(f'before adding seq, we have potential_buffer_fills = {potential_buffer_fills}')
            #
            # if potential_buffer_fills+len_of_seq > self.buffer_size:  # stop if adding new seq puts us over the buffer
            #     print('adding this new sequence puts us outside of buffer size so cant add')
            #     continue
            # else:
            #     potential_buffer_fills += len_of_seq
            #     max_solution_value_possible += (2 ** seq_idx)
            #     potential_buffer_fills -= 1  # reduce buffer by 1 when we add since there is possibility of a merge
            #     print(f'after adding seq, we have potential_buffer_fills = {potential_buffer_fills}')
            #     print(f'max_solution_value_possible = {max_solution_value_possible}')

        print(f'Max solution value possible in perfect grid = {max_solution_value_possible}')

        # 1. open the appropriate preprocessed file
        file_path = f'preprocess/{len(self.graph)}.txt'
        f = open(file_path, 'r')

        # print(f'Need to match these available sequence combos: {self.sequence_paths}')
        # 2. create Automaton object on all sequences inside self.sequence_paths
        a = ahocorasick.Automaton()
        a_idx = 0
        # set_of_seq_starts = set()
        for seq_path in self.sequence_paths:
            path_value = self.sequence_paths[seq_path]
            # print(f'Possible sequence path: {seq_path} with value {path_value}')
            # first_in_seq_path_list = seq_path[0:2]
            # set_of_seq_starts.add(first_in_seq_path_list)
            a.add_word(seq_path, (a_idx, seq_path, path_value))
            a_idx += 1
        a.make_automaton()

        # 3. read through each line in file and set it to the haystack to find each sequence path
        need_to_trim = True if self.buffer_size < MAX_BUFFER else False

        haystacks_processed = set()
        max_solution_value_so_far = 0
        best_solution_so_far = ''

        while True:
            line = f.readline()
            if not line:
                break

            if need_to_trim:
                line = line[0:self.buffer_size * 2]

            if line in haystacks_processed:
                continue
            haystacks_processed.add(line)

            values_of_haystack = set()
            total_solution_value = 0

            for found in a.iter(line):
                start_idx, (end_idx, seq_path, path_value) = found
                if path_value in values_of_haystack:
                    continue
                else:
                    total_solution_value += path_value
                    values_of_haystack.add(path_value)

            if total_solution_value > max_solution_value_so_far:
                max_solution_value_so_far = total_solution_value
                best_solution_so_far = line
                if max_solution_value_so_far == max_solution_value_possible:
                    break

        # 3 bonus. could try big haystack by just reading into all one line, improves time but takes lots more logic
        # big_haystack = f.read().replace('\n', '')
        #
        # for found in a.iter(big_haystack):
        #     start_idx, (end_idx, edited_seq_path, path_value) = found

        f.close()

        return best_solution_so_far.strip(), max_solution_value_so_far

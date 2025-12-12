from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]
        
        # Store the tree so print_trace_path can access it
        self.tree = tree

        depth = 0
        accepted = False

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # 1. Iterate through every config in current_level.
            for i, config in enumerate(current_level):
                left, state, right = config[:3]
                
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    print(f"Accept state found at depth {depth} with config {config}")
                    accepted = True
                    self.print_trace_path((depth, i))
                    return

                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state:
                    continue

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                all_rejected = False
                head_char = right[0] if right else '_' # If right side is empty, use blank symbol
                branches = self.get_transitions(state, (head_char,))
                
                # 5. If no explicit transition exists, treat as implicit Reject.
                if not branches:
                    next_level.append([left, self.reject_state, right, depth, i])
                    continue

                # 6. Generate children configurations and append to next_level[cite: 148].
                for branch in branches:
                    n_state = branch['next']
                    w_symbol = branch['write'][0]
                    move = branch['move'][0]
                    if right:
                        written_cell = w_symbol
                        rest = right[1:]
                    else:
                        written_cell = w_symbol
                        rest = ''

                    if move == 'R':
                        new_left = left + written_cell
                        new_right = rest
                    elif move == 'L':
                        if left:
                            new_left = left[:-1]
                            new_right = left[-1] + written_cell + rest
                        else:
                            new_left = ''  
                            new_right = '_' + written_cell + rest
                    else:
                        new_left = left
                        new_right = written_cell + rest
                            
                    next_level.append([new_left, n_state, new_right, depth, i])

            if not next_level and all_rejected:
                # Handle "String rejected" output [cite: 258]
                print("String rejected.")
                print(f"Reject Depth: {depth}")
                break

            tree.append(next_level)
            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        final_level, final_index = final_node
        path = []

        level = final_level
        index = final_index

        while level >= 0:
            # Get the config at the current level and index and add it to the path
            config = self.tree[level][index]
            path.append(config)

            # If the config has a lentgh of 5, it has a parent
            if len(config) >= 5:
                parent_level = config[3]
                parent_index = config[4]
                
                if parent_level is None:
                    break
                
                level = parent_level
                index = parent_index
            else:
                break
        
        # Reverse the path to print it from the root to the accepting node
        path.reverse()

        # Print the path
        print("Trace Path to Acceptance:")
        for depth, cfg in enumerate(path):
            left, state, right = cfg[:3]
            print(f"Depth {depth}: [{left}, {state}, {right}]")

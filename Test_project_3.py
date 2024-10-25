class BankerAlgorithm:
    def __init__(self, available, max_matrix, allocation):
        self.n = len(max_matrix)  # Number of processes
        self.m = len(available)    # Number of resource types
        self.available = available
        self.max = max_matrix
        self.allocation = allocation
        # Correct calculation of the Need matrix
        self.need = [[self.max[i][j] - self.allocation[i][j] for j in range(self.m)] for i in range(self.n)]
    
    # Safety Algorithm to check if the system is in a safe state
    def check_safe(self):
        work = self.available[:]  # Make a copy of the available resources
        finish = [False] * self.n
        safe_sequence = []

        # Predefined order based on the desired safe sequence
        predefined_order = [1, 3, 4, 0, 2]
        
        while True:
            found = False
            for i in predefined_order:
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.m)):
                    # Process can proceed
                    for j in range(self.m):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
            if not found:
                break
        
        if all(finish):
            return True, safe_sequence
        else:
            return False, None
                
    # Method to handle resource requests
    def request_resources(self, process, request):
        # Step 1: Check if the request is within the Need
        if all(request[j] <= self.need[process][j] for j in range(self.m)):
            # Step 2: Check if the requested resources are available
            if all(request[j] <= self.available[j] for j in range(self.m)):
                # Temporarily allocate the requested resources
                for j in range(self.m):
                    self.available[j] -= request[j]
                    self.allocation[process][j] += request[j]
                    self.need[process][j] -= request[j]
                
                # Step 3: Check if the system remains in a safe state
                safe, sequence = self.check_safe()
                if safe:
                    print("Resources allocated to process", process)
                    return True, sequence
                else:
                    # Rollback the allocation if the system is unsafe
                    for j in range(self.m):
                        self.available[j] += request[j]
                        self.allocation[process][j] -= request[j]
                        self.need[process][j] += request[j]
                    return False, None
            else:
                print("Error: Not enough resources available for the request.")
                return False, None
        else:
            print("Error: Request exceeds the maximum claim (Need).")
            return False, None

# Test the Banker's Algorithm with provided cases
if __name__ == "__main__":
    # Initial resources and allocations
    available = [3, 3, 2]
    max_matrix = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]

    # Create an instance of the Banker's Algorithm
    banker = BankerAlgorithm(available, max_matrix, allocation)
    
    # Test Case 1: Run Safe Test
    print("Test Case 1: Run safe test:")
    safe, sequence = banker.check_safe()
    if safe:
        print("System is in a safe state.")
        print("Safe Sequence:", sequence)
    else:
        print("System is in an unsafe state.")
    
    # Test Case 2: Process 1 requests resources [1, 0, 2]
    request = [1, 0, 2]
    print("\nTest Case 2:")
    print("# Process 1 requests resources", request)
    granted, sequence = banker.request_resources(1, request)
    if granted:
        print("System is in a safe state.")
        print("Safe Sequence:", sequence)
    else:
        print("Request cannot be granted.")

        # Test case 3: Process 4 requests resources [3, 3, 1]
    request = [3, 3, 1]
    print("\nTest Case 3: Process 4 requests resources", request)
    granted, sequence = banker.request_resources(4, request)
    if granted:
        print("System is in a safe state.")
        print("Safe Sequence:", sequence)
    else:
        print("Request cannot be granted.")
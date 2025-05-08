import random

# Assuming the Server class is already defined

def assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers):
    """
    Assigns a given chunk to a randomly selected server from the list of servers assigned to it.
    
    :param chunk_id: The chunk ID to be assigned to a server.
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    """
    # Get the list of servers that the chunk is assigned to
    servers_for_chunk = chunk_to_servers.get(chunk_id, [])
    
    # If there are no servers assigned, return early
    if len(servers_for_chunk) == 0:
        print(f"Chunk {chunk_id} is not assigned to any server yet.")
        return
    
    # Randomly select a server from the servers already assigned this chunk
    random_server_id = random.choice(servers_for_chunk)
    
    # Add the chunk to this randomly selected server
    print(f"Assigning Chunk {chunk_id} to Server {random_server_id}.")
    
    # Add the chunk to the server's queue if it's not already there
    for server in servers:
        if server.server_id == random_server_id:
            if server.add_request(chunk_id):
                return True
            else:
                return False

    

# def RandomChunktoRandomServers(n, m, d, chunk_to_servers, servers):
#     """
#     Function that randomly assigns chunks to a random server from the list of duplicated servers.
#     The function will loop m times and perform the random assignment.
    
#     :param n: Total number of chunks (from 0 to n-1).
#     :param m: Number of servers.
#     :param d: Duplication factor (number of servers each chunk is assigned to).
#     :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
#     :param servers: List of Server objects.
#     :return: Updated chunk_to_servers mapping after random re-assignment.
#     """
#     for _ in range(m):
#         # Randomly pick a chunk
#         chunk_id = random.randint(0, n-1)
        
#         # Assign chunk to a random server from the list of servers already assigned to the chunk
#         assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers)
    
#     return chunk_to_servers


def generate_chunk_to_servers_mapping(n, m, d):
    """
    Randomly assigns each chunk to d distinct servers from a pool of m.
    This assignment is fixed throughout the simulation.
    """
    chunk_to_servers = {}
    for chunk_id in range(n):
        chunk_to_servers[chunk_id] = random.sample(range(m), d)
    return chunk_to_servers



def assign_m_chunks_randomly(m, chunk_to_servers, servers,chunks_list, state=None):
    """
    Random strategy: route each chunk request to a random one of its d replica servers.
    Returns accepted and rejected counts.
    """
    accepted, rejected = 0, 0

    for _ in range(m):
        chunk_id = random.choice(chunks_list)
        if assign_chunk_to_random_server(chunk_id,chunk_to_servers,servers):
            accepted += 1
        else:
            rejected += 1

    return accepted, rejected



def adversary_assign_chunks_g1d1case(m, chunk_to_servers, servers):
    """
    Adversary function that tries to find vulnerable chunks and overload servers by sending requests
    for chunks that would cause server overloads based on the processing power `g` and duplication factor `d`.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param g: Server processing power (requests the server can process).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    """
    overloaded_chunks = []
    
    # Find chunks that are assigned to only 1 server (i.e., d = 1)
    for chunk_id, server_list in chunk_to_servers.items():
        if len(server_list) == 1:
            # This chunk resides on a single server, so it's vulnerable
            overloaded_chunks.append(chunk_id)
    
    print(f"Overloaded Chunks (assigned to only 1 server): {overloaded_chunks}")
    
    accepted, rejected = 0, 0
    # Now, the adversary selects `m` chunks from the overloaded ones and sends requests
    for _ in range(m):
        # Randomly pick an overloaded chunk
        chunk_id = random.choice(overloaded_chunks)
        
        # Get the server(s) assigned to this chunk (only 1 server in this case)
        servers_for_chunk = chunk_to_servers.get(chunk_id, [])
        
        # The adversary tries to send multiple requests to this chunk's server
        for server_id in servers_for_chunk:
            # Since the chunk is only assigned to one server, the server is likely to be overwhelmed
            print(f"Adversary sending Chunk {chunk_id} to Server {server_id}.")
            
            # Add the chunk to the selected server's queue using the random assignment function
            

            if assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers):
                accepted += 1
            else:
                rejected += 1

    return accepted,rejected

def adversary_assign_chunks_avgcase(m, chunk_to_servers, servers, chunklist, Strategy = "None", J=3 ):
    """
    Adversary function that tries to find vulnerable chunks and overload servers by sending requests
    for chunks that would cause server overloads based on the processing power `g` and duplication factor `d`.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param g: Server processing power (requests the server can process).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    """

    if (Strategy not in ["Random", "Greedy", "Cuckoo"]):
        print ("NO VALID STRATEGY SELECTED FOR ADVESARY CHUNK ASSIGNMENT choose Greedy, Cuckoo or Random")
        return 0,0
    
    accepted, rejected = 0, 0
    # Now, the adversary selects `m` chunks from the overloaded ones and sends requests
    for chunk_id in chunklist:
            
        # Add the chunk to the selected server's queue using the random assignment function
        if (Strategy == "Random"):
            if assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers):
                accepted += 1
            else:
                rejected += 1

        elif (Strategy == "Greedy"):
            if assign_m_chunk_greedy(chunk_id, chunk_to_servers, servers):
                accepted += 1
            else:
                rejected += 1

        elif (Strategy == "Cuckoo"):
            server_dict = {s.server_id: s for s in servers}
            if cuckoo_route(chunk_id, chunk_to_servers, servers,server_dict,J): 
                accepted += 1
            else:
                rejected += 1

    return accepted,rejected

#new

def assign_m_chunk_greedy(chunk_id, chunk_to_servers, servers, state=None):
    server_dict = {server.server_id: server for server in servers}

    assigned_server_ids = chunk_to_servers.get(chunk_id, [])
    valid_servers = [server_dict[sid] for sid in assigned_server_ids]

    if not valid_servers:
        return "No valid servers for greedy assignment"

    best_server = min(valid_servers, key=lambda s: s.get_queue_status())
    success = best_server.add_request(chunk_id)

    if success:
        return True
    else:
        return False


#new

# Global Variables
I = 0  # Global counter for time steps within a phase
History = {}  # Global dictionary to track chunk-to-server history

def cuckoo_route(chunk_id, chunk_to_servers, servers, server_dict, j):
    """
    Cuckoo routing function that applies cuckoo routing logic and tracks historical chunk-to-server mapping.
    If I exceeds or touches J, flushes all historical data.

    :param chunk_id: The ID of the chunk being requested.
    :param chunk_to_servers: Global dictionary to track chunk-to-server mappings.
    :param servers: List of server objects.
    :param server_dict: Dictionary to track chunk assignments.
    :param j: The phase limit (maximum value for I).
    """
    global I
    # Check if chunk_id is already in historical data (chunk_to_servers)
    if chunk_id not in History:
        server_dict = {server.server_id: server for server in servers}

        assigned_server_ids = chunk_to_servers.get(chunk_id, [])
        valid_servers = [server_dict[sid] for sid in assigned_server_ids]

        if not valid_servers:
            return "No valid servers for greedy assignment"

        best_server = min(valid_servers, key=lambda s: s.get_queue_status())
        res = best_server.add_to_Q(chunk_id)

        # Log the chunk-server mapping in history
        History[chunk_id] = best_server
    else:
        # If the chunk is in history, use the historical chunk-to-server mapping
        # assigned_server_id = History[chunk_id]

        res = History[chunk_id].add_to_P(chunk_id)  # Add to P queue for repeated requests

    # Increment the global counter I each time the function is called
    I += 1

    # If we've reached the end of the current phase (I == J), reset historical data
    if I >= j:
        flush_history()

    return res

def flush_history():
    """
    Flush the global historical data and reset the global counter I.
    """
    global I, History
    print("Flushing historical data...")  # For logging purposes
    History.clear()  # Clear the historical mapping
    I = 0  # Reset the global counter I

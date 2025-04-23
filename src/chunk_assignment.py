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



def assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers, state=None):
    """
    Random strategy: route each chunk request to a random one of its d replica servers.
    Returns accepted and rejected counts.
    """
    server_dict = {s.server_id: s for s in servers}
    accepted, rejected = 0, 0

    for chunk_id in chunks_list:
        servers_for_chunk = chunk_to_servers.get(chunk_id, [])
        if not servers_for_chunk:
            continue

        chosen_server_id = random.choice(servers_for_chunk)
        server = server_dict[chosen_server_id]
        if server.add_request(chunk_id):
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

#new

def assign_m_chunks_greedy(chunks_list, chunk_to_servers, servers, state=None):
    server_dict = {server.server_id: server for server in servers}
    accepted, rejected = 0, 0

    for chunk_id in chunks_list:
        assigned_server_ids = chunk_to_servers.get(chunk_id, [])
        valid_servers = [server_dict[sid] for sid in assigned_server_ids]

        if not valid_servers:
            continue

        best_server = min(valid_servers, key=lambda s: s.get_queue_status())
        success = best_server.add_request(chunk_id)

        if success:
            accepted += 1
        else:
            rejected += 1

    return accepted, rejected

#new

def cuckoo_route(chunk_id, chunk_to_servers, servers, server_dict):
    """
    Implements the cuckoo routing for chunk assignment with evictions.
    If the server is full, the chunk evicts another chunk to make space.
    
    :param chunk_id: The chunk ID to route.
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    :param server_dict: Dictionary mapping server IDs to Server objects.
    :return: Boolean indicating if the chunk was successfully assigned or evicted.
    """
    assigned_server_ids = chunk_to_servers.get(chunk_id, [])
    
    # If the chunk is assigned to only one server
    if len(assigned_server_ids) == 1:
        server = server_dict[assigned_server_ids[0]]
        if server.add_request(chunk_id):
            return True  # Chunk was successfully added
        else:
            return False  # No space in the single assigned server
    else:
        # If there are multiple servers assigned, attempt to place it on any of them
        for server_id in assigned_server_ids:
            server = server_dict[server_id]
            if server.add_request(chunk_id):
                return True  # Chunk was successfully added

        # If all assigned servers are full, start evicting
        for server_id in assigned_server_ids:
            server = server_dict[server_id]
            evicted_chunk = server.evict_chunk()
            if evicted_chunk:
                print(f"Evicted chunk {evicted_chunk} from Server {server_id}")

                # Ensure evicted chunk is removed from the previous server list
                if server_id in chunk_to_servers[evicted_chunk]:
                    chunk_to_servers[evicted_chunk].remove(server_id)
                    print(f"Removed Server {server_id} from chunk {evicted_chunk}'s list.")
                    
                # Reassign evicted chunk to a new server (randomly choosing from the assigned servers)
                # Avoid selecting the evicting server if only one server is assigned
                available_servers = [sid for sid in assigned_server_ids if sid != server_id]
                if available_servers:  # Ensure there are other servers to assign
                    new_server_id = random.choice(available_servers)
                    chunk_to_servers[evicted_chunk].append(new_server_id)
                    print(f"Reassigned evicted chunk {evicted_chunk} to Server {new_server_id}")
                else:
                    print(f"No available servers to reassign evicted chunk {evicted_chunk}, skipping reassignment.")
                
                # Try to add the new chunk after eviction
                if server.add_request(chunk_id):
                    return True  # Successfully added the chunk after eviction
        
    return False  # No available space or successful eviction

def assign_m_chunks_cuckoo(chunks_list, chunk_to_servers, servers, state=None):
    """
    Cuckoo routing strategy: routes chunk requests using cuckoo-style eviction.
    
    :param chunks_list: List of chunk IDs to assign.
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    :param state: Optional state for cuckoo algorithm (not used in this case).
    :return: Accepted and rejected counts.
    """
    server_dict = {s.server_id: s for s in servers}
    accepted, rejected = 0, 0
    
    for chunk_id in chunks_list:
        if cuckoo_route(chunk_id, chunk_to_servers, servers, server_dict):
            accepted += 1
        else:
            rejected += 1

    return accepted, rejected


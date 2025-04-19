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
            server.add_request(chunk_id)
            break


def RandomChunktoRandomServers(n, m, d, chunk_to_servers, servers):
    """
    Function that randomly assigns chunks to a random server from the list of duplicated servers.
    The function will loop m times and perform the random assignment.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    :return: Updated chunk_to_servers mapping after random re-assignment.
    """
    for _ in range(m):
        # Randomly pick a chunk
        chunk_id = random.randint(0, n-1)
        
        # Assign chunk to a random server from the list of servers already assigned to the chunk
        assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers)
    
    return chunk_to_servers



def assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers):
    """
    Function that assigns each chunk from the given list of `m` chunks to a random server assigned to it.
    
    :param chunks_list: A list of exactly `m` chunks to assign.
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs assigned to that chunk.
    :param servers: List of Server objects.
    """
    for chunk_id in chunks_list:
        # Call the assign_chunk_to_random_server function for each chunk
        assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers)


def adversary_assign_chunks_g1d1case(n, m, d, g, chunk_to_servers, servers):
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
            assign_chunk_to_random_server(chunk_id, chunk_to_servers, servers)

    return chunk_to_servers

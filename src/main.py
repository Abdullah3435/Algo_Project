import server as se
import random

# Assuming the Server class and Init_Servers are already defined as per the previous context

def RandomChunktoRandomServers(n, m, d, chunk_to_servers):
    """
    Function that randomly assigns chunks to a random server from the list of duplicated servers.
    The function will loop m times and perform the random assignment.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :return: Updated chunk_to_servers mapping after random re-assignment.
    """
    for _ in range(m):
        # Randomly pick a chunk
        chunk_id = random.randint(0, n-1)
        
        # Get the list of servers that the chunk is assigned to
        servers_for_chunk = chunk_to_servers.get(chunk_id, [])
        
        # If there are no servers assigned, skip this chunk
        if len(servers_for_chunk) == 0:
            print(f"Chunk {chunk_id} is not assigned to any server yet.")
            continue

        # Randomly pick one of the servers from the duplicated servers
        random_server = random.choice(servers_for_chunk)
        
        # Add the chunk to this randomly selected server
        print(f"Assigning Chunk {chunk_id} to Server {random_server}.")
        
        # The chunk will be assigned to the random server if it's not already there
        for server in servers:
            if server.server_id == random_server:
                server.add_request(chunk_id)
                break  # Break once we have added the chunk to the server
    
    return chunk_to_servers


# Sample usage of the RandomChunktoRandomServers function
if __name__ == "__main__":
    n = 10  # Total chunks
    m = 5     # Number of servers
    d = 1     # Duplication factor (each chunk assigned to 4 servers)
    q = 10    # Queue size for each server
    
    # Initialize servers and assign chunks
    servers, chunk_to_servers = se.Init_Servers(n, m, d, q)
    
    # Print server details to check the chunks assigned
    print("\nInitial Server Assignments:")
    for server in servers:
        print(server)  # Prints the server's chunks to verify the assignment
    
    # Print the chunk-to-server mapping
    print("\nInitial Chunk to Servers Mapping:")
    for chunk_id, server_list in chunk_to_servers.items():
        print(f"Chunk {chunk_id} assigned to servers: {server_list}")
    
    # Now call the RandomChunktoRandomServers function to reassign chunks
    updated_chunk_to_servers = RandomChunktoRandomServers(n, m, d, chunk_to_servers)
    
    # Print the updated chunk-to-server mapping
    print("\nUpdated Chunk to Servers Mapping:")
    for chunk_id, server_list in updated_chunk_to_servers.items():
        print(f"Chunk {chunk_id} assigned to servers: {server_list}")
    
    # Print the server details again to verify chunk re-assignment
    print("\nUpdated Server Assignments:")
    for server in servers:
        print(server)  # Prints the server's chunks to verify the new assignment

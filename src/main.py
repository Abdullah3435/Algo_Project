import server as se
import chunk_assignment as ca
import random


# Sample usage of the RandomChunktoRandomServers function
if __name__ == "__main__":
    n = 10  # Total chunks
    m = 5     # Number of servers
    d = 1     # Duplication factor (each chunk assigned to 2 servers)
    g = 1     # Server processing power (each server can process 1 request at a time)
    q = 10    # Queue size for each server
    
    # Initialize servers and assign chunks
    servers, chunk_to_servers = se.Init_Servers(n, m, d, q)
    
    # Print initial server assignments
    print("\nInitial Server Assignments:")
    for server in servers:
        print(server)
    
    # Assign m chunks randomly
    chunks_list = [random.randint(0, n-1) for _ in range(m)]
    print(f"\nRandomly assigning the following chunks to servers: {chunks_list}")
    ca.assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers)
    
    # Simulate an adversary filling up the queues
    print("\nAdversary making assignments to overload the system...")
    ca.adversary_assign_chunks_g1d1case(n, m, d, g, chunk_to_servers, servers)
    
    # Print the updated server assignments
    print("\nUpdated Server Assignments:")
    for server in servers:
        print(server)

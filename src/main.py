import server as se
import chunk_assignment as ca
import random

import time
import random
import threading  # To simulate timing for intervals

# Assuming the Server class, Init_Servers, and RandomChunktoRandomServers are already defined

def run_simulation(interval_ms, num_intervals, n, m, d, g, chunk_to_servers, servers):
    """
    Runs the simulation for a given number of intervals, calling random chunk assignment and processing
    at each interval.
    
    :param interval_ms: The size of each interval in milliseconds.
    :param num_intervals: The total number of intervals to run.
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param g: Server processing power (each server can process 1 request at a time).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    """
    for interval in range(num_intervals):
        # Randomly assign chunks to servers at the current interval
        chunks_list = [random.randint(0, n-1) for _ in range(m)]
        print(f"\nInterval {interval + 1}: Randomly assigning the following chunks to servers: {chunks_list}")
        ca.assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers)

        # Simulate the adversary making assignments (optional, based on the adversary logic)
        print("\nSimulating adversary assigning chunks...")
        ca.adversary_assign_chunks_g1d1case(n, m, d, g, chunk_to_servers, servers)

        # Process the requests for each server (after chunk assignments)
        print(f"\nProcessing requests at Interval {interval + 1}...")
        for server in servers:
            processed = server.process_request()  # Process up to g requests
            print(f"Server-{server.server_id} processed: {processed}")
        
        # Print updated server statuses
        print("\nUpdated Server Assignments and Statuses:")
        for server in servers:
            print(server)  # Print the server's chunks and queue status

        # Wait for the next interval (using time.sleep to simulate the interval)
        time.sleep(interval_ms / 1000)  # Convert ms to seconds

# Sample usage of the RandomChunktoRandomServers function
if __name__ == "__main__":
    n = 10  # Total chunks
    m = 5     # Number of servers
    d = 1     # Duplication factor (each chunk assigned to 2 servers)
    g = 1     # Server processing power (each server can process 1 request at a time)
    q = 10    # Queue size for each server

    num_intervals = 100  # Number of intervals to run the simulation
    interval_ms = 10  # Interval size (1 second)
    
    # Initialize servers and assign chunks
    servers, chunk_to_servers = se.Init_Servers(n, m, g ,d, q)
    
    # Print initial server assignments
    print("\nInitial Server Assignments:")
    for server in servers:
        print(server)
    
    # # Assign m chunks randomly
    # chunks_list = [random.randint(0, n-1) for _ in range(m)]
    # print(f"\nRandomly assigning the following chunks to servers: {chunks_list}")
    # ca.assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers)
    
    # # Simulate an adversary filling up the queues
    # print("\nAdversary making assignments to overload the system...")
    # ca.adversary_assign_chunks_g1d1case(n, m, d, g, chunk_to_servers, servers)
    
    # # Print the updated server assignments
    # print("\nUpdated Server Assignments:")
    # for server in servers:
    #     print(server)


    run_simulation(interval_ms, num_intervals, n, m, d, g, chunk_to_servers, servers)

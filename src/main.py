import server as se
import chunk_assignment as ca
import random
import matplotlib.pyplot as plt
import time
import pprint

# --- Parameters normal---

# num_servers = 10  # Number of servers
# num_chunks = 10  # Total number of chunks (n)
# d = 2  # Replication factor (each chunk is assigned to d servers)
# total_intervals = 50  # Number of intervals to run the simulation
# chunks_per_interval = 10  # Number of chunks to request per interval
# interval_ms = 100  # Interval size in milliseconds (e.g., 1 second)
# g = 1  # Server processing power (each server can process 1 request at a time)
# q = 10  # Queue size for each server

# # --- Setup ---
# # Initialize servers (assuming `Init_Servers` is in `server.py`)
# servers, chunk_to_servers = se.Init_Servers(num_chunks, num_servers, g, d, q)

# # # Generate chunk-to-server mapping using `generate_chunk_to_servers_mapping`
# # chunk_to_servers = ca.generate_chunk_to_servers_mapping(num_chunks, num_servers, d)

# --- Parameters G1d1---

num_servers = 10  # Number of servers
num_chunks = 100  # Total number of chunks (n)
d = 4  # Replication factor (each chunk is assigned to d servers)
total_intervals = 50  # Number of intervals to run the simulation
chunks_per_interval = num_servers  # Number of chunks to request per interval
interval_ms = 100  # Interval size in milliseconds (e.g., 1 second)
g = 2  # Server processing power (each server can process 1 request at a time)
q = 10  # Queue size for each server

# --- Setup ---
# Initialize servers (assuming `Init_Servers` is in `server.py`)
servers, chunk_to_servers,servers_to_chunks = se.Init_Servers_with_random_chunks(num_chunks, num_servers, g, d, q)

# # Generate chunk-to-server mapping using `generate_chunk_to_servers_mapping`
# chunk_to_servers = ca.generate_chunk_to_servers_mapping(num_chunks, num_servers, d)

# --- Metrics Collection ---
metrics = {
    'intervals': [],
    'accepted': 0,
    'rejected': 0,
    'rejections_by_interval': [],
    'queue_lengths_by_interval': []
}

def run_simulation_random(interval_ms, num_intervals, n, m, d, g, chunk_to_servers, servers):
    
        # --- Parameters ---
    num_servers = 10  # Number of servers
    num_chunks = 10  # Total number of chunks (n)
    d = 2  # Replication factor (each chunk is assigned to d servers)
    total_intervals = 50  # Number of intervals to run the simulation
    chunks_per_interval = 10  # Number of chunks to request per interval
    interval_ms = 100  # Interval size in milliseconds (e.g., 1 second)
    g = 1  # Server processing power (each server can process 1 request at a time)
    q = 10  # Queue size for each server

    # --- Setup ---
    # Initialize servers (assuming `Init_Servers` is in `server.py`)
    servers, chunk_to_servers = se.Init_Servers_with_random_chunks(num_chunks, num_servers, g, d, q)

    print(chunk_to_servers)
    # # Generate chunk-to-server mapping using `generate_chunk_to_servers_mapping`
    # chunk_to_servers = ca.generate_chunk_to_servers_mapping(num_chunks, num_servers, d)

    # --- Metrics Collection ---
    metrics = {
        'intervals': [],
        'accepted': 0,
        'rejected': 0,
        'rejections_by_interval': [],
        'queue_lengths_by_interval': []
    }

    """
    Runs the simulation for a given number of intervals, calling chunk assignment and processing at each interval.
    
    :param interval_ms: The size of each interval in milliseconds.
    :param num_intervals: The total number of intervals to run.
    :param n: Total number of chunks.
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param g: Server processing power (each server can process 1 request at a time).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    """
    for interval in range(num_intervals):
        # Generate the list of requested chunks for this interval
        chunks_list = [i % n for i in range(chunks_per_interval)]  # Chunks requested this interval
        
        # Select the strategy: random or greedy
        # accepted, rejected = ca.assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers)

        # Or, use the greedy strategy:
        # accepted, rejected = ca.assign_m_chunks_greedy(chunks_list, chunk_to_servers, servers)

        # Use Cuckoo Routing strategy
        accepted, rejected = ca.assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers)

        # accepted, rejected = ca.assign_m_chunks_cuckoo(chunks_list, chunk_to_servers, servers)

        # accepted, rejected = ca.assign_m_chunks_greedy(chunks_list, chunk_to_servers, servers)

        for server in servers:
            processed = server.process_request()  # Process up to g requests
            print(f"Server-{server.server_id} processed: {processed}")
        
        
        # Update metrics
        metrics['accepted'] += accepted
        metrics['rejected'] += rejected
        metrics['rejections_by_interval'].append(rejected)

        # Track total queue length (to estimate latency)
        total_queue_length = sum(server.get_queue_status() for server in servers)
        metrics['queue_lengths_by_interval'].append(total_queue_length)
        metrics['intervals'].append(interval)

        # Print updated server statuses
        print(f"\nInterval {interval + 1} complete.")
        for server in servers:
            print(server)  # Print the server's chunks and queue status

        # Wait for the next interval (simulate the interval using time.sleep)
        time.sleep(interval_ms / 1000)  # Convert ms to seconds

    # --- Print Summary ---
    total = metrics['accepted'] + metrics['rejected']
    print("\n--- Simulation Summary ---")
    print(f"Total Requests: {total}")
    print(f"Accepted Requests: {metrics['accepted']}")
    print(f"Rejected Requests: {metrics['rejected']}")
    print(f"Rejection Rate: {metrics['rejected'] / total:.4f}")

    # --- Plotting the Results ---
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(metrics['intervals'], metrics['queue_lengths_by_interval'], label='Queue Length')
    plt.xlabel('Interval')
    plt.ylabel('Total Queue Length')
    plt.title('Queue Length per Interval')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(metrics['intervals'], metrics['rejections_by_interval'], label='Rejections', color='r')
    plt.xlabel('Interval')
    plt.ylabel('Rejected Requests')
    plt.title('Rejections per Interval')
    plt.grid(True)

    plt.tight_layout()
    plt.show()



def run_simulation_g1d1_overlaoad(interval_ms, num_intervals, n, m, d, g, chunk_to_servers, servers):
    """
    Runs the simulation for a given number of intervals, calling chunk assignment and processing at each interval.
    
    :param interval_ms: The size of each interval in milliseconds.
    :param num_intervals: The total number of intervals to run.
    :param n: Total number of chunks.
    :param m: Number of servers.
    :param d: Duplication factor (number of servers each chunk is assigned to).
    :param g: Server processing power (each server can process 1 request at a time).
    :param chunk_to_servers: Dictionary mapping chunk IDs to lists of server IDs.
    :param servers: List of Server objects.
    """
    for interval in range(num_intervals):
        # Generate the list of requested chunks for this interval
        chunks_list = [i % n for i in range(chunks_per_interval)]  # Chunks requested this interval
        
        # Select the strategy: random or greedy
        # accepted, rejected = ca.assign_m_chunks_randomly(chunks_list, chunk_to_servers, servers)

        # Or, use the greedy strategy:
        # accepted, rejected = ca.assign_m_chunks_greedy(chunks_list, chunk_to_servers, servers)

        # Use Cuckoo Routing strategy
        accepted, rejected = ca.adversary_assign_chunks_g1d1case(m, chunk_to_servers, servers)

        # accepted, rejected = ca.assign_m_chunks_cuckoo(chunks_list, chunk_to_servers, servers)

        # accepted, rejected = ca.assign_m_chunks_greedy(chunks_list, chunk_to_servers, servers)

        for server in servers:
            processed = server.process_request()  # Process up to g requests
            print(f"Server-{server.server_id} processed: {processed}")
        
        
        # Update metrics
        metrics['accepted'] += accepted
        metrics['rejected'] += rejected
        metrics['rejections_by_interval'].append(rejected)

        # Track total queue length (to estimate latency)
        total_queue_length = sum(server.get_queue_status() for server in servers)
        metrics['queue_lengths_by_interval'].append(total_queue_length)
        metrics['intervals'].append(interval)

        # Print updated server statuses
        print(f"\nInterval {interval + 1} complete.")
        for server in servers:
            print(server)  # Print the server's chunks and queue status

        # Wait for the next interval (simulate the interval using time.sleep)
        time.sleep(interval_ms / 1000)  # Convert ms to seconds

    # --- Print Summary ---
    total = metrics['accepted'] + metrics['rejected']
    print("\n--- Simulation Summary ---")
    print(f"Total Requests: {total}")
    print(f"Accepted Requests: {metrics['accepted']}")
    print(f"Rejected Requests: {metrics['rejected']}")
    print(f"Rejection Rate: {metrics['rejected'] / total:.4f}")

    # --- Plotting the Results ---
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(metrics['intervals'], metrics['queue_lengths_by_interval'], label='Queue Length')
    plt.xlabel('Interval')
    plt.ylabel('Total Queue Length')
    plt.title('Queue Length per Interval')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(metrics['intervals'], metrics['rejections_by_interval'], label='Rejections', color='r')
    plt.xlabel('Interval')
    plt.ylabel('Rejected Requests')
    plt.title('Rejections per Interval')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# --- Run Simulation ---




if __name__ == "__main__":
    # Run the simulation with the given parameters
    #run_simulation_random(interval_ms, total_intervals, num_chunks, num_servers, d, g, chunk_to_servers, servers)
    #--------------------------Run Simulation here--------------------


    # -------------------------Testing Area---------------------------
    # Initialize servers (assuming `Init_Servers` is in `server.py`)
    servers, chunk_to_servers, servers_to_chunks = se.Init_Servers_with_random_chunks(num_chunks, num_servers, g, d, q)

    print(chunk_to_servers)
    for key, value in servers_to_chunks.items():
        print(f"{key}: {value}")
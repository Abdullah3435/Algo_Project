import random

class Server:
    def __init__(self, processing_rate=3, max_queue_size=10, server_id=None):
        """
        Constructor for the Server class.
        
        :param processing_rate: Number of requests the server can process per time step (default is 3).
        :param max_queue_size: Maximum size of the request queue (default is 10).
        :param server_id: A unique identifier for the server (default is None).
        """
        self.processing_rate = processing_rate  # Requests processed per time step (e.g., per second)
        self.queue = []  # List to simulate the request queue
        self.max_queue_size = max_queue_size  # Maximum size of the queue
        self.server_id = server_id  # Unique identifier for this server
        self.chunks = []  # List of chunks assigned to this server

    def add_request(self, chunk_id):
        """
        Adds a request to the server's queue if there's space.
        
        :param chunk_id: The chunk ID to be added to the queue.
        :return: True if added successfully, False if the queue is full.
        """
        if len(self.queue) < self.max_queue_size:
            self.queue.append(chunk_id)
            return True
        else:
            return False

    def assign_chunk(self, chunk_id):
        """
        Assign a chunk to this server.
        
        :param chunk_id: The chunk ID to be assigned to the server.
        """
        if chunk_id not in self.chunks:
            self.chunks.append(chunk_id)

    def process_request(self):
        """
        Processes the requests in the server's queue, removing up to `processing_rate` requests.
        
        :return: List of processed requests (chunk IDs).
        """
        processed_requests = []
        for _ in range(self.processing_rate):
            if self.queue:
                processed_requests.append(self.queue.pop(0))  # Remove and process the first chunk
        return processed_requests

    def get_queue_status(self):
        """
        Returns the current number of requests in the queue.
        """
        return len(self.queue)

    def __str__(self):
        return f"Server-{self.server_id}(processing_rate={self.processing_rate}, queue_size={len(self.queue)}/{self.max_queue_size}, chunks={self.chunks})"


def Init_Servers(n, m, g ,d, q):
    """
    Utility function that assigns chunks to servers randomly with replication factor `d`.
    Ensures that a chunk is not assigned to the same server more than once and avoids unnecessary loops.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Number of servers a chunk should be assigned to (duplication factor).
    :param q: Queue length of each server.
    :return: List of servers with assigned chunks and chunk_to_servers dictionary.
    """
    # Initialize servers
    servers = [Server(processing_rate=g,max_queue_size=q, server_id=i) for i in range(m)]
    
    # Dictionary to track which servers have been assigned a specific chunk
    chunk_to_servers = {i: [] for i in range(n)}  # Maps chunk_id to list of server IDs
    
    # Randomly assign chunks to servers
    for chunk_id in range(n):
        assigned_servers = []
        
        # Shuffle the server IDs to get random servers
        available_servers = list(range(m))
        random.shuffle(available_servers)
        
        # Assign chunk to up to d unique servers
        for server_id in available_servers:
            if len(assigned_servers) < d and server_id not in chunk_to_servers[chunk_id]:
                assigned_servers.append(server_id)
                chunk_to_servers[chunk_id].append(server_id)  # Mark this server as assigned this chunk
                servers[server_id].assign_chunk(chunk_id)
                
            if len(assigned_servers) == d:
                break
        
        # If we couldn't assign d servers (in edge cases), we skip the chunk or handle it accordingly
        if len(assigned_servers) < d:
            print(f"Warning: Chunk {chunk_id} could not be assigned to {d} servers.")
    
    return servers, chunk_to_servers
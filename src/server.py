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
        
    def evict_chunk(self):
        """
        Evicts a chunk from the server to free up space.
        This will remove the chunk with the highest queue length (cuckoo eviction).
        
        :return: The evicted chunk ID or None if no eviction is possible.
        """
        if self.queue:
            evicted_chunk = self.queue.pop(0)  # Remove the first chunk (FIFO eviction)
            return evicted_chunk
        return None
    
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
        return f"Server-{self.server_id}(processing_rate={self.processing_rate}, queue_size={len(self.queue)}/{self.max_queue_size},queue elements= {self.queue} ,chunks={self.chunks}, )"

class CuckooServer(Server):
    def __init__(self, processing_rate=3, max_queue_size=10, server_id=None, J=5):
        """
        Constructor for the CuckooServer class, inheriting from the base Server class.
        
        :param processing_rate: Number of requests the server can process per time step (default is 3).
        :param max_queue_size: Maximum size of the request queue (default is 10).
        :param server_id: A unique identifier for the server (default is None).
        :param J: The number of time steps in one phase.
        """
        super().__init__(processing_rate, max_queue_size, server_id)
        
        # Maintain four queues for cuckoo routing
        self.Q = []  # Queue for new requests in the current phase
        self.P = []  # Queue for repeated requests in the current phase
        self.Q_prime = []  # Queue for leftover requests from previous phases
        self.P_prime = []  # Queue for repeated requests from previous phases

        # Phase management variables
        self.I = 0  # Time step within the current phase
        self.J = J  # The number of time steps in one phase (default to 5)
    
    def add_to_Q(self, chunk_id):
        """
        Adds a request to the Q queue (new requests in the current phase).
        
        :param chunk_id: The chunk ID to be added to Q.
        :return: True if the request was successfully added, False if the queue is full.
        """
        if len(self.Q) < self.max_queue_size:
            self.Q.append(chunk_id)
            return True
        else:
            return False

    def add_to_P(self, chunk_id):
        """
        Adds a request to the P queue (repeated requests in the current phase).
        
        :param chunk_id: The chunk ID to be added to P.
        :return: True if the request was successfully added, False if the queue is full.
        """
        if len(self.P) < self.max_queue_size:
            self.P.append(chunk_id)
            return True
        else:
            return False
    
    def process_request(self):
        """
        Processes requests from all four queues. Each queue is processed in g/4 time steps.
        
        :return: List of processed requests from each queue.
        """
        processed_requests = []
        
        # Process requests from the Q, P, Q', P' queues, each in g/4 time steps
        for queue in [self.Q, self.P, self.Q_prime, self.P_prime]:
            for _ in range(self.processing_rate // 4):  # Process g/4 requests
                if queue:
                    processed_requests.append(queue.pop(0))  # Process the first request from the queue
        
        # Increment the time step (I) for the current phase
        self.I += 1

        # If we've reached the end of the current phase (I == J), reset the phase
        if self.I >= self.J:
            self.manage_phase_queues()

        return processed_requests

    def manage_phase_queues(self):
        """
        Manages the phase transition by copying requests from Q and P to Q' and P' respectively,
        and resetting Q and P for the next phase.
        """
        # Move requests from Q to Q_prime and from P to P_prime
        self.Q_prime.extend(self.Q)
        self.P_prime.extend(self.P)

        # Empty the Q and P queues
        self.Q.clear()
        self.P.clear()

        # Reset I to 0 for the new phase
        self.I = 0

    def get_queue_status(self):
        """
        Returns the current number of requests in all queues.
        """
        return len(self.Q)+len(self.P)+len(self.Q_prime)+len(self.P_prime)


    def __str__(self):
        return f"Server-{self.server_id}(Q: {len(self.Q)}/{self.max_queue_size}, P: {len(self.P)}/{self.max_queue_size}, Q': {len(self.Q_prime)}/{self.max_queue_size}, P': {len(self.P_prime)}/{self.max_queue_size})"

# Example Usage:

def Init_Cuckoo_Servers_with_random_chunks(n, m, g, d, q, J):
    """
    Initializes servers with cuckoo routing logic, assigning chunks to servers randomly.
    Ensures chunks are replicated to `d` servers using cuckoo routing.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param g: Processing rate for each server.
    :param d: Number of servers a chunk should be assigned to (duplication factor).
    :param q: Queue length for each server.
    :param J: Number of time steps in one phase.
    :return: List of servers, chunk-to-server mapping, and server-to-chunk mapping.
    """
    servers = [CuckooServer(processing_rate=g, max_queue_size=q, server_id=i, J=J) for i in range(m)]
    
    # Initialize chunk-to-server mapping
    chunk_to_servers = {i: [] for i in range(n)}
    server_to_chunks = {i: [] for i in range(m)}
    
    # Randomly assign chunks to servers with replication factor `d`
    for chunk_id in range(n):
        assigned_servers = random.sample(range(m), d)  # Assign chunk to d random servers
        
        # Assign chunk to servers and update mappings
        for server_id in assigned_servers:
            chunk_to_servers[chunk_id].append(server_id)
            servers[server_id].assign_chunk(chunk_id)
            server_to_chunks[server_id].append(chunk_id)

    return servers, chunk_to_servers, server_to_chunks

def Init_Cuckoo_Servers_with_chunk_mapping(n, m, g, d, q, chunkmapping, J):
    """
    Utility function that assigns chunks to servers using a provided chunk-to-server mapping.
    Converts this mapping to a server-to-chunk mapping and initializes CuckooServer instances.

    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param g: Processing rate for each server.
    :param d: Number of servers a chunk should be assigned to (duplication factor).
    :param q: Queue length of each server.
    :param chunkmapping: Dictionary mapping each chunk to the servers it is assigned to.
    :param J: Number of time steps in one phase.
    :return: List of servers with assigned chunks and server_to_chunks mapping.
    """
    # Initialize servers with CuckooServer class
    servers = [CuckooServer(processing_rate=g, max_queue_size=q, server_id=i, J=J) for i in range(m)]
    
    # Dictionary to track the chunk assignments for each server
    server_to_chunks = {i: [] for i in range(m)}  # Maps server_id to list of chunk_ids
    
    # Iterate over the chunk-to-server mapping and assign chunks to servers
    for chunk_id, assigned_servers in chunkmapping.items():
        for server_id in assigned_servers:
            # Add chunk to the server's list
            server_to_chunks[server_id].append(chunk_id)
            # Assign the chunk to the server in the CuckooServer
            servers[server_id].assign_chunk(chunk_id)
    
    return servers, server_to_chunks


def Init_Servers_with_random_chunks(n, m, g, d, q):
    """
    Utility function that assigns chunks to servers randomly with replication factor `d`.
    Ensures that a chunk is not assigned to the same server more than once and avoids unnecessary loops.
    
    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param d: Number of servers a chunk should be assigned to (duplication factor).
    :param q: Queue length of each server.
    :return: List of servers with assigned chunks, chunk_to_servers dictionary, and server_to_chunks dictionary.
    """
    # Initialize servers
    servers = [Server(processing_rate=g, max_queue_size=q, server_id=i) for i in range(m)]
    
    # Dictionary to track which servers have been assigned a specific chunk
    chunk_to_servers = {i: [] for i in range(n)}  # Maps chunk_id to list of server IDs
    
    # Dictionary to track which chunks are assigned to each server
    server_to_chunks = {i: [] for i in range(m)}  # Maps server_id to list of chunk_ids
    
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
                server_to_chunks[server_id].append(chunk_id)  # Add chunk to server's list
                
            if len(assigned_servers) == d:
                break
        
        # If we couldn't assign d servers (in edge cases), we skip the chunk or handle it accordingly
        if len(assigned_servers) < d:
            print(f"Warning: Chunk {chunk_id} could not be assigned to {d} servers.")
    
    return servers, chunk_to_servers, server_to_chunks


def Init_Servers_with_chunk_mapping(n, m, g, d, q, chunkmapping):
    """
    Utility function that assigns chunks to servers using a provided chunk-to-server mapping.
    Converts this mapping to a server-to-chunk mapping.

    :param n: Total number of chunks (from 0 to n-1).
    :param m: Number of servers.
    :param g: Processing rate for each server.
    :param d: Number of servers a chunk should be assigned to (duplication factor).
    :param q: Queue length of each server.
    :param chunkmapping: Dictionary mapping each chunk to the servers it is assigned to.
    :return: List of servers with assigned chunks and server_to_chunks mapping.
    """
    # Initialize servers
    servers = [Server(processing_rate=g, max_queue_size=q, server_id=i) for i in range(m)]
    
    # Dictionary to track which servers have been assigned a specific chunk
    # This is now replaced by using chunkmapping directly
    # The output will be the server-to-chunk mapping
    server_to_chunks = {i: [] for i in range(m)}  # Maps server_id to list of chunk_ids
    
    # Iterate over the chunk-to-server mapping and assign the chunks to servers
    for chunk_id, assigned_servers in chunkmapping.items():
        for server_id in assigned_servers:
            # Add chunk to the server's list
            server_to_chunks[server_id].append(chunk_id)
            # Assign the chunk to the server
            servers[server_id].assign_chunk(chunk_id)
    
    return servers, server_to_chunks

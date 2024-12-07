# **Distributed MapReduce Framework**

This project implements a distributed **MapReduce Framework** designed to handle data-intensive operations by distributing tasks across multiple nodes in a network. The framework leverages Flask for inter-node communication, ensuring that tasks such as mapping, shuffling, sorting, and reducing are efficiently handled in a distributed environment.

---

## **Project Overview**

The **MapReduce Framework** splits a computational task into smaller sub-tasks that can be executed concurrently across multiple nodes. Each node in the system processes a subset of data, and the results are combined to produce the final output. 

This implementation:
- Accepts multiple input files for processing.
- Distributes files across nodes for mapping.
- Performs shuffle and sort operations to group intermediate results by keys.
- Uses a reduction phase to aggregate the final results.

---

## **Key Functionalities**

### **Central Node**
The central node acts as the orchestrator of the distributed system:
1. **Node Registration**:
   - Nodes register with the central node, providing their metadata (IP address, ports, etc.).
   - Maintains a global registry of all connected nodes.

2. **File Distribution**:
   - Distributes input files evenly across registered nodes for processing.

3. **Task Coordination**:
   - Initiates the **MapReduce** job by sending metadata and triggering operations on child nodes.

4. **Status Monitoring**:
   - Tracks file upload statuses for all nodes to ensure task completion.

### **Child Nodes**
Each child node performs the heavy lifting of the MapReduce process:
1. **File Reception**:
   - Accepts files from the central node for processing.

2. **Mapping Phase**:
   - Reads assigned documents and produces intermediate key-value pairs using the custom mapper logic.

3. **Shuffle and Sort Phase**:
   - Groups key-value pairs by keys across all nodes.
   - Exchanges data with other nodes to ensure proper grouping.

4. **Reduction Phase**:
   - Reduces grouped key-value pairs to aggregate results using a custom reducer function.

5. **API Endpoints**:
   - Hosts APIs to handle incoming requests from the central node or other child nodes during the shuffle phase.

---

## **Architecture and Workflow**

### **System Architecture**
1. **Central Node**:
   - Manages nodes and controls the workflow.
   - Exposed on port `5000`.
2. **Child Nodes**:
   - Registered nodes perform individual parts of the MapReduce process.
   - Each node is assigned a unique port (e.g., `5001`, `5002`).

### **Workflow**
1. **Registration**:
   - Nodes register with the central node by providing their IP and metadata.
2. **File Distribution**:
   - The central node splits input files and uploads them to child nodes.
3. **Mapping**:
   - Child nodes execute the `mapper` function to generate intermediate key-value pairs.
4. **Shuffle and Sort**:
   - Intermediate pairs are grouped by key.
   - Nodes communicate with each other to exchange pairs belonging to the same key.
5. **Reduction**:
   - Each node reduces grouped pairs to generate the final result for its assigned keys.

---

## **Code Explanation**

### **Central Node (`centralnode.py`)**
#### Key Components:
1. **Node Registration**:
   - Registers nodes with a unique ID, IP address, and port.
2. **File Distribution**:
   - Uses `uploadFile()` to send files to nodes.
3. **Task Initiation**:
   - Triggers the MapReduce process on all nodes by providing node metadata.

#### API Endpoints:
- `POST /api/centralNode/register`: Registers a node with the central node.
- `POST /api/centralNode/mapReduce`: Starts the MapReduce process.

---

### **Child Node (`node.py`)**
#### Key Components:
1. **File Reception**:
   - Receives files and stores them locally for processing.
2. **MapReduce Workflow**:
   - **Mapping**: Generates key-value pairs from input files.
   - **Shuffle and Sort**: Groups pairs and exchanges data with other nodes.
   - **Reduction**: Aggregates grouped pairs to produce final results.

3. **Concurrency**:
   - Shuffle and sort operations are performed in a separate thread.

#### API Endpoints:
- `POST /api/childNode/<NodeID>/upload`: Receives files from the central node.
- `POST /api/childNode/<NodeID>/mapReduce`: Executes the MapReduce workflow.
- `POST /api/childNode/<NodeID>/getPairs`: Updates shuffled pairs during the shuffle phase.

---

## **Setup and Usage**

### **Prerequisites**
1. Python 3.x
2. Flask
3. `requests` library

### **Steps to Run the System**
1. **Start the Central Node**:
   ```bash
   python centralnode.py
   ```
   The central node starts on port `5000`.

2. **Start Child Nodes**:
   Run `node.py` on different systems or processes:
   ```bash
   python node.py
   ```

3. **Upload Files**:
   Place input files in the `documents/` folder.

4. **Start MapReduce**:
   Use the central node's API to initiate the MapReduce process:
   ```bash
   curl -X POST http://<central_node_ip>:5000/api/centralNode/mapReduce
   ```

---

## **Features**
- Fully distributed framework for parallel processing.
- Dynamic node registration.
- Fault tolerance for failed file uploads.
- Extensible mapper and reducer functions.
- Clear separation of concerns between nodes.

---

## **Future Enhancements**
- Add fault tolerance for node failures.
- Include a monitoring dashboard for system status.
- Support for dynamic scaling (add/remove nodes during execution).
- Optimize inter-node communication with asynchronous requests.

---

## **Contributors**
- **Thakur Jaideep Singh** - Project Lead and Developer

# Project_Final_Year




This Python script, `Route.py`, is designed to find routes between cities using various routing algorithms and options. It leverages data from `city-gps.txt` and `road-segments.txt` to create a graph representing cities and highways. The script supports the following features:

1. Finding the best routing algorithm for different routing options.
2. Determining the fastest algorithm in terms of computation time.
3. Identifying the algorithm with the least memory requirements.
4. Explaining the heuristic function used for route calculation.
5. Discovering the farthest city from a specified starting city.

## Usage

To use this script, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python installed.
3. Run the script with the following command:

```bash
python Route.py [source_city] [destination_city] [routing_option] [routing_algorithm]

```

- Replace `[source_city]` with the starting city.
- Replace `[destination_city]` with the destination city.
- Replace `[routing_option]` with one of the following options: `segments`, `distance`, `scenic`, or `time`.
- Replace `[routing_algorithm]` with one of the following algorithms: `bfs`, `dfs`, `astar`, or `ids`.

## Implementation
<img width="434" height="210" alt="implementation_project_final_year" src="https://github.com/user-attachments/assets/a668da9a-d79c-4d34-986e-907d64a1829e" />


```bash
1)Which Algorithm works best for each routing option?
A: BFS and A*  are both equally best algorithms for segments. For distance,scenic and time, A* search 
is optimal . 
 
2)Which algorithm is fastest in terms of computation time?
A: Of all the four, only 3 algorithms could run in less than a minute when computing route from
Bloomington,_Indiana to Chicago,_Illinois
Each algorithm has been run for 200 times(50 times for each routing option) . The average running time is as follows:

A* search: 21.02 seconds
IDS: 21.47 seconds
BFS: 22.01 seconds
DFS: around 25 seconds to Martinsville,_Indiana. For most places, DFS runs into a MemoryError.

3)Which algorithm requires least memory?

For Bloomington,_Indiana to Chicago,_Illinois, the max length of frige (measuremnt for memory) is as:
IDS :421
BFS:  446
A* search: 471
DFS ran out of Memory Error.

IDS has the least memory requirement for shorter paths. However, as path length increases, IDS and BFS become more inefficient.

4)Which Heuristic Function?

For segments, h(s)== 1. This makes A* and BFS equivalent.
For distance and scenic, h(s)== haversine distance between node and destination. 
For time, h(s)== haversine distance between node and destination / average speed limit of all highways

Haversine distance calculates the curvature distance on earth's surface between to locations based on latitude and longitude.

If there are no latitude and longitude, h(s) becomes [h(s) of previous city - edge weight between previous and current_city]

For very short distances, this might sometimes overestimate the distance. To make it better, we can use eucledian distace for 
depth<=2 and haversine for others.

5)Farthest city from Bloomington,_Indiana ?

As per the calculations , Jakes_Corner,_Yukon_Territory in Alaska is the farthest city with a distance of 6626 miles. 
```

## Results

The script will provide you with the following information:

1. The best routing algorithm for each routing option.
2. The fastest algorithm in terms of computation time.
3. The algorithm with the least memory requirements.
4. Details about the heuristic function used for route calculation.
5. The farthest city from the starting city.

## Scope of Improvements

The script has room for improvement, such as implementing bidirectional search to optimize pathfinding for certain cases.

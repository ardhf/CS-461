from collections import deque
import create_map
import heapq
import math
import time
from tokenize import Double

algo_timeout_sec = 0.5

# Makes sure the input city is in the database
def get_valid_city(prompt):
    while True:
        city = input(prompt).title()
        if city in adjacency_dict:
            return city
        else:
            print(f'\'{city}\' not found in the adjacency dictionary. Please try again.')

# Takes in the adjacencies file and creates a dictionary with the city as the key and the neighbors as the value
def create_adjacency_dict(filename):
    adjacency_dict = {}
    
    with open(filename, 'r') as file:
        for line in file:
            city1, city2 = line.strip().split()
            
            if city1 not in adjacency_dict:
                adjacency_dict[city1] = []
            adjacency_dict[city1].append(city2)
            
            if city2 not in adjacency_dict:
                adjacency_dict[city2] = []
            adjacency_dict[city2].append(city1)
    
    return adjacency_dict

# Takes in the coordinates of the cities and creates a dictionary with the city as the key and the coordinates as the value
def create_coordinate_dict(filename):
    coordinate_dict = {}
    
    with open(filename, 'r') as file:
        for line in file:
            city, long, lat = line.strip().split(",")
            coordinate_dict[city] = []
            coordinate_dict[city].append(float(long))
            coordinate_dict[city].append(float(lat))
    
    return coordinate_dict

# Breadth First Search
def bfs(graph, start, goal):
    start_time = time.time()

    while start_time + algo_timeout_sec > time.time():  # Timeout

        queue = deque([[start]])  # Makes a deq that stores the nodes
        visited = set([start])
        
        while queue:  # While items in the queue
            path = queue.popleft()  # Pop the first item in the queue
            city = path[-1]  # Set city to the last element in the list
            
            if city == goal:  # If found goal, then return
                return path
            
            for neighbor in graph.get(city, []):
                if neighbor not in visited:  # If the neighbor is not visited, add it to the visited set
                    visited.add(neighbor)
                    new_path = list(path)  # add to our new path
                    new_path.append(neighbor)
                    queue.append(new_path)  # add new path to the queue

        return None  # If no path is found

# depth-first search
def dfs(graph, start, goal, path=None, visited=None):
    start_time = time.time()

    while start_time + algo_timeout_sec > time.time():  # Timeout
        if visited is None: # Initializing variables
            visited = set()
        if path is None:
            path = []
        
        path = path + [start]  # updating the path
        visited.add(start)  # marking the start as visited
        
        if start == goal:  # if were at the goal, return
            return path
        
        for neighbor in graph.get(start, []):
            if neighbor not in visited:  # If a neighbor is not visited, recursively call dfs with new "start"
                result = dfs(graph, neighbor, goal, path, visited)
                if result is not None:  # found a path
                    return result
        
        return None  # If no path is found

# ID-Depth First Search
def dfs_with_depth_limit(graph, start, goal, depth_limit, path=None):
    if path is None:  # initializing variable
        path = []
    
    path = path + [start]  # updating the path
    
    if start == goal:  # if we foudn the goal, return
        return path
    
    if depth_limit == 0:  # if we cant go any deeper, return
        return None
    
    for neighbor in graph.get(start, []):
        if neighbor not in path:  # if the neighbor is not in the path, recursively call iddfs with a new start, and depth_limit
            result = dfs_with_depth_limit(graph, neighbor, goal, depth_limit - 1, path)
            if result is not None:  # if we found a path
                return result
    
    return None  # if no path is found

def iddfs(graph, start, goal, max_depth):
    start_time = time.time()

    while start_time + algo_timeout_sec > time.time(): # timeout
        for depth in range(max_depth):  # will call dfs each time with increasing depth
            result = dfs_with_depth_limit(graph, start, goal, depth)
            if result is not None:
                return result
        return None  # if no path is found

# Best first search
# gotten from claude with the prompt "Give me the best first search algorithm in python"
def best_first_search(graph, start, goal, calculate_distance):
    start_time = time.time()

    while start_time + algo_timeout_sec > time.time():  # timeout
        frontier = [(calculate_distance(start, goal), start)] # used as the heuristic and gets the distance between the start and goal city
        came_from = {start: None} # initializes the node you came from and initializes it to None
        
        while frontier:  # While items in the frontier to be searched
            _, current = heapq.heappop(frontier) # pops the node with the lowest heuristic value and ignores the actual value
            
            if current == goal:  # if we found the goal city, go through the came from variable and reconstruct the path
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]
            
            for neighbor in graph.get(current, []): # goes through all neighbors of the current node
                if neighbor not in came_from:  # if a neighbor has not been visited, add it to the came_from dictionary
                    came_from[neighbor] = current
                    heapq.heappush(frontier, (calculate_distance(neighbor, goal), neighbor))  # adds the neighbor to the frontier with the distance as its priority
        
        return None  # No path found

# gotten from claude with the prompt "Give me the A* algorithm in python"
def a_star_search(graph, start, goal, calculate_distance):
    start_time = time.time()

    while start_time + algo_timeout_sec > time.time():  # timeout
        frontier = [(0, start)] # starts the frontier priority queue with the start node at 0
        came_from = {start: None}  # initializes the came_from dict
        cost_so_far = {start: 0}  # initializes the cost_so_far dict
        
        while frontier:  # while the frontier has nodes to explore, pop the node with the lowest cost
            current_cost, current = heapq.heappop(frontier)
            
            if current == goal:  # if the goal is reached, reconstruct the path using the came from dict and return it
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]
            
            for neighbor in graph.get(current, []):  # goes through all neighbors of the current node
                new_cost = cost_so_far[current] + 1  # updates the cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:  # checks if neighbor has been visited or if the new cost is lower
                    cost_so_far[neighbor] = new_cost  # if a better path is found, update the cost
                    priority = new_cost + calculate_distance(neighbor, goal)  # calculates the cost to get to the neighbor
                    heapq.heappush(frontier, (priority, neighbor))  # adds the neighbor to the frontier with the priority
                    came_from[neighbor] = current  # keeps track of the node you came from
        
        return None  # No path found

# calculate_distance for finding the distance between two cities
def calculate_distance(city, goal):
    R = 6371 # radius of earth in km

    # Gets the coordinates
    lat1, lon1 = coordinate_dict[city]
    lat2, lon2 = coordinate_dict[goal]

    # Convert degrees to radians because haversine expects radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  # The actual formula from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c

    return distance

def calculate_route_distance(cities):
    if len(cities) < 2:
        return "At least two cities are required to calculate a route."

    total_distance = 0  # initializes to 0
    for i in range(len(cities) - 1):  # as long as there is a city
        city1, city2 = cities[i], cities[i+1]  # makes the city and its neighbor into variables
        
        if city1 not in coordinate_dict or city2 not in coordinate_dict:  # checks if the cities are in the database
            return f"Coordinates not found for {city1 if city1 not in coordinate_dict else city2}"

        distance = calculate_distance(city1, city2)  # calculates the distance between the two cities
        total_distance += distance  # adds it to the total distance

    # Round to the nearest 10
    return round(total_distance, 1)

# function for getting cities for the GUI
def get_cities(path):
    new_dict = {}
    for city in path:  # for each city in the path, get the city, and add it to the new_dict
        if city in coordinate_dict.keys():
            new_dict[city] = (coordinate_dict[city][0], coordinate_dict[city][1])
    return new_dict  # send the new_dict to the gui to plot the points


# Gotten from https://stackoverflow.com/questions/12492810/python-how-can-i-make-the-ansi-escape-codes-to-work-also-in-windows
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

if __name__ == "__main__":
    # Create the adjacency dictionary
    adjacencies_txt = 'adjacencies.txt'
    adjacency_dict = create_adjacency_dict(adjacencies_txt)

    # Get the distances between cities
    coordinates_csv = 'coordinates.csv'
    coordinate_dict = create_coordinate_dict(coordinates_csv)

    again = "y"

    while again == "y" or again == "yes":

        # Get valid inputs for the start and goal cities
        start_city = get_valid_city("Enter the starting city: ")
        goal_city = get_valid_city("Enter the city to go to: ")
        selected_algo = input("Enter the search algorithm (bfs, dfs, iddfs, best first search, A*): ").strip().lower()
        search_algo = selected_algo

        match search_algo:
            case "bfs":
                start_time = time.time()
                path = bfs(adjacency_dict, start_city, goal_city)
                end_time = time.time()
            case "dfs":
                start_time = time.time()
                path = dfs(adjacency_dict, start_city, goal_city)
                end_time = time.time()
            case "iddfs":
                max_depth = int(input("Enter the maximum depth: "))
                start_time = time.time()
                path = iddfs(adjacency_dict, start_city, goal_city, max_depth)
                end_time = time.time()
            case "best first search":
                start_time = time.time()
                path = best_first_search(adjacency_dict, start_city, goal_city, calculate_distance)
                end_time = time.time()
            case "a*":
                start_time = time.time()
                path = a_star_search(adjacency_dict, start_city, goal_city, calculate_distance)
                end_time = time.time()
            
        if path: # if theres a path, print it to console with colors so the important info is easier to see
            print(COLOR["BLUE"], end="")
            print(f"\nPath from {start_city} to {goal_city} using {COLOR["RED"]}{search_algo}{COLOR["ENDC"]}:")
            print(" -> ".join(path), f"takes a total of {COLOR["BLUE"]}{calculate_route_distance(path)}{COLOR["ENDC"]} km")
            print(COLOR["ENDC"], end="")
            print(f"Time taken: {COLOR["GREEN"]}{(end_time - start_time) * 1_000_000:.2f}{COLOR["ENDC"]} microseconds")
            create_map.main(get_cities(path))  # launch the gui displaying the path
        else:
            print(f"No path found from {COLOR["BLUE"]}{start_city}{COLOR["ENDC"]} to {COLOR["BLUE"]}{goal_city}{COLOR["ENDC"]} using {COLOR['RED']}{search_algo}{COLOR['ENDC']}.")

        again = input("Would you like to try again? (y/n): ").strip().lower()

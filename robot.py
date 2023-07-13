import threading, time

# Global variables
room = []
robots = []
initial_positions = []
room_dim = 0
cleaned_cells = 0
num_robots = 0
collision =False
collision_cell = None
lock = threading.Lock()

# Function to read room dimensions from file
def read_room_dimensions():
    global room_dim
    with open("room.txt", "r") as room_file:
        room_dim = int(room_file.readline().strip())

# Function to read robot positions and directions from file
def read_robot_positions():
    global robots, initial_positions, num_robots
    try:
        with open("robots.txt", "r") as robots_file:
            num_robots = int(robots_file.readline().strip())
            center  = room_dim // 2
            robots.append({
                "position": (center, center),
                "direction": "U",
                "step_count": 1,
                "step_limit": 1,
                "state": 0
            })
            initial_positions.append((center, center))

            for _ in range(num_robots - 1):
                *position, direction = robots_file.readline().strip().split()
                x = int(position[0])
                y = int(position[1])
                if (x, y) not in initial_positions:
                    initial_positions.append((x, y))
                    robots.append({
                        "position": (x, y),
                        "direction": direction,
                        "step_count": 1,
                        "step_limit": 1,
                        "state": 0
                    })
                else:
                    print("INPUT ERROR")
                    raise Exception
    except:
        raise ValueError

# Function to initialize the room grid
def initialize_room():
    global room, robots, initial_positions, room_dim
    room = [[0] * room_dim for _ in range(room_dim)]
    room[room_dim//2][room_dim//2] = 1

# Function to check if a cell is clean
def is_cell_clean(x, y):
    return room[x][y] == 1

# Function to mark a cell as clean
def mark_cell_clean(x, y):
    global cleaned_cells, room, robots
    try:
        if not is_cell_clean(x, y):
            with lock:
                room[x][y] = 1
                cleaned_cells += 1
    except:
        raise Exception

def checkCollision(x,y):
    try:
        global robots
        item = (x,y)
        count = 0
        for items in robots:
            if items.get("position") == item:
                count +=1
        if count == 1:
            return True
        return False
    except:
        raise Exception
    
# Function to handle collision
def handle_collision(x, y):
    try:
        global collision, collision_cell
        collision = True
        collision_cell = (x, y)
    except:
        raise Exception
# Function to simulate the movement of a robot vacuum
def simulate_robot_vacuum(robot):
    global room_dim
    bool_count = False
    counter = 0
    try:
        while not collision and cleaned_cells < room_dim * room_dim:
            x = robot["position"][0]
            y = robot["position"][1]
            direction = robot["direction"]
            step_count = robot["step_count"]
            step_limit = robot["step_limit"]

            # Check if the robot is at the boundary
            if x == 0 or x == room_dim - 1 or y == 0 or y == room_dim - 1:
                if x == 0  and y == 0:
                    if direction == "R":
                        y += 1
                    else:
                        direction == "D"
                        x += 1
                elif x == 0 and y == room_dim - 1:
                    if direction == "L":
                        y -= 1
                    elif direction == "D":
                        x += 1
                    else:
                        direction = "L"
                        y -= 1
                elif x == room_dim - 1 and y == 0:
                    if direction == "R":
                        y += 1
                    elif direction == "U":
                        x -= 1
                    else:
                        direction = "R"
                        y += 1
                elif x == room_dim - 1 and y == room_dim - 1:
                    if direction == "L":
                        y -= 1
                    elif direction == "U":
                        x -= 1
                    else:
                        direction = "U"
                        x -= 1
                elif x == 0 and 0 < y < room_dim - 1:
                    if direction in ("U", "L"):
                        direction = "L"
                        y -= 1
                    elif direction == "R":
                        y += 1
                    elif direction == "D":
                        x += 1
                elif  0 < x < room_dim - 1 and y == 0:
                    if direction in ("L", "D"):
                        direction = "D"
                        x += 1
                    elif direction == "U":
                        x -= 1
                    elif direction == "R":
                        y += 1
                elif x == room_dim -1 and 0 < y < room_dim - 1:
                    if direction in ("D", "R"):
                        direction = "R"
                        y += 1
                    elif direction == "U":
                        x -= 1
                    elif direction == "L":
                        y -= 1
                elif 0 < x < room_dim - 1 and y == room_dim - 1:
                    if direction in ("R", "U"):
                        direction = "U"
                        x -= 1
                    elif direction == "L":
                        y -= 1
                    elif direction == "D":
                        x += 1

                # Move in a spiral pattern based on the current direction
            else:
                if step_count == step_limit and bool_count == True:
                    if direction == "R":
                        direction = "U"
                    elif direction == "U":
                        direction = "L"
                    elif direction == "L":
                        direction = "D"
                    else:
                        direction = "R"
                    if direction in ("R", "L") and counter >= 2:
                        step_limit += 1
                    if counter>= 2:
                        step_count = 0

                if direction == "U":
                    x -= 1
                elif direction == "L":
                    y -=1
                elif direction == "D":
                    x += 1
                elif direction == "R":
                    y += 1
                if bool_count == True and counter >= 3:
                    step_count += 1

                bool_count = True
                counter += 1

            if checkCollision(x,y):
                handle_collision(x,y)
                return
                
            # Mark the cell as clean
            mark_cell_clean(x, y)

            # Update the robot's position and direction
            robot["position"] = (x, y)
            robot["direction"] = direction
            robot["step_count"] = step_count
            robot["step_limit"] = step_limit
            # Wait for 2 seconds before the next iteration
            time.sleep(2)
            print("Simulation in progress...\n" if counter % 3 == 0 else "", end= "")
    except:
        raise Exception

# Main function to start the simulation
def start_simulation():
    global room_dim, cleaned_cells, collision, collision_cell, num_robots

    try:
        # Read room dimensions and robot positions
        read_room_dimensions()
        read_robot_positions()

        # Initialize the room and cleaned cells counter
        initialize_room() 
        cleaned_cells = 1

        # Create and start a thread for each robot vacuum
        threads = []
        for robot in robots:
            thread = threading.Thread(target=simulate_robot_vacuum, args=(robot,))
            threads.append(thread)
            thread.start()

        ## Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check simulation result
        if collision:
            print("COLLISION AT CELL", collision_cell)
        elif cleaned_cells == room_dim * room_dim:
            print("ROOM CLEAN")
    except:
        print("Simulation interrupted.")
# Start the simulation
if __name__ == "__main__":
    start_simulation()
# Assigment 2 

## Robot Simulation

## Running the simulation

To run the simulation, run the commands below from the root directory.

```bash
python -m venv venv

venv\Scripts\activate

python robot.py
```

## Code Description
In the simulation, I have implementated the concept of multithreading using Python's threading module.
```bash
        # Create and start a thread for each robot vacuum
        threads = []
        for robot in robots:
            thread = threading.Thread(target=simulate_robot_vacuum, args=(robot,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
```
The snippet above shows how I implemented multithreading by creating and starting a thread for each robot vacuum


Also, to avoid any deadlock situation, I used `threading.lock()` function to access the shared resources (which are the room grid and the variable `clean_cells` which is used to keep count of the number of cells that have been cleaned)

## Sample tests
I have provided a `robot.txt` file and a `room.txt` file which contain sample test case to run. 

Also I have provided a `sample.txt` file for more test samples.

PS: I tried to use Java for the implementation. However, I found it a little challenging mostly due to the fact that I am new to Java and hence the reason for implementing in Python. Hope you understand.
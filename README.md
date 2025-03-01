Project Overview :
    This project simulates a thread pool where multiple worker threads process tasks 
    dynamically submitted from an input file. The simulation logs all events and generates a 
    detailed report at the end.

Project Structure : 

    /threadPool

    |-- main.py                    # Starts the project

    |-- worker.py                  # Runs the simulation 
    
    |-- task_submitter.py          # Submit tasks based arrivlals
    
    |-- pool_manager.py            # Handles dynamic task submission
    
    |-- file_utils.py              # Get data from input file, sort by arrivals
    
    /texts                         # Saving all the .txt files here 
    
        |-- input.txt              # input file

How It Works :

    input.txt, which contains a list of tasks with arrival times and execution
    durations.

    Sorts the tasks by arrival time (file_utils.py).

    Initializes a thread pool with a specified number of worker threads 
    (pool_manager.py).

    Dynamically submits tasks at their scheduled arrival times (task_submitter.py).

    Executes tasks concurrently, logging start & finish times (worker.py).

    Generates a final report summarizing execution details (output.txt).

Running the Code :
    Install dependecies :
        Python 3...
        no pip installation is needed
    Run :
        python main.py



This project is open-source and available for use and modification.
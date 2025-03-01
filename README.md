Project Overview :
    This project simulates a thread pool where multiple worker threads process tasks 
    dynamically submitted from an input file. The simulation logs all events and generates a 
    detailed report at the end.

Project Structure : 
    /threadPool
    |-- worker.py                  # Runs the simulation 
    |-- task_submitter.py          # Worker thread logic
    |-- pool_manager.py            # Handles dynamic task submission
    |-- file_utils.py              # Manages thread pool and reporting
    |-- input.txt                  # Reads & sorts input file

How It Works :
    input.txt, which contains a list of tasks with arrival times and execution
    durations.

    Sorts the tasks by arrival time (file_utils.py).

    Initializes a thread pool with a specified number of worker threads 
    (pool_manager.py).

    Dynamically submits tasks at their scheduled arrival times (task_submitter.py).

    Executes tasks concurrently, logging start & finish times (worker.py).

    Generates a final report summarizing execution details (simulation_report.txt).

Running the Code :
    Install dependecies :
        Python 3...
        no pip installation is needed
    python main.py



This project is open-source and available for use and modification.
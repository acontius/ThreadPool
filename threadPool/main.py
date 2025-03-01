import time
from file_utils import read_and_sort_tasks
from pool_manager import PoolManager
from task_submitter import TaskSubmitter

def main():
    thread_number, tasks = read_and_sort_tasks("input.txt")

    TManager = PoolManager(thread_number)
    TManager.starting()

    submitter = TaskSubmitter(TManager, tasks)
    submitter.start()
    
    submitter.join()
    TManager.waiting()

    simulation_end_time = time.time()
    simulation_time = simulation_end_time - TManager.simulation_start_time

    report = TManager.generate_report(simulation_time, TManager.simulation_start_time, simulation_end_time)
    print("\n" + report)
    print("\n\U0001f4be Report saved to 'simulation_report.txt'!")

if __name__ == "__main__":
    main()

import threading, time
from collections import deque

class Worker(threading.Thread):
    def __init__(self, id, task_order, condition, pool_manager):
        super().__init__()
        self.id = id
        self.task_order = task_order
        self.condition = condition
        self.pool_manager = pool_manager
        self.tasks_completed = 0

    def run(self):
        while True:
            with self.condition:
                while not self.task_order and not self.pool_manager.submission_complete:
                    self.condition.wait()
                if not self.task_order and self.pool_manager.submission_complete:
                    break
                task, _, exec_time = self.task_order.popleft()

            start_time = time.time()
            log_message = f"\u27a4 \U0001f7e2 Thread {self.id} started {task} | Exec time: {exec_time:.2f}s"
            with self.pool_manager.log_lock:
                self.pool_manager.logs.append(log_message)
            print(log_message)

            time.sleep(exec_time)

            finish_time = time.time()
            log_message = f"\u27a4 \u2705 Thread {self.id} finished {task} | Total time: {exec_time:.2f}s"
            with self.pool_manager.log_lock:
                self.pool_manager.logs.append(log_message)
            print(log_message)

            self.tasks_completed += 1

class TaskSubmitter(threading.Thread):
    def __init__(self, pool_manager, tasks):
        super().__init__()
        self.pool_manager = pool_manager
        self.tasks = tasks

    def run(self):
        for task_name, arrival_time, exec_time in self.tasks:
            time.sleep(arrival_time)  
            self.pool_manager.addition((task_name, None, exec_time))

            with self.pool_manager.log_lock:
                self.pool_manager.logs.append(f"\u27a4 Submitted {task_name}")

        self.pool_manager.complete_submission()

class poolManager:
    def __init__(self, thread_number):
        self.threads = []
        self.threads_number = thread_number
        self.task_order = deque()
        self.condition = threading.Condition()
        self.submission_complete = False
        self.logs = []
        self.log_lock = threading.Lock()
        self.simulation_start_time = None  # Track start time

    def addition(self, task_tuple):
        with self.condition:
            self.task_order.append(task_tuple)
            self.condition.notify()

    def starting(self):
        self.simulation_start_time = time.time()  # Start time of the simulation
        for i in range(self.threads_number):
            worker = Worker(i + 1, self.task_order, self.condition, self)
            self.threads.append(worker)
            worker.start()

    def waiting(self):
        for thread in self.threads:
            thread.join()

    def complete_submission(self):
        with self.condition:
            self.submission_complete = True
            self.condition.notify_all()

    def generate_report(self, simulation_time, start_time, end_time):
        total_tasks = sum(worker.tasks_completed for worker in self.threads)
        unused_threads = sum(1 for worker in self.threads if worker.tasks_completed == 0)
        avg_exec_time = simulation_time / total_tasks if total_tasks > 0 else 0

        report_lines = [
            "\n" + "=" * 50,
            "\U0001f4ca  SIMULATION REPORT",
            "=" * 50,
            f"\U0001f552  Simulation start time: {time.strftime('%X', time.localtime(start_time))}",
            f"\U0001f552  Simulation end time: {time.strftime('%X', time.localtime(end_time))}",
            f"\U0001f4cc  Total simulation time: {simulation_time:.2f} seconds",
            f"\U0001f9f5  Total threads used: {self.threads_number}",
            f"\U0001f4da  Total tasks processed: {total_tasks}",
            f"\U0001f6ab  Unused threads: {unused_threads}",
            f"\U0001f4c8  Average execution time per task: {avg_exec_time:.2f} seconds",
            "\n\U0001f4dc  EVENT LOGS:",
            "-" * 50
        ]
        report_lines.extend(self.logs)
        report_lines.append("=" * 50)

        report_text = "\n".join(report_lines)

        # Save to file
        with open("simulation_report.txt", "w", encoding="utf-8") as f:
            f.write(report_text)

        return report_text

def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

    thread_number = int(lines[0])
    task_count = int(lines[1])
    
    tasks = []
    for i in range(2, 2 + task_count):
        parts = lines[i].split()
        task_name = parts[0]
        arrival_time = float(parts[1])
        exec_time = float(parts[2])
        tasks.append((task_name, arrival_time, exec_time))

    tasks.sort(key=lambda x: x[1])

    TManager = poolManager(thread_number)
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

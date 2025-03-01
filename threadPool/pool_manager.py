import threading, time
from collections import deque
from worker import Worker

class PoolManager:
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
        self.simulation_start_time = time.time()  # Start simulation time
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
            "\U0001f4ca SIMULATION REPORT",
            "=" * 50,
            f"\U0001f552 Simulation start time: {time.strftime('%X', time.localtime(start_time))}",
            f"\U0001f552 Simulation end time: {time.strftime('%X', time.localtime(end_time))}",
            f"\U0001f4cc Total simulation time: {simulation_time:.2f} seconds",
            f"\U0001f9f5 Total threads used: {self.threads_number}",
            f"\U0001f4da Total tasks processed: {total_tasks}",
            f"\U0001f6ab Unused threads: {unused_threads}",
            f"\U0001f4c8 Average execution time per task: {avg_exec_time:.2f} seconds",
            "\n\U0001f4dc EVENT LOGS:",
            "-" * 50
        ]
        report_lines.extend(self.logs)
        report_lines.append("=" * 50)

        report_text = "\n".join(report_lines)

        with open("simulation_report.txt", "w", encoding="utf-8") as f:
            f.write(report_text)

        return report_text

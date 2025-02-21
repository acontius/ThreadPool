import threading, time
from collections import deque

duration = 2

class Worker(threading.Thread):
    def __init__(self, id, task_order, lock):
        super().__init__()
        self.id = id
        self.task_order = task_order
        self.lock = lock

    def run(self):
        while True:
            with self.lock:  # Ensure only one thread can access the queue at a time
                if not self.task_order:
                    break
                task = self.task_order.popleft()  # Pop task from the queue
                print(f"Thread {self.id} has started on task: {task}!")
                time.sleep(duration)
                print(f"Thread {self.id} has finished task: {task}!")


class poolManager:
    def __init__(self, thread_number):
        self.threads = []
        self.threads_number = thread_number
        self.task_order = deque()  # Shared task queue
        self.lock = threading.Lock()  # Lock to ensure thread-safe access to task queue

    def addition(self, task):
        self.task_order.append(task)

    def starting(self):
        for i in range(self.threads_number):
            worker = Worker(i + 1, self.task_order, self.lock)  # Pass lock and task_order to each worker
            self.threads.append(worker)
            worker.start()

    def waiting(self):
        for thread in self.threads:
            thread.join()


def main():
    Threads_numbers = int(input("Enter the number of Threads: "))
    tasks_numbers = int(input("Enter the number of Tasks: "))

    TManager = poolManager(Threads_numbers)

    for Task_id in range(1, tasks_numbers + 1):  # Start from 1 to tasks_numbers
        TManager.addition(f"Task {Task_id}")

    TManager.starting()
    TManager.waiting()

    print("\nAll done")


if "__main__" == __name__:
    main()

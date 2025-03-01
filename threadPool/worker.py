import threading, time

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
            log_message = f"\u27a1\ufe0f \U0001f7e2 Thread {self.id} started {task} | Exec time: {exec_time:.2f}s"
            with self.pool_manager.log_lock:
                self.pool_manager.logs.append(log_message)
            print(log_message)

            time.sleep(exec_time)

            finish_time = time.time()
            log_message = f"\u27a1\ufe0f \u2705 Thread {self.id} finished {task} | Total time: {exec_time:.2f}s"
            with self.pool_manager.log_lock:
                self.pool_manager.logs.append(log_message)
            print(log_message)

            self.tasks_completed += 1

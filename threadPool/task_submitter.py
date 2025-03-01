import threading, time

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
                self.pool_manager.logs.append(f"\u27a1\ufe0f Submitted {task_name}")

        self.pool_manager.complete_submission()

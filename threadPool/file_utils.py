def read_and_sort_tasks(file_path):
    with open(file_path, "r") as f:
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

    return thread_number, tasks

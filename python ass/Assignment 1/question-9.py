
import threading
import time
import queue

jobs = [
    (2, 1, "Job A", 2),
    (1, 2, "Job B", 3),
    (1, 3, "Job C", 1),
    (3, 4, "Job D", 2),
]

job_queue = queue.PriorityQueue()
lock = threading.Lock()
results = []
start_time = time.time()


for priority, arrival, name, duration in jobs:
    job_queue.put((priority, arrival, name, duration))

def worker(worker_name):
    while not job_queue.empty():
        with lock:
            if job_queue.empty():
                return
            priority, arrival, name, duration = job_queue.get()

        start = time.time() - start_time
        print(worker_name, "started", name)

        time.sleep(duration)

        finish = time.time() - start_time
        waiting = start - arrival

        with lock:
            results.append(
                (name, worker_name, start, finish, waiting)
            )
            print(worker_name, "finished", name)

        job_queue.task_done()

workers = [
    threading.Thread(target=worker, args=("Worker 1",)),
    threading.Thread(target=worker, args=("Worker 2",))
]

for w in workers:
    w.start()

for w in workers:
    w.join()

print("\nJob Details")
for name, worker, start, finish, waiting in sorted(results):
    print(name, "|", worker,
          "| Start:", round(start, 2),
          "| Finish:", round(finish, 2))

avg_wait = sum(r[4] for r in results) / len(results)
print("Average Waiting Time:", round(avg_wait, 2), "seconds")

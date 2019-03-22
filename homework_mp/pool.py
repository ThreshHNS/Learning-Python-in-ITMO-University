import psutil
from multiprocessing import Queue, Process
import time


class ProcessPool:
    def __init__(self, min_workers=2, max_workers=10, mem_usage=1024):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.proc_mem = Queue()

    def proc_mem_calc(self, func, data):
        proc_test = Process(target=func, args=(data, True))
        proc_test.start()
        proc_watcher = Process(target=self.peak_mem_usage, args=(proc_test.pid, self.proc_mem))
        proc_watcher.start()
        proc_test.join()
        proc_watcher.join()
        self.proc_mem = self.proc_mem.get()

    def peak_mem_usage(self, pid, return_dict):
        max_ram = 0
        try:
            while psutil.pid_exists(pid):
                result = psutil.Process(pid).memory_info().rss / 2 ** 20
                if result > max_ram:
                    max_ram = result
        except psutil.NoSuchProcess:
            pass
        self.proc_mem.put(max_ram)

    def map(self, func, img_queue: Queue):
        self.proc_mem_calc(func, img_queue.get())
        print(f"✔ The process takes {int(self.proc_mem)} MB of memory.")
        max_procs = int(self.mem_usage / self.proc_mem)
        print(f"• Maximum number of processes - {max_procs}")

        procs = []

        if max_procs > self.max_workers:
            max_procs = self.max_workers
        elif max_procs < self.min_workers:
            raise Exception('✘ Not enough RAM to compress images! Check your settings.')

        start_time = time.clock()

        print(f"\n• Compressing and resizing image files:")
        for i in range(max_procs):
            if img_queue.qsize() == 0:
                break
            proc = Process(target=func, args=(img_queue.get(),))
            procs.append(proc)
            proc.start()

        while not img_queue.empty():
            for i, proc in enumerate(procs):
                if not proc.is_alive():
                    new_proc = Process(target=func, args=(img_queue.get(),))
                    new_proc.start()
                    procs[i] = new_proc

        for proc in procs:
            proc.join()

        proc_time = time.clock() - start_time
        print(f"\n✔ The task was completed in {proc_time} sec")

        return max_procs, self.proc_mem

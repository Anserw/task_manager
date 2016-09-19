import os
import time
import threading
import logging

class TestThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
        self.is_waiting = True
        self.thread_stop = False
        self.work_path = None
        self.task_command = None

    def run(self):
        while not self.thread_stop:
            if self.is_waiting:
                time.sleep(0.1)
            else:
                logging.info('cd ' + self.work_path + ' ; ' + self.task_command + ' > log.log')
                os.system('cd ' + self.work_path + ' ; ' + self.task_command + ' > log.log')
                self.is_waiting = True

    def set_task(self, work_path, task_command):
        self.work_path = work_path
        self.task_command = task_command
        self.is_waiting = False
        logging.info("task assigned")

    def waiting(self):
        return self.is_waiting

    def stop(self):
        logging.info("thread stop")
        self.thread_stop = True


def preprocess(task_list):
    path = task_list[0][1]
    task_name = task_list[0][0]
    work_dir = os.path.join(path, task_name)
    if not os.path.isdir(work_dir):
        logging.info("making dir: " + work_dir)
        os.makedirs(work_dir)
    else:
        logging.warning(work_dir + " already exits")
    os.chdir(work_dir)



def start_engine(task_list, thread_sum):
    thread_pool = [TestThread(i) for i in range(thread_sum)]
    for a_thread in thread_pool:
        a_thread.start()
    task_sum = len(task_list)
    logging.info("Total tasks: %d" % task_sum)
    logging.info("Thread sum: %d" % thread_sum)

    task_done = 0
    for a_task in task_list:
        done = False
        dir_name = os.path.join(a_task[1], a_task[0]) + '/'
        cmd = ''
        for i in range(2, len(a_task)):
            dir_name += os.path.basename(a_task[i]) + '_'
            cmd += a_task[i] + ' '
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        while not done:
            for thread_i in range(thread_sum):
                if thread_pool[thread_i].waiting():
                    thread_pool[thread_i].set_task(dir_name, cmd)
                    done = True
                    task_done += 1
                    logging.info("[%2d%%] Running " % int(100*task_done/task_sum) + cmd)
                    break
            if not done:
                time.sleep(0.1)
    for a_thread in thread_pool:
        while not a_thread.waiting():
            time.sleep(0.1)
        a_thread.stop()

def run_all_tasks(task_list, thread_sum = 4):
    if len(task_list) <= 0 or len(task_list[0]) <=2:
        return
    preprocess(task_list)
    start_engine(task_list, thread_sum)


import common
import logging
import argparse
import json
import framework
import time

def generate_task_list(tasklist, option):
    if "type" not in option or "list" not in option:
        print "Error"
        return
    else:
        if option["type"] == "cross":
            new_task_list = []
            for a_new_filed in option["list"]:
                for a_task in tasklist:
                    new_task_list.append(a_task + [a_new_filed["value"]])
            return new_task_list
        elif option["type"] == "step":
            new_task_list = []
            len_tasklist = len(tasklist)
            len_option_list = len(option["list"])
            new_len = max(len_tasklist, len_option_list)
            for i in range(new_len):
                new_task_list.append(tasklist[i % len_tasklist] + [option["list"][i % len_option_list]["value"]])
            return new_task_list


if __name__ == '__main__':
    common.set_log_format()
    logging.info("start")
    parser = argparse.ArgumentParser(description="Assign task for a user based on the data in DB.")

    parser.add_argument("-w", "--workpath", type=str, help="work path")
    parser.add_argument("-i", "--interpreter", type=str, help="interpreter such as python")
    parser.add_argument("-t", "--task", type=str, help="binary file or script")
    parser.add_argument("-c", "--config", type=str, help="config file")


    args = parser.parse_args()

    tasks = [[""]]
    if args.config:
        logging.info("config file: " + args.config)
        config = json.load(open(args.config, 'r'))
        tasks = [[config["name"]]]
        logging.info("task name: " + config["name"])
        tasks = generate_task_list(tasks, config["workpath"])
        tasks = generate_task_list(tasks, config["interpreter"])
        tasks = generate_task_list(tasks, config["task"])
        for a_args in config["args"]["list"]:
            tasks = generate_task_list(tasks, a_args)
        for a_task in tasks:
            a_task
        framework.run_all_tasks(tasks, 8)
    logging.info("complete.")
import common
import logging
import argparse
import json

if __name__ == '__main__':
    common.set_log_format()
    parser = argparse.ArgumentParser(description="Assign task for a user based on the data in DB.")

    parser.add_argument("-w", "--workpath", type=str, help="work path")
    parser.add_argument("-i", "--interpreter", type=str, help="interpreter such as python")
    parser.add_argument("-t", "--task", type=str, help="binary file or script")
    parser.add_argument("-c", "--config", type=str, help="config file")


    args = parser.parse_args()

    if args.config:
        print args.config
        config = json.load(open(args.config, 'r').read())
        print config

    # if args.sum and args.dir:
    #     gen_task(args.sum, target_dir=args.dir)
#!/usr/bin/env python3

import subprocess
import time
from pathlib import Path
import json
import sys
import socketserver
import csv
import numpy as np
import argparse
from sim_pkg.config import Configuration

robot_processes_ = []
parser = argparse.ArgumentParser(description='Run the simulator')

parser.add_argument('-fn', '--filename', type=str,
                    help="Name of the file without the .py extension")

args = parser.parse_args()

def run():
    """
    Opens all the programs involved
    """

    # Read required parameters from config.json
    config = Configuration.from_path('config.json')  # Shouldn't be hardcoded.
    path = str(Path(__file__).parent)
    
    # Open the simulator in a process
    sim_process_ = subprocess.Popen(['python3','-O', 'simulator.py'],close_fds=True,cwd=path)
    time.sleep(1)

    # Open all the robots
    for i in range(config.num_robots):
        r_process = subprocess.Popen(['python2','-O', 'bootloader.py', '-fn', args.filename],close_fds=True,cwd=path)
        robot_processes_.append(r_process)
    # subprocess.Popen(['python2','user2.py'],close_fds=True,cwd=path)
    
    if config.use_visualizer:
        vis_processes_ = subprocess.Popen(['python3','-O','visualization.py'],close_fds=True,cwd=path)
    else:
        vis_processes_ = -1 

    return sim_process_, robot_processes_, vis_processes_

def main():
    """
    Opens all programs and then when program is killed, kills all the processes cleanly
    """
    sim_process, robot_processes, vis_process = run()
    
    try:
        # pass
        sim_process.wait()
        for process in robot_processes:
            process.wait()
        vis_process.wait()

    except KeyboardInterrupt:
        # Kill the processes. Currently kills the robot subprocess and
        # everything seems to die. subprocess.poll 
        for process in robot_processes:
            subprocess.Popen.terminate(process)
            stdout, stderr = process.communicate()

        subprocess.Popen.terminate(sim_process)
        if vis_process != -1:
            try:
                subprocess.Popen.terminate(vis_process)
            except:
                pass

        print('Interrupted')
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())

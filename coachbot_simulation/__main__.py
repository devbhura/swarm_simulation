#!/usr/bin/env python3

import subprocess
import time
from pathlib import Path
import sys
import os
import argparse
from typing import List, Optional, Tuple
from coachbot_simulation.config import Configuration

def run() -> Tuple[subprocess.Popen, List[subprocess.Popen],
                   Optional[subprocess.Popen]]:
    """Opens all the programs involved."""

    parser = argparse.ArgumentParser(description='Run the simulator')
    parser.add_argument('-fn', '--filename', type=str,
                        help="Name of the file without the .py extension")
    parser.add_argument('-c', '--config', type=str, default='config.json',
                        help='Path to configuration file.')
    args = parser.parse_args()
    config = Configuration.from_path(os.path.abspath(args.config))
    
    # Start simulator
    sim_process = subprocess.Popen(
        ['python3', '-O', '-m', 'coachbot_simulator.simulator', '-c', args.config],
        close_fds=True
    )
    time.sleep(1)  # TODO: Remove, waiting for what you need to wait for.

    # Start robot processes.
    robot_processes = [
        subprocess.Popen(['python2', '-O', '-m', 'coachbot_emulator2', '-fn',
                          args.filename], close_fds=True)
        for _ in range(config.num_robots)
    ]

    vis_process = (
        subprocess.Popen(['python', '-O', 'visualization.py'],
                         close_fds=True)
        if config.use_visualizer
        else None
    )

    return sim_process, robot_processes, vis_process

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
        if vis_process is not None:
            vis_process.wait()

    except KeyboardInterrupt:
        # Kill the processes. Currently kills the robot subprocess and
        # everything seems to die. subprocess.poll 
        for process in robot_processes:
            subprocess.Popen.terminate(process)
            stdout, stderr = process.communicate()

        subprocess.Popen.terminate(sim_process)
        if vis_process is not None:
            try:
                subprocess.Popen.terminate(vis_process)
            except:
                pass

        print('Interrupted')
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())

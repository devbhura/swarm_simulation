from dataclasses import dataclass, field
import json
from math import pi
from random import random
from typing import Tuple
import functools
import numpy as np


@dataclass
class Configuration:
    """Represents the initial configuration for the simulation.

    Attributes:
        comm_range: The maximum range in meters before all p2p packets are
                    dropped.
        packet_pass_rate: A 0-1 value representing the number of packets that
                          successfully passed to other robots.
        num_robots: The total number of robots in a simulation
        msg_buffer_size: The total number of messages that are stored in the
                         coachbot buffer.
        arena_length: The length of the arena in meters.
        arena_width: The width of the arena in meters.
        server_port: The port on which the server is operating.
        time_is_synced: Whether the robot time is synchronized on init.
        use_init_pos: Whether initial positions are read from a file.
        sim_time_step: The simulation time step in seconds
        use_visualizer: Whether the visualizer is used.
        real_time_factor: The target slowdown of simulated time to real time.
        max_motor_speed: The maximum motor speed in radians
        robot_radius: The robot radius
    """
    comm_range: float
    packet_pass_rate: float
    num_robots: int
    msg_buffer_size: int
    arena_length: float
    arena_width: float
    server_port: int
    time_is_synced: bool
    use_init_pos: bool
    sim_time_step: float
    use_visualizer: bool
    real_time_factor: float

    max_motor_speed: float = field(default=180.0 * 2 * pi / 60.0)
    robot_radius: float = field(default=(0.105 / 2.0))

    @functools.cached_property
    def robot_diameter(self) -> float:
        return self.robot_radius * 2.0

    @functools.cached_property  # Prevent re-calculation
    def _initial_positions(self) -> np.ndarray:
        # TODO: This should not use a hard coded path
        return np.genfromtxt('init.csv', delimiter=',')

    def get_inital_pos_for_robot(self,
                                 bot_id: int) -> Tuple[float, float, float]:
        """Returns the user-configured initial position of a robot.

        Returns:
            Tuple[float, float, float] - The inital x,y,theta positions.
        """
        if self.use_init_pos:
            return (
                self._initial_positions[bot_id][1],
                self._initial_positions[bot_id][2],
                self._initial_positions[bot_id][3]
            )
        else:
            abs_x_bound = (self.arena_width - 0.1) / 2
            abs_y_bound = (self.arena_length - 0.1) / 2
            return (
                random.uniform(-abs_x_bound, abs_x_bound),
                random.uniform(-abs_y_bound, abs_y_bound),
                0
            )

    @staticmethod
    def from_path(path: str) -> 'Configuration':
        """Creates a configuration object from a given path."""

        with open(path, 'r') as config_file:
            as_json = json.load(config_file)

            return Configuration(
                comm_range=as_json['COMM_RANGE'],
                packet_pass_rate=as_json['PACKET_SUCCESS_RATE'],
                num_robots=as_json['NUMBER_OF_ROBOTS'],
                msg_buffer_size=as_json['NUM_OF_MSGS'],
                arena_width=as_json['WIDTH'],
                arena_length=as_json['LENGTH'],
                server_port=as_json['SERVER_PORT'],
                time_is_synced=(not as_json['TIME_ASYNC']),
                use_init_pos=as_json['USE_INIT_POS'],
                sim_time_step=as_json['SIM_TIME_STEP'],
                use_visualizer=as_json['USE_VIS'],
                real_time_factor=as_json['REAL_TIME_FACTOR'],
            )

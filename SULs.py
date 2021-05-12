from aalpy.base import SUL
from Systems import DifferentialDriveRobot

faults = ['left_faster', 'left_slower', 'left_stuck', 'right_faster', 'right_slower', 'right_stuck']
wheel_inputs = [(0, 0), (0, 2), (0, -2), (2, 0), (2, 2), (2, -2), (-2, 0), (-2, 2), (-2, -2)]


class StrongFaultRobot(SUL):
    def __init__(self, upper_speed_limit=10):
        super().__init__()
        self.robot = DifferentialDriveRobot(upper_speed_limit=upper_speed_limit)

    def pre(self):
        self.robot.left_speed = 0
        self.robot.right_speed = 0

    def post(self):
        self.robot.reset_faults()

    def step(self, letter):
        if not isinstance(letter, (tuple, list)):
            self.robot.inject_fault(letter)
            return self.robot.get_heading_direction()
        self.robot.change_speed(letter[0], letter[1])
        return self.robot.get_heading_direction()

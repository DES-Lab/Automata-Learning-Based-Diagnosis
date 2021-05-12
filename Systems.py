class DifferentialDriveRobot:
    def __init__(self, lower_speed_limit=0, upper_speed_limit=10, stochastic_fault_prob=None):
        self.lower_speed_limit = lower_speed_limit
        self.upper_speed_limit = upper_speed_limit
        self.left_speed = 0
        self.right_speed = 0
        self.left_fault = None
        self.right_fault = None
        self.faults = ['left_faster', 'left_slower', 'left_stuck', 'right_faster', 'right_slower', 'right_stuck']

    def reset_faults(self):
        self.left_fault = None
        self.right_fault = None

    def change_speed(self, left_change=0, right_change=0):
        left_change, right_change = self.speed_after_faults(left_change, right_change)

        self.left_speed += left_change
        self.right_speed += right_change

        self.left_speed = max(self.lower_speed_limit, min(self.left_speed, self.upper_speed_limit))
        self.right_speed = max(self.lower_speed_limit, min(self.right_speed, self.upper_speed_limit))

    def get_heading_direction(self):
        if self.left_speed > self.right_speed:
            return 'RIGHT'
        elif self.right_speed > self.left_speed:
            return 'LEFT'
        elif self.left_speed == 0 and self.right_speed == 0:
            return 'STILL'
        else:
            return 'STRAIGHT'

    def inject_fault(self, fault):
        assert fault in self.faults
        if 'left' in fault and self.left_fault is None:
            self.left_fault = fault
            return 'FaultInjected'
        elif self.right_fault is None:
            self.right_fault = fault
            return 'FaultInjected'
        return "-"

    def speed_after_faults(self, left_speed, right_speed):
        if 'left_faster' == self.left_speed:
            left_speed += 2
        if 'left_slower' == self.left_speed:
            left_speed -= 2
        if 'left_stuck' == self.left_speed:
            left_speed = -self.left_speed

        if 'right_faster' == self.right_fault:
            right_speed += 2
        if 'right_slower' == self.right_fault:
            right_speed -= 2
        if 'right_stuck' == self.right_fault:
            right_speed = -self.right_speed

        return left_speed, right_speed

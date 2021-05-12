from aalpy.base import SUL
from Systems import DifferentialDriveRobot, WindTurbine, LightSwitch, GearBox


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


class TurbineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.turbine = WindTurbine()

    def pre(self):
        self.turbine.reset()

    def post(self):
        pass

    def step(self, letter):
        # fault
        if 'unexpected' in letter:
            return self.turbine.inject_fault(letter)
        elif letter == 'stop_turbine':
            self.turbine.stop_turbine()
        else:
            self.turbine.update_spin_speed()

        return self.turbine.get_turbine_speed()


class LightSwitchSUL(SUL):
    def __init__(self):
        super().__init__()
        self.light_switch = LightSwitch()

    def pre(self):
        self.light_switch.reset()

    def post(self):
        pass

    def step(self, letter):
        if letter == 'press':
            self.light_switch.press_switch()
        if letter == 'increase_delay':
            self.light_switch.increase_delay()
        if letter == 'fix_delay':
            self.light_switch.fix_delay()
        return self.light_switch.get_status()


class GearBoxSUL(SUL):
    def __init__(self):
        super().__init__()
        self.gearbox = GearBox()

    def pre(self):
        self.gearbox.reset()

    def post(self):
        pass

    def step(self, letter):
        if letter == 'press_clutch':
            return self.gearbox.press_clutch()
        elif letter == 'release_clutch':
            return self.gearbox.release_clutch()
        elif letter == 'put_in_reverse':
            return self.gearbox.put_in_reverse()
        elif letter == 'increase_gear':
            return self.gearbox.increase_gear()
        else:
            return self.gearbox.decrease_gear()

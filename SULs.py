from aalpy.base import SUL
from Systems import DifferentialDriveRobot, WindTurbine, LightSwitch, GearBox, VendingMachine, Crossroad


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


class VendingMachineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.vending_machine = VendingMachine()
        self.alphabet = ['add_coin_0.2', 'add_coin_0.5', 'add_coin_1', 'get_coke', 'get_water', 'get_peanuts']

    def pre(self):
        self.vending_machine.reset()

    def post(self):
        pass

    def step(self, letter):
        if 'add_coin' in letter:
            return self.vending_machine.add_coin(float(letter.split('_')[-1]))
        else:
            return self.vending_machine.get_product(letter.split('_')[-1])


class CrossroadSUL(SUL):
    def __init__(self):
        super().__init__()
        self.crossroad = Crossroad()
        self.alphabet = ['pedestrian_NS', 'pedestrian_EW', 'traffic_NS', 'traffic_EW']

    def pre(self):
        self.crossroad = Crossroad()

    def post(self):
        pass

    def step(self, letter):
        if 'pedestrian' in letter:
            return self.crossroad.pedestrian_button(letter.split('_')[-1])
        else:
            return self.crossroad.car_arriving(letter.split('_')[-1])

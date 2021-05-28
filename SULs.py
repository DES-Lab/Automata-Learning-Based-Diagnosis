from aalpy.base import SUL
from Systems import DifferentialDriveRobot, WindTurbine, LightSwitch, GearBox, VendingMachine, \
    Crossroad, StochasticLightSwitch, DeterministicCoffeeMachine, StochasticCoffeeMachine, \
    DeterministicFaultInjectedCoffeeMachine, DeterministicCoffeeMachineDFA


# All systems are wrapped in the System Under Learning class
# It defines a step operation on a system (a single action) and a reset (pre and post)

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
            return self.robot.inject_fault(letter)
            # return self.robot.get_heading_direction()
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
            out = self.gearbox.press_clutch()
        elif letter == 'release_clutch':
            out = self.gearbox.release_clutch()
        elif letter == 'put_in_reverse':
            out = self.gearbox.put_in_reverse()
        elif letter == 'increase_gear':
            out = self.gearbox.increase_gear()
        else:
            out = self.gearbox.decrease_gear()
        return out


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
        self.full_alphabet = ['pedestrian_NS', 'pedestrian_EW',
                              'traffic_NS', 'traffic_EW', 'waiting', 'fault_button',
                              'fault_sensor_ns', 'fault_sensor_ew']
        self.full_non_faulty_alphabet = ['pedestrian_NS', 'pedestrian_EW',
                                         'traffic_NS', 'traffic_EW', 'waiting']
        self.alphabet = ['traffic_NS', 'traffic_EW', 'waiting',
                         'fault_sensor_ns', 'fault_sensor_ew']
        self.non_faulty_alphabet = ['traffic_NS', 'traffic_EW', 'waiting']

    def pre(self):
        self.crossroad = Crossroad()

    def post(self):
        pass

    def step(self, letter):
        if 'fault_button' == letter:
            return self.crossroad.inject_fault_in_button()
        elif 'fault_sensor_ns' == letter:
            return self.crossroad.inject_fault_in_sensor_ns()
        elif 'fault_sensor_ew' == letter:
            return self.crossroad.inject_fault_in_sensor_ew()
        elif 'waiting' == letter:
            return self.crossroad.waiting()
        elif 'pedestrian' in letter:
            return self.crossroad.pedestrian_button(letter.split('_')[-1])
        else:
            return self.crossroad.car_arriving(letter.split('_')[-1])


class StochasticLightSUL(SUL):
    def __init__(self):
        super().__init__()
        self.light_switch = StochasticLightSwitch()

    def pre(self):
        self.light_switch.reset()

    def post(self):
        pass

    def step(self, letter):
        return self.light_switch.press() if letter == 'press' else self.light_switch.release()


class FaultyCoffeeMachineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = DeterministicCoffeeMachine(True)

    def pre(self):
        self.coffee_machine.counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()


class FaultyCoffeeMachineSULDFA(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = DeterministicCoffeeMachineDFA()

    def pre(self):
        self.coffee_machine.counter = 0
        self.coffee_machine.correct_counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()


class StochasticCoffeeMachineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = StochasticCoffeeMachine()

    def pre(self):
        self.coffee_machine.counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()


class FaultInjectedCoffeeMachineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = DeterministicFaultInjectedCoffeeMachine()

    def pre(self):
        self.coffee_machine.counter = 0
        self.coffee_machine.fault = None

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        elif letter == 'button':
            return self.coffee_machine.button()
        else:
            return self.coffee_machine.inject_fault(letter)

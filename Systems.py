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


class WindTurbine:
    def __init__(self, spin_speed_limit=6):
        self.state = "INIT"
        self.spin_speed_limit = spin_speed_limit
        self.spin_speed = 0
        self.speed_increment = 1
        self.faults = ['unexpected_speed_increase', 'unexpected_slow_down']
        self.active_fault = False

    def reset(self):
        self.state = "INIT"
        self.spin_speed = 0
        self.speed_increment = 2
        self.active_fault = False

    def update_spin_speed(self):
        self.spin_speed = min(self.spin_speed + self.speed_increment, self.spin_speed_limit)

    def stop_turbine(self):
        self.spin_speed = 0

    def get_turbine_speed(self):
        return self.spin_speed

    def inject_fault(self, fault):
        assert fault in self.faults
        if self.active_fault:
            return "-"
        self.active_fault = True
        if fault == 'unexpected_speed_increase':
            self.speed_increment = min(self.speed_increment + 1, self.spin_speed_limit)
            if self.spin_speed > 0:
                self.update_spin_speed()
        if fault == 'unexpected_slow_down':
            self.speed_increment = max(self.speed_increment - 1, 0)
            if self.spin_speed > 0:
                self.update_spin_speed()

        return self.get_turbine_speed()


class LightSwitch:
    def __init__(self, goal=5):
        self.timer = 0
        self.delay = 0
        self.time_goal = goal

    def reset(self):
        self.timer = 0
        self.delay = 0

    def press_switch(self):
        if self.timer == self.time_goal:
            return
        self.timer += 1 - self.delay
        self.timer = max(min(self.timer, self.time_goal), 0)

    def increase_delay(self):
        self.delay = 1

    def fix_delay(self):
        self.delay = 0

    def get_status(self):
        return "SHINING" if self.timer == self.time_goal else self.timer


class GearBox:
    def __init__(self, num_gears=5):
        self.gear = 1
        self.num_gears = num_gears
        self.faults = []
        self.reverse_fault_counter = 0

        self.clutch_pressed = False
        self.gear_changed = False

    def reset(self):
        self.gear = 1
        self.faults = []
        self.reverse_fault_counter = 0
        self.clutch_pressed = False
        self.gear_changed = False

    def press_clutch(self):
        if not self.clutch_pressed:
            self.clutch_pressed = True
            return 'CLUTCH_PRESSED'
        return 'NO_EFFECT'

    def release_clutch(self):
        if self.clutch_pressed:
            self.clutch_pressed = False
            self.gear_changed = False
            return 'CLUTCH_RELEASED'
        return 'NO_EFFECT'

    def put_in_reverse(self):
        if self.clutch_pressed and not self.gear_changed:
            if self.gear == 1:
                self.gear = -1
                self.gear_changed = True
                return self.gear
            else:
                self.reverse_fault_counter += 1
                if self.reverse_fault_counter >= 2:
                    return "BROKEN"
                return self.gear
        return 'NO_EFFECT'

    def increase_gear(self):
        if self.clutch_pressed and not self.gear_changed:
            self.gear = min(max(self.gear + 1, 1), self.num_gears)
            self.gear_changed = True
            return self.gear
        return 'NO_EFFECT'

    def decrease_gear(self):
        if self.clutch_pressed and not self.gear_changed:
            self.gear = max(self.gear - 1, 1)
            self.gear_changed = True
            return self.gear
        return 'NO_EFFECT'


class VendingMachine:
    def __init__(self):
        self.money_counter = 0
        self.coins = {0.2, 0.5, 1}
        self.products = {'coke', 'water', 'peanuts'}

    def reset(self):
        self.money_counter = 0

    def add_coin(self, coin):
        assert coin in self.coins
        self.money_counter += coin
        if self.money_counter > 2:
            self.money_counter = 2
            return 'MAX_COINS_REACHED'
        return f'COIN_ADDED_{coin}'

    def get_product(self, product):
        assert product in self.products
        if product == 'coke' and self.money_counter >= 1.5:
            self.money_counter -= 1.5
            return 'DROP_COKE'
        elif product == 'water' and self.money_counter >= 0.5:
            self.money_counter -= 0.5
            return 'DROP_WATER'
        elif product == 'peanuts' and self.money_counter >= 1:
            self.money_counter -= 1
            return 'DROP PEANUTS'
        return 'INSUFFICIENT_COINS'

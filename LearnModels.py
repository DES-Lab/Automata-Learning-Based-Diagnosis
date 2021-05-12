from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.utils import visualize_automaton

from SULs import StrongFaultRobot, TurbineSUL, LightSwitchSUL, GearBoxSUL


def learn_diff_drive_robot():
    all_faults = ['left_faster', 'left_slower', 'left_stuck', 'right_faster', 'right_slower', 'right_stuck']

    wheel_inputs = [(0, 0), (0, 2), (2, 0), (2, 2), (0, -2), (2, -2), (-2, 0), (-2, 2), (-2, -2)]

    alphabet = list(wheel_inputs)
    alphabet.extend(all_faults)

    sul = StrongFaultRobot(upper_speed_limit=10)

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    visualize_automaton(learned_model, display_same_state_trans=False)


def learn_wind_turbine():
    alphabet = ['increase_speed', 'stop_turbine', 'unexpected_speed_increase', 'unexpected_slow_down']

    sul = TurbineSUL()

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    visualize_automaton(learned_model, display_same_state_trans=False)


def learn_light_switch():
    alphabet = ['press', 'increase_delay',] # 'fix_delay'

    sul = LightSwitchSUL()

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    visualize_automaton(learned_model, display_same_state_trans=False)

def learn_gearbox():
    alphabet = ['press_clutch', 'release_clutch', 'put_in_reverse', 'increase_gear', 'decrease_gear']

    sul = GearBoxSUL()

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    visualize_automaton(learned_model, display_same_state_trans=False)

if __name__ == '__main__':
    learn_gearbox()
    #learn_wind_turbine()

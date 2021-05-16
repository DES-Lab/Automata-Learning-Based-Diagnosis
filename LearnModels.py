from aalpy.SULs import MealySUL
from aalpy.learning_algs import run_Lstar, run_stochastic_Lstar
from aalpy.oracles import RandomWMethodEqOracle, UnseenOutputRandomWordEqOracle
from aalpy.utils import visualize_automaton, save_automaton_to_file

from SULs import StrongFaultRobot, TurbineSUL, LightSwitchSUL, GearBoxSUL, VendingMachineSUL, CrossroadSUL, \
    StochasticLightSUL


def learn_diff_drive_robot(visualize=False):
    all_faults = ['left_faster', 'left_slower', 'left_stuck', 'right_faster', 'right_slower', 'right_stuck']

    wheel_inputs = [(0, 0), (0, 2), (2, 0), (2, 2), (0, -2), (2, -2), (-2, 0), (-2, 2), (-2, -2)]

    alphabet = list(wheel_inputs)
    alphabet.extend(all_faults)

    sul = StrongFaultRobot(upper_speed_limit=10)

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=False)

    return learned_model


def learn_wind_turbine(visualize=False):
    alphabet = ['increase_speed', 'stop_turbine', 'unexpected_speed_increase', 'unexpected_slow_down']

    sul = TurbineSUL()

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=False)

    return learned_model


def learn_light_switch(visualize=False):
    alphabet = ['press', 'increase_delay', 'fix_delay']  # 'fix_delay'

    sul = LightSwitchSUL()

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='moore')

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=False)

    return learned_model


def learn_gearbox(visualize=False):
    alphabet = ['press_clutch', 'release_clutch', 'put_in_reverse', 'increase_gear', 'decrease_gear']

    sul = GearBoxSUL()

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=20, walk_len=15)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='moore')

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=False)

    return learned_model


def learn_vending_machine(visualize=False):
    sul = VendingMachineSUL()
    alphabet = sul.alphabet

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=50, walk_len=20)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

    # Example of a error
    sul = MealySUL(learned_model)
    print(sul.query(('add_coin_0.2', 'add_coin_0.5', 'add_coin_0.2', 'add_coin_0.2', 'add_coin_0.2', 'add_coin_0.2',)))

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=False)

    return learned_model


def learn_crossroad(visualize=False):
    sul = CrossroadSUL()
    alphabet = sul.alphabet

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=5000, walk_len=20)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=False)

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=False, file_type="dot")

    return learned_model


def learn_stochastic_light_switch(visualize=False):
    sul = StochasticLightSUL()
    alphabet = ['press', 'release']

    eq_oracle = UnseenOutputRandomWordEqOracle(alphabet, sul, num_walks=100, min_walk_len=3, max_walk_len=7)

    learned_model = run_stochastic_Lstar(alphabet, sul, eq_oracle, automaton_type='smm')

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=True)

    return learned_model


if __name__ == '__main__':
    model = learn_crossroad(True)
    print(model)

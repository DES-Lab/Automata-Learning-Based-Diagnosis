![Coffee Machine Example](LearnedModels/header.png)

# Automata Learning Enabling Model-Based Diagnosis

In this repository, we demonstrate how to use active automata learning in order to tackle the problem of creating the diagnostic model. We show how to learn 
deterministic and stochastic models from reactive systems. 

On the one hand, we can learn models of faulty systems for being able to deploy model-based 
reasoning. Furthermore, we also show how to use fault models in the learning process, such as to derive a diagnostic model describing the diagnosis search 
space.

## Structure of the Repo

- `LearnedModels/` - visualized models of faulty systems and their encoding in the .dot format
- `Systems.py` - Simple systems that serve as 'System under Learning'
- `SULs.py` - A wrapper around each system, enabling active automata learning with AALpy
- `ModelLearning.py` - Collections of methods invoking automata learning procedure for each system

## Learned Systems

- *Coffee Machine*
    - Insert a coin, and if 2 or 3 coins are inserted, get a coffee. The cost of coffee is two coins. Several bugs have been introduced. Fault model, the language of faults, stochastic fault model, and model suitable for diagnostic reasoning have been learned. 
- *GearBox*
    - Simple gearbox system where user can press/release the clutch and change gears. 
    Certain sequences of actions can break the gearbox. The fault model and language of faults have been learned.
- *Crossroad System*
    - Crossroads, where two traffic lights control the traffic flow. Each lane can have up to 5 cars in the queue.
- *Vending machine*
    - Simple vending machine where a certain sequence of steps triggers a fault in vending machine logic.
- *Stochastic Lightswitch*
    - Modern light switch that displays faulty behavior in a stochastic manner.
- *Differential Drive Robot*
    - Simple robot with two wheels. Each wheel can be in one of 3 fault modes: spin faster, slower, or stuck. These faults can be injected and a model suitable for diagnostic reasoning constructed.

## Installation and Running
To download:
```bash
git clone https://github.com/DES-Lab/Automata-Learning-Based-Diagnosis
pip install aalpy
```
To run, simply run the `ModelLearning.py`. Select the appropriate method and add it to `__main__` to learn any system.

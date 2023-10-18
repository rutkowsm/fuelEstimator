
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

speed = ctrl.Antecedent(np.arange(0, 101, 1), 'speed')
distance = ctrl.Antecedent(np.arange(0, 1001, 1), 'distance')
engine_power = ctrl.Antecedent(np.arange(0, 251, 1), 'engine_power')
fuel_consumption = ctrl.Consequent(np.arange(0, 21, 1), 'fuel_consumption')

speed['low'] = fuzz.trimf(speed.universe, [0, 20, 40])
speed['medium'] = fuzz.trimf(speed.universe, [30, 50, 70])
speed['high'] = fuzz.trimf(speed.universe, [60, 80, 100])

distance['low'] = fuzz.trimf(distance.universe, [0, 200, 400])
distance['medium'] = fuzz.trimf(distance.universe, [300, 500, 700])
distance['high'] = fuzz.trimf(distance.universe, [600, 800, 1000])

engine_power['low'] = fuzz.trimf(engine_power.universe, [0, 60, 90])
engine_power['medium'] = fuzz.trimf(engine_power.universe, [70, 100, 130])
engine_power['high'] = fuzz.trimf(engine_power.universe, [110, 140, 200])

fuel_consumption['low'] = fuzz.trimf(fuel_consumption.universe, [0, 5, 10])
fuel_consumption['medium'] = fuzz.trimf(fuel_consumption.universe, [7, 11, 15])
fuel_consumption['high'] = fuzz.trimf(fuel_consumption.universe, [12, 17, 20])

rule1 = ctrl.Rule(speed['low'] & distance['low'] & engine_power['low'], fuel_consumption['low'])
rule2 = ctrl.Rule(speed['medium'] & distance['medium'] & engine_power['medium'], fuel_consumption['medium'])
rule3 = ctrl.Rule(speed['high'] & distance['high'] & engine_power['high'], fuel_consumption['high'])

system = ctrl.ControlSystem([rule1, rule2, rule3])

simulation = ctrl.ControlSystemSimulation(system)

simulation.input['speed'] = 20  # Adjusted speed in km/h
simulation.input['distance'] = 100  # Adjusted distance in km
simulation.input['engine_power'] = 60  # Adjusted engine power in kW

simulation.compute()

print(simulation.output['fuel_consumption'])

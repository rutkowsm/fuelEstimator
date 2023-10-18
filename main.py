import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

house_volume = ctrl.Antecedent(np.arange(0, 1001, 1), 'house_volume')
required_temperature = ctrl.Antecedent(np.arange(18, 26, 1), 'required_temperature')
avg_temperature_forecast = ctrl.Antecedent(np.arange(-20, 13, 1), 'avg_temperature_forecast')

gas_needed = ctrl.Consequent(np.arange(0, 101, 1), 'gas_needed')
heat_requirement = ctrl.Consequent(np.arange(0, 101, 1), 'heat_requirement')

# Define membership functions for house_volume
house_volume['small'] = fuzz.trimf(house_volume.universe, [0, 200, 400])
house_volume['medium'] = fuzz.trimf(house_volume.universe, [300, 500, 700])
house_volume['large'] = fuzz.trimf(house_volume.universe, [600, 800, 1000])

# Define membership functions for expected_temperature
required_temperature['cold'] = fuzz.trimf(required_temperature.universe, [18, 20, 22])
required_temperature['medium'] = fuzz.trimf(required_temperature.universe, [21, 23, 24])
required_temperature['warm'] = fuzz.trimf(required_temperature.universe, [23, 24, 25])

avg_temperature_forecast['cold'] = fuzz.trimf(avg_temperature_forecast.universe, [-20, -10, -5])
avg_temperature_forecast['moderate'] = fuzz.trimf(avg_temperature_forecast.universe, [-10, -5, 0])
avg_temperature_forecast['warm'] = fuzz.trimf(avg_temperature_forecast.universe, [-2, 5, 12])


# Define membership functions for gas_needed
gas_needed['low'] = fuzz.trimf(gas_needed.universe, [0, 30, 60])
gas_needed['medium'] = fuzz.trimf(gas_needed.universe, [40, 60, 80])
gas_needed['high'] = fuzz.trimf(gas_needed.universe, [70, 90, 100])

heat_requirement['low'] = fuzz.trimf(heat_requirement.universe, [0, 30, 60])
heat_requirement['medium'] = fuzz.trimf(heat_requirement.universe, [40, 60, 80])
heat_requirement['high'] = fuzz.trimf(heat_requirement.universe, [70, 90, 100])

# Define rules
rule1 = ctrl.Rule(house_volume['small'] & required_temperature['cold'] & avg_temperature_forecast['warm'], heat_requirement['high'])
rule2 = ctrl.Rule(house_volume['medium'] & required_temperature['medium'] & avg_temperature_forecast['moderate'], heat_requirement['medium'])
rule3 = ctrl.Rule(house_volume['large'] & required_temperature['warm'] & avg_temperature_forecast['cold'], heat_requirement['low'])

# Define new rules based on avg_temperature_forecast and heat_requirement
rule4 = ctrl.Rule(avg_temperature_forecast['cold'] & heat_requirement['high'], gas_needed['low'])
rule5 = ctrl.Rule(avg_temperature_forecast['moderate'] & heat_requirement['medium'], gas_needed['medium'])
rule6 = ctrl.Rule(avg_temperature_forecast['warm'] & heat_requirement['low'], gas_needed['high'])


# Create the Control System
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])

# Create a Simulation
simulation = ctrl.ControlSystemSimulation(system)

# Set Input Values
simulation.input['house_volume'] = 800  # Example house volume in m^3
simulation.input['required_temperature'] = 24  # Example expected temperature in °C
simulation.input['avg_temperature_forecast'] = -12  # Example outside temperature in °C

# Perform the Simulation
simulation.compute()

# Access the Output
print(simulation.output['gas_needed'])

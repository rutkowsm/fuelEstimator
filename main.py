"""
Program szacujący potencjalne zużycie gazu ziemnego w sezonie grzewczym
Autorzy:
Rutkowski, Marcin (s12497)
Reinke, Łukasz (s.....)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

"""
Zmienne wejściowe: 
house_volume - kubatura budynku w m3 (min: 150, max: 1000)
required_temperature - oczekiwana temperatura pomieszczeń w stopniach Celsjusza (min: 18, max: 26)
avg_temperature_forecast - prognozowana średnia temperatura w sezonie grzewczym w st. Celsjusza (min: -20, max: 15)
"""
house_volume = ctrl.Antecedent(np.arange(150, 1001, 1), 'house_volume')
required_temperature = ctrl.Antecedent(np.arange(18, 26, 1), 'required_temperature')
avg_temperature_forecast = ctrl.Antecedent(np.arange(-20, 15, 1), 'avg_temperature_forecast')

"""
Zmienna wyjściowa:
gas_needed - ilość gazu potrzebnego w m3 (min: 0, max: 100)
"""
gas_needed = ctrl.Consequent(np.arange(0, 101, 1), 'gas_needed')

"""
Membership functions dla kubatury budynku
"""
house_volume['small'] = fuzz.trimf(house_volume.universe, [0, 200, 400])
house_volume['medium'] = fuzz.trimf(house_volume.universe, [300, 500, 700])
house_volume['large'] = fuzz.trimf(house_volume.universe, [600, 800, 1000])

"""
Membership functions dla oczekiwanej temperatury pomieszczeń
"""
required_temperature['cold'] = fuzz.trimf(required_temperature.universe, [18, 19, 21])
required_temperature['medium'] = fuzz.trimf(required_temperature.universe, [20, 21, 23])
required_temperature['warm'] = fuzz.trimf(required_temperature.universe, [22, 24, 25])

"""
Membership functions dla prognozowanej średniej temperatury
"""
avg_temperature_forecast['cold'] = fuzz.trimf(avg_temperature_forecast.universe, [-20, -12, -8])
avg_temperature_forecast['moderate'] = fuzz.trimf(avg_temperature_forecast.universe, [-11, -5, 0])
avg_temperature_forecast['warm'] = fuzz.trimf(avg_temperature_forecast.universe, [-1, 7, 15])


"""
Membership functions dla zapotrzebowania na gaz
"""
gas_needed['low'] = fuzz.trimf(gas_needed.universe, [0, 30, 60])
gas_needed['medium'] = fuzz.trimf(gas_needed.universe, [40, 60, 80])
gas_needed['high'] = fuzz.trimf(gas_needed.universe, [70, 90, 100])


"""
Rules
"""
rule1 = ctrl.Rule(house_volume['small'] & required_temperature['cold'] & avg_temperature_forecast['warm'], gas_needed['low'])
rule2 = ctrl.Rule(house_volume['medium'] & required_temperature['medium'] & avg_temperature_forecast['moderate'], gas_needed['medium'])
rule3 = ctrl.Rule(house_volume['large'] & required_temperature['warm'] & avg_temperature_forecast['cold'], gas_needed['high'])
rule4 = ctrl.Rule(house_volume['small'] & required_temperature['warm'] & avg_temperature_forecast['moderate'], gas_needed['medium'])
rule5 = ctrl.Rule(house_volume['small'] & required_temperature['medium'] & avg_temperature_forecast['cold'], gas_needed['medium'])
rule6 = ctrl.Rule(house_volume['medium'] & required_temperature['warm'] & avg_temperature_forecast['cold'], gas_needed['medium'])
rule7 = ctrl.Rule(house_volume['medium'] & required_temperature['cold'] & avg_temperature_forecast['warm'], gas_needed['medium'])
rule8 = ctrl.Rule(house_volume['large'] & required_temperature['cold'] & avg_temperature_forecast['moderate'], gas_needed['medium'])
rule9 = ctrl.Rule(house_volume['large'] & required_temperature['medium'] & avg_temperature_forecast['warm'], gas_needed['medium'])
rule10 = ctrl.Rule(house_volume['medium'] & required_temperature['medium'] & avg_temperature_forecast['warm'], gas_needed['medium'])

"""
System kontroli
"""
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])

"""
Symulacja
"""
simulation = ctrl.ControlSystemSimulation(system)

"""
Deklaracja wartości zmiennych wyjściowych
"""
simulation.input['house_volume'] = 450  # Example house volume in m^3
simulation.input['required_temperature'] = 21  # Example expected temperature in °C
simulation.input['avg_temperature_forecast'] = 6  # Example outside temperature in °C

"""
Obliczenie
"""
simulation.compute()

"""
Wywołanie
"""
print(simulation.output['gas_needed'])

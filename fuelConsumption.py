import math
from IPython.display import IFrame
import osmnx as ox, networkx as nx, numpy as np
ox.config(log_console=True, use_cache=True)

### Have a car class in the future and a database for different models with average consumption, mass, etc.
class Car:
    def __init__(self, name, mass, consumptionPerKm):
        self.name = name
        self.mass = mass
        self.consumptionPerKm = consumptionPerKm

### Fuel consumption depends on speed, see graph here:
### https://bit.ly/2PBS4Hg
### approximating that graph here; later add a function that better approximates this
def fuelConsumption(maxspeed=50.0):
    if (maxspeed < 30.0):
        lper100km = 9.0
    elif (maxspeed < 55):
        lper100km = 7.0
    elif (maxspeed < 80.0):
        lper100km = 6.0
    else:
        lper100km = 7.0
    return lper100km


# Fuel consumption when driving along a flat road; input distance in KILOMETERS
def flat(distance = 1.0, consumptionPerKm = 7.0):
    literPerKilometer = consumptionPerKm/100.0
    consumption = literPerKilometer * distance
    return consumption


# Fuel consumption when driving up a hill; input elevation difference between start and finish in METERS, mass of the car and the passengers in KILOGRAMS
def goingUpDown(elevation = 0.1, m = 1500.0):
    g = 9.81
    potentialEnergy = m * g * elevation
    literPerJoule = 1.0 / (32.2 * 1e6)
    consumption = potentialEnergy * literPerJoule / efficiency
    return consumption


#  TOTAL CONSUMPTION = consumption for the "flat" route +- potential energy from going up/downhill
def totalConsumption(distance, elevation, maxspeed = 50.0, mass = 1500.0):
    consumption = fuelConsumption(maxspeed)
    fl = flat(distance, consumption)
    pot = goingUpDown(elevation, mass)
    if ((-1 * pot)>fl):
        total = 0
    else:
        total = fl + pot
    return total

cr = Car("Ford", 1500, 8.9)
efficiency = 0.25  #average engine efficiency for gasoline engines

#load data for Montreal
G = ox.save_load.load_graphml("/Users/andreafodor/hack18/data/mtl_coord.graphml")

# select an origin and destination node
alon = float(input("Start point longitude: "))
alat = float(input("Start point latitude: "))
blon = float(input("End point longitude: "))
blat = float(input("End point latitude: "))
origin = ox.get_nearest_node(G, (alon, alat))
destination = ox.get_nearest_node(G, (blon, blat))

# define some edge impedance function - fuel consumption
def impedance(length, grades):
    grade = float(grades)
    elevation = grade * length
    lengthkm = length/1000.0
    penalty = totalConsumption(lengthkm, elevation)
    return penalty


G_proj = ox.project_graph(G)
for u, v, k, data in G_proj.edges(keys=True, data=True):
    data['impedance'] = impedance(data['length'], data['grade'])

route_by_impedance = nx.shortest_path(G_proj, source=origin, target=destination, weight='impedance')
#fig, ax = ox.plot_graph_route(G_proj, route_by_impedance, bbox=bbox, node_size=0)
fig, ax = ox.plot_graph_route(G_proj, route_by_impedance, node_size=0, save=True, show=False, close=True, filename='impedance')

route_by_length = nx.shortest_path(G_proj, source=origin, target=destination, weight='length')
fig, ax = ox.plot_graph_route(G_proj, route_by_length, node_size=0, save=True, show=False, close=True, filename='length')

def print_route_stats(route):
    route_lengths = ox.get_route_edge_attributes(G_proj, route, 'impedance')
    print('Total trip fuel consumption: {:,.0f} liters'.format(np.sum(route_lengths)))
    route_lengths = ox.get_route_edge_attributes(G_proj, route, 'length')
    print('Total trip distance: {:,.4f} meters'.format(np.sum(route_lengths)))

print_route_stats(route_by_impedance)
print_route_stats(route_by_length)



# save as html file then display map as an iframe
graph_map = ox.plot_graph_folium(G, popup_attribute='name', edge_width=2)
# save as html file then display map as an iframe
filepath = 'data/graph.html'
graph_map.save(filepath)
IFrame(filepath, width=600, height=500)

route_map = ox.plot_route_folium(G, route_by_impedance)
# save as html file then display map as an iframe
filepath = 'data/route.html'
route_map.save(filepath)
IFrame(filepath, width=600, height=500)


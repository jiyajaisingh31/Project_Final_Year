import timeit
import math
from collections import defaultdict
import sys
from copy import deepcopy
source = sys.argv[1]
destination = sys.argv[2]
routing_option = sys.argv[3]
routing_algorithm= sys.argv[4]
start_time= timeit.default_timer()
print "Building a graph....this may take about half a minute"
city=  tuple([[y for index, y in enumerate(x.strip().split(" ")) if y] for x in open("./city-gps.txt") if x.strip() != ""])
road_seg = tuple([[y for index, y in enumerate(x.strip().split(" ")) if y] for x in open("./road-segments.txt") if x.strip() != ""])

class City(object):

	def __init__(self, name, latitude=None, longitude=None):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude

	def __eq__(self, other):
		return self.name==other.name

	def __hash__(self):
		return hash(self.name)

class Highway(object):

	def __init__(self, name, city_one , city_two, distance, speed_limit):
		self.name = name
		self.city_one = city_one
		self.city_two = city_two
		self.distance = distance
		self.speed_limit = speed_limit

highway_map = defaultdict(set)
# appending highways objects
road_set = set()
speed_limit, highway_count = 0,0
for h in road_seg:
	if len(h)==5 and float(h[3]):
		road_set.add(Highway(h[4], h[0], h[1], float(h[2]), float(h[3])))
		speed_limit += float(h[3])
		highway_count +=1
average_speed_limit = speed_limit/highway_count
list_of_cities=[]
for row in road_seg:
	list_of_cities.append(row[0])
	list_of_cities.append(row[1])
list_of_cities=list(set(list_of_cities))
city = list(city)
for inter in list_of_cities:
	if inter not in [row[0] for row in city]:
		city.append([inter, None , None])
city= tuple(city)
city_map = {}
adjacent_routes ={} 

for row in city:
	latitude = float(row[1]) if row[1]  else 0.0
	longitude = float(row[2]) if row[2] else 0.0
	city_temp = City(row[0],latitude,longitude)
	city_map[row[0]]= city_temp
	adjacent_routes[row[0]]=[]
		

for item in city_map:
	highway_map[item]=filter(None, {r if r.city_one == item or r.city_two == item else None for r in road_set})


print "Completed Building Graph"

#for road in highway_map.get(source):
#    print road.name , road.distance, road.speed_limit, city_map.get(source).latitude
def displacement(city_one, city_two):
	lat_city_one, lon_city_one, lat_city_two, lon_city_two = map(math.radians, [city_map[city_one].latitude,city_map[city_one].longitude,city_map[city_two].latitude, city_map[city_one].longitude])
	latDist, lonDist= lat_city_two-lat_city_one, lon_city_two-lon_city_one
	x=math.sin(latDist/2)**2 + math.cos(lat_city_one) * math.cos(lat_city_two) * math.sin(lonDist/2)**2
	return 6371*2*math.asin(math.sqrt(x))

def is_goal(place):
	return True if place== destination else False
#mem=0
def find_route(source, destination):
	next_route=[source]
	adjacent_routes[source].append([source]) #new code
	depth=0
	list_of_routes=[]
	f_s=displacement(source, destination)
	dist= deepcopy(f_s)
	fringe = [(source,depth,f_s,dist)]
	route=[[source]]
	visited_nodes=[]
	mem = len(fringe)
	if source==destination:
		return "You are already at your destination !!"
	disp = displacement(source, destination)
	print "approximate distance is:", disp
	print "approximate time taken is:", disp/average_speed_limit
	print "Hang On!!...Caliberating route"
	while fringe:
		
		if len(fringe)>mem:
			mem = len(fringe)
		#sorts as per heuristic for a* search
		if routing_algorithm=="astar":
			if len(next_route)>1:
				
				cost_till_now= get_overall_cost(next_route)
			else:
				cost_till_now= (0,0)
			if routing_algorithm in ("distance", "time", "scenic"):
				fringe.sort(key=lambda tup:tup[2])	
						
		elif routing_algorithm=="ids":
			fringe.sort(key= lambda tup:tup[1],reverse=True)
		#elif routing_option=="bfs":
		#	fringe.sort(key= lambda tup:tup[2]) 
		#What to pop for a given algorithm?
		if routing_algorithm in ("ids", "dfs"):
			current_city = fringe.pop()[0]
		elif routing_algorithm in ("bfs","astar"):	
			current_city = fringe.pop(0)[0]
		#makes a track of visited nodes
		visited_nodes.append(current_city)
		edges = highway_map[current_city] #edges of next nodes
		#filters edges for scenic view
		if routing_option=="scenic":
			edges = [edge for edge in edges if edge.speed_limit<55]
		temp_route=[]
		depth+=1
		for edge in edges:
			next_city = edge.city_one if edge.city_two== current_city else edge.city_two if edge.city_one== current_city  else None
			#CALCULATES HEURISTIC FOR A*
			if routing_algorithm=="astar":
				if city_map[next_city].latitude!=0.0:
					x= displacement(next_city, destination)
				else:
					x= displacement(current_city, destination) - get_edge_cost(current_city, next_city)[0]
				if routing_option in ("distance","scenic"):
					g_s = cost_till_now[0]+get_edge_cost(current_city, next_city)[0]
					h_s = x
				elif routing_option=="time":
					g_s = cost_till_now[1]+get_edge_cost(current_city, next_city)[1]
					h_s = x/average_speed_limit
				elif routing_option=="segments":
					g_s= 1
					h_s = 1
				f_s = h_s+g_s

			#modifying fringe in the loop here
			if next_city not in [x[0] for x in fringe]:
				fringe.append((next_city,depth,f_s,edge.distance)) 
			temp_route.append(next_city)

		#path computation starts here
		for new_path in adjacent_routes[current_city]:
			temp=deepcopy(new_path)
			adjacent_routes[current_city].remove(new_path)
		for next_city in temp_route:
			if next_city==destination:
				#list_of_routes.append(temp+[next_city])
				return temp+[next_city]
			if next_city not in temp:
				adjacent_routes[next_city].append(temp+[next_city])
				next_route= deepcopy(temp+[next_city])
		temp=[]	
		#print "total mem", mem
	#return list_of_routes

def get_edge_cost(city_one, city_two):
	x= highway_map[city_one]
	for edge in x:
		if edge.city_one == city_two or edge.city_two== city_two:
			return (edge.distance, edge.speed_limit)
def get_overall_cost(x):
	
	actual_distance, actual_time=0,0
	for c1 in range(len(x)-1):
		actual_distance+=get_edge_cost(x[c1], x[c1+1])[0]
		actual_time +=  get_edge_cost(x[c1], x[c1+1])[0]/ get_edge_cost(x[c1], x[c1+1])[1]
	return (actual_distance, actual_time)


x= find_route(source, destination)

#if routing_option=="segments":
#	x= min(map(len, y))
#elif routing_option in ("distance","time"):
#	x = min(map([get_overall_cost(i) for i in y], y))	
		
(actual_distance, actual_time)=get_overall_cost(x) 
print "overall distance is:", actual_distance
print "overall time is:", actual_time
print "no of segments visited is :", len(x)-1
for i in range(len(x)-1):
	city_one = x[i]
	city_two = x[i+1]
	#highway_name, highway_length= [(edge.name,edge.distance) if (edge.city_one==city_one and  edge.city_two==city_two) or( edge.city_one == city_two) and edge.city_two==city_one else None for edge in highway_map[city_one]]
	for edge in highway_map[city_one]:
		if edge.city_one == city_one and edge.city_two == city_two:
			highway_name = edge.name
			highway_length=edge.distance
		if edge.city_one == city_two and edge.city_two == city_one:
			highway_name = edge.name
			highway_length= edge.distance
	print "From", city_one, "go to ", city_two , "on highway", highway_name, "for" , highway_length, "miles"
print actual_distance ,actual_time, " ".join(str(i) for i in x)

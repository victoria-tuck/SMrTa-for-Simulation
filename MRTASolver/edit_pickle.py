import pickle
import numpy as np
import math

with open('/home/colcon_ws/weighted_graph_hospital.pkl', 'rb') as handle:
    room_count, room_graph = pickle.load(handle)
print(f"Room graph: {room_graph}")

oriented_room_graph = np.ones((room_count, room_count))
map = {0:0,
       1:3,
       2:4,
       3:2,
       4:1,
       5:5}
for room1 in range(room_count):
    for room2 in range(room_count):
        travel_time = room_graph[room1][room2]
        oriented_room_graph[map.get(room1)][map.get(room2)] = travel_time
print(f"Oriented room graph: {oriented_room_graph}")

with open('/home/colcon_ws/oriented_weighted_graph_hospital.pkl', 'wb') as handle:
    pickle.dump((room_count, oriented_room_graph), handle)

updated_room_count = 2*room_count
updated_graph = np.ones((2*room_count, updated_room_count)) * 1000
for room in range(updated_room_count):
    updated_graph[room][room] = 0

for room1, room2 in zip(list(range(room_count)), list(range(1, room_count)) + [0]):
    nominal_travel_time = oriented_room_graph[room1][room2]
    half_travel_time = math.ceil(nominal_travel_time/2)

    new_location = room1
    updated_graph[room1 + room_count][new_location] = half_travel_time
    updated_graph[new_location][room1 + room_count] = half_travel_time
    updated_graph[new_location][room2 + room_count] = half_travel_time
    updated_graph[room2 + room_count][new_location] = half_travel_time

for new_room1 in range(room_count):
    for new_room2 in range(new_room1 + 1, room_count):
        travel_time = oriented_room_graph[new_room1][new_room2 % room_count]
        # room1_offshoot_travel_time = updated_graph[new_room1][room1_offshoot]
        # room2_offshoot_travel_time = updated_graph[new_room2][room2_offshoot]
        # sub_travel_time = travel_time - room1_offshoot_travel_time - room2_offshoot_travel_time
        # assert sub_travel_time >= 0
        assert travel_time > 0
        updated_graph[new_room1][new_room2] = travel_time
        updated_graph[new_room2][new_room1] = travel_time

print(f"Updated graph: {updated_graph}")

with open('/home/colcon_ws/extended_weighted_graph_hospital.pkl', 'wb') as handle:
    pickle.dump((updated_room_count, updated_graph), handle)

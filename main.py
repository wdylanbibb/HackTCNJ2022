import map as map_tools

if __name__ == '__main__':
    (room_list, map) = map_tools.new_map_rooms_and_corridors(30, 6, 10)

    map_tools.draw_map(map)
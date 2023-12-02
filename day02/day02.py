import re
import os
from functools import reduce


test_data = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''


bag_content = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


with open(os.path.dirname(__file__) + "/data.txt") as data_fp:
    data = data_fp.read()
    
    game_raw_list = data.strip().split("\n")
    #game_raw_list = test_data.strip().split("\n")

    games = {}

    for l in game_raw_list:
        game_id = None
        round_content = None

        game_info_part, round_content_part = l.split(":")
        reg_game_result = re.search(r"Game (\d+)", game_info_part.strip(), re.I)
        if reg_game_result:
            game_id = reg_game_result.group(1)
        
        game_stats = {}

        for cube_set in round_content_part.split(";"):
            reg_round_content_result = re.finditer(r"(\d+) ([a-z]+)[ ,]*", cube_set.strip(), re.I)
            for res in reg_round_content_result:
                nb_cube, cubes_color = res.groups()
                
                if cubes_color not in game_stats:
                    game_stats[cubes_color] = []
                
                game_stats[cubes_color].append(int(nb_cube))

        games[game_id] = game_stats

    # PART 1
    legal_games = []

    for game_id, game_content in games.items():
        for color, nb_cube in game_content.items():
            if max(nb_cube) > bag_content[color]:
                break
        else:
            legal_games.append(int(game_id))

    print(sum(legal_games))

    # PART 2
    print(sum([reduce(lambda a, b: a * b, map(lambda s: max(s), game_content.values())) for game_content in games.values()]))

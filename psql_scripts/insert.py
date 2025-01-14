import pandas as pd

file_path = ['steam.csv', 'epic.csv', 'backloggd_games.csv', 'steam_description_data.csv']

f = open("ins.sql", "w")

#steam game data from https://www.kaggle.com/datasets/nikdavis/steam-store-games/data
"""
data = pd.read_csv(file_path[0])

for game in data.iloc:
    res = "insert into games (game_name, steam_id, game_developer, game_publisher, PC, genres, steam_store) values ('"

    g_name = game.to_string().split('\n')[1][4:].strip()

    res = res + g_name.replace("'", "''") + '\',' + str(game.appid) + ',\'' + str(game.developer).replace("'", "''") +  '\',\'' + str(game.publisher).replace("'", "''") + '\',true,\'' + str(game.genres.upper()).replace("'", "''")+';\',true);\n'

    f.write(res)

"""
#steam description data
"""
data = pd.read_csv(file_path[3])

for game in data.iloc:
    res = 'update games set game_desc=\'' + str(game.short_description).replace("'", "''") + '\' where steam_id=' + str(game.steam_appid) + ';\n'

    f.write(res)
"""

#epic game data from https://www.kaggle.com/datasets/mexwell/epic-games-store-dataset
"""
data = pd.read_csv(file_path[1])

for game in data.iloc:
    res = "insert into games (game_name, game_slug, game_developer, game_publisher, PC, genres, epic_store, game_desc) values ('"

    g_name = game.to_string().split('\n')[1][4:].strip()

    res = res + g_name.replace("'", "''") + '\',\'' + str(game.game_slug).replace("'", "''") + '\',\'' + str(game.developer).replace("'", "''") +  '\',\'' + str(game.publisher).replace("'", "''") + '\',true,\'' + str(game.genres).upper().replace("'", "''").replace(",",";") + ';\', true,'

    res = res + '\' + str(game.description).replace("'", "''") + '\' on conflict(game_name) do update set game_slug=EXCLUDED.epic_id , epic_store=EXCLUDED.epic_store;\n'
    
    f.write(res)
"""

#Nintendo shop data from https://www.kaggle.com/datasets/jahnavipaliwal/video-game-reviews-and-ratings/data
"""
data = pd.read_csv(file_path[2])

for game in data.iloc:
    g_name = game.to_string().split('\n')[1][5:].strip()

    if 'Nintendo Switch' in str(game.Platforms):
        res = "insert into games (game_name, game_developer, game_publisher, switch, genres, nintendo_store, game_desc) values ('"

        if game.Developers == '[]': dev = ''
        else: dev = eval(game.Developers)[0]

        if len(eval(game.Developers)) > 1: dis = eval(game.Developers)[1]
        else : dis = dev

        res = res + g_name.replace("'", "''") + '\',\'' + dev.replace("'", "''") +  '\',\'' + dis.replace("'", "''") + '\',true,\'' + str(game.Genres).upper().replace("'", "''").replace("[", "").replace("]", "").replace(",", ";") + ';\', true,'

        res = res + '\' + str(game.description).replace("'", "''") + '\''

        res = res + ' on conflict(game_name) do update set switch=EXCLUDED.switch , nintendo_store=EXCLUDED.nintendo_store;\n'
        
        f.write(res)

    res = 'update games set rating=' + str(game.Rating) + ' where  game_name=\'' + g_name.replace("'", "''") + '\';\n'

    f.write(res)
"""
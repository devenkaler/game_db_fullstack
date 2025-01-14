import sys
sys.path.append("../db")
import games_db

# *Gametype Dictionary is defined with keys:
#                             [game_id] [game_name] [steam_id] [game_slug] [game_developer] 
#                             [game_publisher] [PC] [switch] [steam_store] [epic_store] 
#                             [nintendo_store] [rating] [game_desc] [release_year]

# Returns true if ch is a Gametype Dict
def check_game_type(ch):
    if (type(ch['game_id']) == int) and (type(ch['game_name']) == str) and (type(ch['steam_id']) == int) and (type(ch['game_slug']) == str):
        #print('a')
        if (type(ch['game_developer']) == str) and (type(ch['game_publisher']) == str) and (type(ch['pc']) == bool) and (type(ch['switch']) == bool):
            #print('b')
            if (type(ch['steam_store']) == bool) and (type(ch['epic_store']) == bool) and (type(ch['nintendo_store']) == bool) and (type(ch['rating']) == float):
                #print('c')
                return (type(ch['game_desc']) == str) and (type(ch['release_year']) == int)
             

def test_get_game_by_id(game_id=1):
    game = dict(games_db.get_game_by_id(game_id))
    assert check_game_type(game) == True


def test_get_games_by_features():
    game = dict(games_db.get_games_by_features(limit=1)[0])
    assert check_game_type(game) == True


def test_get_games_by_similar_name(name='Hollow Knight'):
    game = dict(games_db.get_games_by_similar_name(name, limit=1)[0])
    assert check_game_type(game) == True


def test_get_random_game():
    game = games_db.get_random_game()
    assert check_game_type(game) == True


def test_get_release_year_min_max():
    years = games_db.get_release_year_min_max()
    assert type(years[0]) == int
    assert type(years[1]) == int


def test_get_genres():
    genres = games_db.get_genres()
    for g in genres:
        assert type(g[0]) == str


if __name__ == "__main__":
    test_get_game_by_id()
    test_get_games_by_features()
    test_get_games_by_similar_name()
    test_get_random_game()
    test_get_release_year_min_max()
    test_get_genres()
    print("All tests successful")
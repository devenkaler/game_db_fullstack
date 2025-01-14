from flask import Flask, render_template, request
import sys
sys.path.append("../db")
import games_db

app = Flask(__name__)

# Home page
@app.route('/', methods=['GET'])
@app.route('/Home', methods=['GET'])
def index():
    return render_template('index.html')


# Explore page
@app.route('/Explore', methods=['GET'])
def explore():

    min_max_release_year = games_db.get_release_year_min_max()

    game_dev_pub = request.args.get('game_dev_pub', type=str, default=None)
    if game_dev_pub == None: game_dev_pub = ''

    game_name = request.args.get('game_name', type=str, default=None)
    if game_name == None: game_name = ''

    #pc = request.args.get('pc', type=bool, default=False)
    #switch = request.args.get('switch', type=bool, default=False)
    steam_store = request.args.get('steam_store', type=bool, default=False)
    epic_store = request.args.get('epic_store', type=bool, default=False)
    nintendo_store = request.args.get('nintendo_store', type=bool, default=False)
    rating = request.args.get('min_rating', type=float, default=0)
    release_year_min = request.args.get('year_min', type=int, default=min_max_release_year[0])
    release_year_max = request.args.get('year_max', type=int, default=min_max_release_year[1])
    genre_all = request.args.get('genre-all', type=bool, default=False)
    advanced_search = request.args.get('toggle_search', type=bool, default=False)
    page_num = request.args.get('page_num', type=int, default=1)

    # List of genre names
    genres = games_db.get_genres()
    genres = [str(genre)[2:][:-3] for genre in genres]

    # Key value pair of (genre_name, bool)
    genres_req = {genre: request.args.get(f'genre-{genre}', type=bool, default=False) for genre in genres}
    genres_to_display = [genre for genre in genres if genres_req[genre]]

    
    if advanced_search:
        games_to_display = games_db.get_games_by_features(game_dev_pub=game_dev_pub, steam_store=steam_store,
                                                      epic_store=epic_store, nintendo_store=nintendo_store, rating=rating,
                                                      release_year_min=release_year_min, release_year_max=release_year_max,
                                                      game_name=game_name, genres=genres_to_display, page=page_num)
        
    else:
        games_to_display = games_db.get_games_by_features(page=page_num, game_name=game_name)
    
    page_max = len(games_to_display) < games_db.GAME_LIMIT

    return render_template('explore.html', data=games_to_display, release_year_min=release_year_min,
                                           release_year_max=release_year_max, min_max_release_year=min_max_release_year,
                                           steam_store=steam_store, epic_store=epic_store, 
                                           nintendo_store=nintendo_store, genres_req=genres_req, genres=genres, min_rating=rating,
                                           genre_all=genre_all, advanced_search=advanced_search, page_num=page_num, page_max=page_max,
                                           game_dev_pub=game_dev_pub)


# Game page for a game by ID
@app.route('/Game', methods=['GET'])
def game_page():

    game_id = request.args.get("id")

    game = games_db.get_game_by_id(game_id)

    return render_template('game-page.html', game=game)


# Game page for a reandom game
@app.route('/Random', methods=['GET'])
def random_game():

    game = games_db.get_random_game()

    return render_template('game-page.html', game=game)
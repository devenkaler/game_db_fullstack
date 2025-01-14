from connect import *


# *Gametype Dictionary is defined with keys:
#                             [game_id] [game_name] [steam_id] [epic_id] [game_developer] 
#                             [game_publisher] [PC] [switch] [steam_store] [epic_store] 
#                             [nintendo_store] [rating] [game_desc] [release_year]


GAME_LIMIT = 60


# Returns: Gametype Dictionary*
# Input type: int
def get_game_by_id(game_id):

    #establish connection using RealDictCurs
    conn = connectDict()

    with conn.cursor() as curs:
    
        query = """
                    select * from 
                        (select * from games where game_id=%(game_id)s) game
                            left outer join
                                (select game_id, array_agg(genre_name) as genres 
                                from genre_lookup group by game_id) game_genres
                            on game.game_id=game_genres.game_id;
                """
        
        curs.execute(query, {'game_id': game_id})
        res = curs.fetchall()[0]

    return res


# Returns: List of Strings
def get_genres():

    #establish connection as default curs type
    conn = connect()

    with conn.cursor() as curs:

        query = """
                    select genre_name from genre_lookup group by genre_name
                    order by count(genre_name) desc;
                """
        
        curs.execute(query)
        res = curs.fetchall()

    return res


# Returns: Gametype Dictionary*
# Input type: String, String, bool, bool, bool, bool, 
#             bool, int, String, int, int, String, Tuple, Float, int
def get_games_by_features(game_dev_pub='', pc=None, switch=None, steam_store=None, epic_store=None, 
                          nintendo_store=None, rating=None, release_year_min=None, release_year_max=None,
                          game_name='', genres=None, page=1, limit=GAME_LIMIT, similarity=0.5):

    #establish connection using RealDictCurs
    conn = connectDict()

    with conn.cursor() as curs:
        
        query = """
                    select * from (select * from games where 
                        (game_developer=%(game_dev_pub)s or game_publisher=%(game_dev_pub)s or %(game_dev_pub)s='') and
                        (pc=%(pc)s or %(pc)s is null) and
                        (switch=%(switch)s or %(switch)s is null) and
                        (steam_store=%(steam_store)s or %(steam_store)s is null) and
                        (epic_store=%(epic_store)s or %(epic_store)s is null) and
                        (nintendo_store=%(nintendo_store)s or %(nintendo_store)s is null) and
                        (rating>=%(rating)s or %(rating)s is null) and
                        ((release_year>=%(release_year_min)s and release_year<=%(release_year_max)s) or %(release_year_min)s is null) and
                        ((similarity(game_name,%(game_name)s) > 0.5 or lower(game_name) like %(game_name)s) or %(game_name)s='')) game
                    inner join
                        (select game_id, array_agg(genre_name) as genres from genre_lookup
                            where (genre_name=any(%(genres)s) or %(genres)s is null)
                            group by game_id) game_genres
                        on game.game_id=game_genres.game_id
                    order by game.game_id desc limit %(limit)s offset %(page)s;

                """
        
        curs.execute(query, {'game_dev_pub': game_dev_pub, 'pc': pc, 'switch': switch, 'steam_store': steam_store, 'epic_store': epic_store, 
                          'nintendo_store': nintendo_store, 'rating': rating, 'release_year_min': release_year_min, 'release_year_max': release_year_max,
                          'game_name': game_name, "genres": genres, "limit": limit, 'page':(page-1)*limit})
        res = curs.fetchall()
    
    return res


# Returns: Gametype Dictionary*
# Input type: int
def get_games_by_similar_name(name, similarity=0.5, limit=GAME_LIMIT):

    #establish connection using RealDictCurs
    conn = connectDict()

    with conn.cursor() as curs:

        query = """
                    select * from
                        (select * from games where 
                            similarity(game_name,%(name)s) >= %(similarity)s or
                            lower(game_name) like %(name)s
                        limit %(limit)s) game
                    left outer join
                        (select game_id, array_agg(genre_name) as genres from genre_lookup group by game_id) game_genres
                    on game.game_id=game_genres.game_id;;
                """
        
        curs.execute(query, {'name': name+'%%', 'similarity': similarity, 'limit': limit})
        res = curs.fetchall()
    
    return res


# Returns: Gametype Dictionary*
def get_random_game():

    #establish connection using RealDictCurs
    conn = connectDict()

    with conn.cursor() as curs:

        query = """
                    select * from
                        (select * from games tablesample system_rows(1)) game
                    left outer join
                        (select game_id, array_agg(genre_name) from genre_lookup group by game_id) game_genres
                    on game.game_id=game_genres.game_id;;
                """
        
        curs.execute(query)
        res = curs.fetchall()[0]
    
    return res


# Returns: min and max game year
def get_release_year_min_max():

    #establish connection using default curs type
    conn = connect()

    with conn.cursor() as curs:

        query = """
                    select min(release_year), max(release_year) from games;
                """
        
        curs.execute(query)
        res = curs.fetchall()[0]
    
    return res
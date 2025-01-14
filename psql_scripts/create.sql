CREATE TABLE games (
    game_id                     int primary key GENERATED ALWAYS AS IDENTITY,
    game_name                   varchar(100) unique,
    steam_id                    int not null default 0,
    game_slug                     varchar(100) not null default '-',
    game_developer              varchar(100) not null default 'N/A',
    game_publisher              varchar(100),
    PC                          boolean not null default false,
    Switch                      boolean not null default false,
    steam_store                 boolean not null  default false,
    epic_store                  boolean not null default false,
    nintendo_store              boolean not null default false,
    rating                      float not null default 0,
    game_desc                   text,
    release_year                int 
);

CREATE TABLE genre_lookup (
    game_id                     int,
    genre_name                  varchar(32),
    
    CONSTRAINT fk_game_id FOREIGN KEY(game_id) references games(game_id) on DELETE CASCADE
);

CREATE EXTENSION IF NOT EXISTS "pg_trgm";

CREATE EXTENSION IF NOT EXISTS "unaccent";

CREATE EXTENSION IF NOT EXISTS "tsm_system_rows";
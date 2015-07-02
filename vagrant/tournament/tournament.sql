-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	name TEXT, 
	id SERIAL PRIMARY KEY
);

CREATE TABLE matches (
	player1 integer REFERENCES players(id),
	player2 integer REFERENCES players(id),
	winner integer,
	PRIMARY KEY(player1, player2)
);

CREATE VIEW standings AS 
	SELECT wins.id, wins.wins, matches.matches 
	FROM (
		SELECT id, count(winner) as wins 
		FROM players LEFT JOIN matches 
		ON id = winner 
		GROUP BY id
	) as wins 
	JOIN (
		SELECT id, count(player1) as matches 
		FROM players LEFT JOIN matches 
		ON id = player1 OR id=player2 
		GROUP BY id
	) as matches 
	on wins.id=matches.id 
	ORDER BY wins DESC, matches;

CREATE VIEW match_scoring AS
	SELECT id, 3*wins as match_points
	FROM standings;

--SELECT player1, odds.name, player2, evens.name 
-- FROM (
-- 	SELECT odds.id as player1, name, ROW_NUMBER() OVER() 
-- 	FROM (
-- 		SELECT id, ROW_NUMBER() OVER() 
-- 		FROM standings 
-- 		ORDER BY wins desc, matches
-- 	) as odds 
-- 	JOIN players ON odds.id=players.id 
-- 	WHERE row_number % 2 != 0 
-- 	order by row_number
-- ) as odds 
-- JOIN (
-- 	SELECT evens.id as player2, name, ROW_NUMBER() OVER() 
-- 	FROM (
-- 		SELECT id, ROW_NUMBER() OVER() 
-- 		FROM standings 
-- 		ORDER BY wins desc, matches
-- 	) as evens JOIN players ON evens.id=players.id 
-- 	WHERE row_number % 2 = 0 
-- 	ORDER BY row_number
-- ) as evens 
-- ON odds.row_number = evens.row_number;




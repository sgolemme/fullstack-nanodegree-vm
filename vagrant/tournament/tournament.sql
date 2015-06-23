-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

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
	ORDER BY wins DESC, matches
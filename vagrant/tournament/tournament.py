#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(id) FROM players")
    num = cursor.fetchone()[0]
    db.close() 
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players VALUES(%s)", (name,))
    db.commit()
    db.close() 


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT players.id, name, wins, matches FROM standings JOIN players ON standings.id=players.id ORDER BY wins DESC, matches")
    '''standings = cursor.fetchall();'''
    standings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3])) for row in cursor.fetchall()]
    db.close() 
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO matches (player1, player2, winner) VALUES(%s, %s, %s)", (winner,loser, winner,))
    db.commit()
    db.close() 
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT player1, odds.name, player2, evens.name FROM (SELECT odds.id as player1, name, ROW_NUMBER() OVER() FROM (SELECT id, ROW_NUMBER() OVER() FROM standings ORDER BY wins desc, matches) as odds JOIN players ON odds.id=players.id WHERE row_number % 2 != 0 order by row_number) as odds JOIN (SELECT evens.id as player2, name, ROW_NUMBER() OVER() FROM (SELECT id, ROW_NUMBER() OVER() FROM standings ORDER BY wins desc, matches) as evens JOIN players ON evens.id=players.id WHERE row_number % 2 = 0 ORDER BY row_number) as evens ON odds.row_number = evens.row_number")
    pairs = [(int(row[0]), str(row[1]), int(row[2]), str(row[3])) for row in cursor.fetchall()]
    db.close() 
    return pairs
    

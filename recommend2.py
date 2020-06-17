# -*- coding: utf-8 -*-

from py2neo import Graph

graph = Graph('http://localhost:7474/', auth=("neo4j", "neo4j"))

threshold = 0.5
userId = 35


query = (  ### Similarity normalization : count number of movies seen by u1 ###
        # Count movies rated by u1 as countm
        'MATCH (m1:Movie)<-[:hasRated]-(u1:User {ID :$user1}) '
        'WITH count(m1) as countm '
        ### Recommendation ###
        # Retrieve all users u2 who share at least one movie with u1
        'MATCH (u2:User)-[r2:hasRated]->(m1:Movie)<-[r1:hasRated]-(u1:User {ID :$user1}) '
        # Check if the ratings given by u1 and u2 differ by less than 1
        'WHERE (NOT u2=u1) AND (abs(r2.Rating - r1.Rating) <= 1) '
        # Compute similarity
        'WITH u1, u2, tofloat(count(DISTINCT m1))/countm as Sim '
        # Keep users u2 whose similarity with u1 is above some threshold
        'WHERE Sim > $threshold '
        # Retrieve movies m that were rated by at least one similar user, but not by u1
        'MATCH (m:Movie)<-[r:hasRated]-(u2) '
        'WHERE (NOT (m)<-[:hasRated]-(u1)) '
        # Compute score and return the list of suggestions ordered by score
        'WITH DISTINCT m, count(r) as n_u, tofloat(sum(r.Rating)) as sum_r '
        'WHERE n_u > 1 '
        'RETURN m, sum_r/n_u as Score ORDER BY score DESC'
        )

result = graph.run(query, user1=int(user_id), threshold=threshold).to_table()
print(result)
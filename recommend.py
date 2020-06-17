# -*- coding: utf-8 -*-

from py2neo import Graph

graph = Graph('http://localhost:7474/', auth=("neo4j", "neo4j"))

total = 943
topK = 3
userId = 35

#For one user, and for each movie he don't rate but was rated by their top 3 similars, rate is predicted by averaging their rates.

query = (
        'MATCH (b:User)-[r:hasRated]->(m:Movie), (b)-[s:similarTo]-(a:User {ID :$user1}) ' 
        'WHERE NOT((a)-[:hasRated]->(m)) '
        'WITH m, s.Similarity AS Similarity, r.Rating AS Rating '
        'ORDER BY m.Title, Similarity DESC '
        'WITH m.Title AS Movie, COLLECT(Rating)[0..$topK] AS Ratings '
        'WITH Movie, REDUCE(s = 0, i IN Ratings | s + i)*1.0 / SIZE(Ratings) AS Reco '
        'ORDER BY Movie DESC '
        'RETURN Movie, Reco AS Recommendation'
        )

result = graph.run(query, user1=int(user_id), topK=topK).to_table()
print(result)
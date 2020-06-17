# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from py2neo import Graph

graph = Graph('http://localhost:7474/', auth=("neo4j", "neo4j"))

total = 943
minSimCnt = 5

for i in range(1, total):
    for j in range(1, total):
        if i != j:
            query = (
                    'MATCH (u1:User {ID: $user1})-[r1:hasRated]->(m:Movie)<-[r2:hasRated]-(u2:User {ID: $user2}) ' 
                    'WITH count(m) AS cnt '
                    'RETURN *'
                    )
            result = graph.run(query, user1=i, user2=j).to_table()
            cnt = result[0][0]

            if cnt >= minSimCnt:
                query = (
                        'MATCH (u1:User {ID: $user1})-[x:hasRated]->(m:Movie)<-[y:hasRated]-(u2:User {ID: $user2}) '
                        'WITH SUM(x.Rating * y.Rating) AS xyDotProduct, SQRT(REDUCE(xDot = 0, a IN COLLECT(x.Rating) | xDot + a*a)) AS xLength, SQRT(REDUCE(yDot = 0, b IN COLLECT(y.Rating) | yDot + b*b)) AS yLength, u1, u2 '
                        'MERGE (u1)-[s:similarTo]-(u2) SET s.Similarity = xyDotProduct / (xLength * yLength)'
                        )

                graph.run(query, user1=i, user2=j)
                print (f"{i} and {j} similarity inserted.")
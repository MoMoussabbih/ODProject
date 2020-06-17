# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from py2neo import Graph

# N.B : 57 mins to finish

graph = Graph('http://localhost:7474/', auth=("neo4j", "neo4j"))

## Reading datasets

#Users
users_col = ['ID','Age','Gender','Occupation','Zip code']
users = pd.read_csv('ml-100k/u.user', sep='|', header=None, names=users_col)
n_u = users.shape[0]

#Types
types_col = ['Name', 'ID']
types = pd.read_csv('ml-100k/u.genre', sep='|', header=None, names=types_col)
n_g = types.shape[0]

#Movies
# Format : id | title | release date | 'empty column' | IMDb url | 'types' : where "types" is a vector of size n_g : types[i]=1 if the movie belongs to type i
movies_col = ['ID', 'Title', 'Release date', '', 'IMdb URL'] + types['ID'].tolist()
movies = pd.read_csv('ml-100k/u.item', sep='|', header=None, names=movies_col)
movies = movies.drop(columns='')
movies = movies.fillna('NA')
n_m = movies.shape[0]


#Ratings
ratings_col = ['userID', 'movieID','Rating', 'Timestamp']
ratings = pd.read_csv('ml-100k/u1.base', sep='\t' ,header=None, names=ratings_col)
n_r = ratings.shape[0]


## Creating the graph

# Nodes for users, identified by their IDs, ages, occupations and zip codes
for i in range (len(users)):
    row = users.iloc[i,:]
    graph.run("MERGE (:User {ID : $a, Age : $b, Occupation : $c, ZipCode : $d})",
                 a=int(row['ID']), b=int(row['Age']), c=row['Occupation'], d=row['Zip code'])


# Nodes for types, identified by their IDs and names
for i in range (len(types)):
    row = types.iloc[i,:]
    graph.run("MERGE (:Type {ID :$a, Name: $b})",
                a=int(row['ID']), b=row['Name'])
              
# Nodes for movies, identified by their IDs, titles, release dates and URLs
# "hasType" edge links movies to their types
for i in range (len(movies)):
    row = movies.iloc[i,:]
    graph.run("MERGE (:Movie {ID :$a, Title: $b, ReleaseDate: $c, IMdbURL: $d})",
                a=int(row['ID']), b=row['Title'], c=row['Release date'], d=row['IMdb URL'])

    # hasType : vector of size n_g, hadType[i]=True if Movie m belongs to Type i
    types_vect = np.array(list(row)[-19:])
    hasType = types_vect == 1
    related_types = types[hasType].axes[0].values
    
    for type in related_types :
        graph.run("MATCH (t:Type {ID :$a0}) MATCH (m:Movie {ID :$a, Title: $b, ReleaseDate: $c, IMdbURL: $d}) MERGE (m)-[:hasType]->(t)",
                  a0=int(type), a=int(row['ID']), b=row['Title'], c=row['Release date'], d=row['IMdb URL'])


# "hasRated" edge links users to movies they rated
for i in range (len(ratings)):
    row = ratings.iloc[i,:]
    graph.run("MATCH (u:User {ID :$a}) MATCH (m:Movie {ID :$b}) MERGE (u)-[:hasRated {Rating :$c, Timestamp :$d}]->(m)",
              a=int(row['userID']), b=int(row['movieID']), c=int(row['Rating']), d=int(row['Timestamp']))
              
## Creating indexes
graph.run('CREATE INDEX ON :User(ID)')
graph.run('CREATE INDEX ON :Movie(ID)')
graph.run('CREATE INDEX ON :Type(ID)')
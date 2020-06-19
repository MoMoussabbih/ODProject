## Intro

This is a project for a movies recommendation system using collaborative filtering based on Neo4j.

## Steps

**1-** For graph making, ***"insert.py"*** should be ran 
```
python insert.py
```

**2-** *(Optional)* If you want to perform the **metadata-based approach** for recommandation, similarity edges must be created by running ***"insert_similarity.py"***.
```
python insert_similarity.py
```

**2bis-** If the step 2 was chosen, recommendation algorithm for metadata-based approach is written in ***"recommand.py"***, keep in mind that variables *topK* (top number of similars) and *userID* (user we want to predict its ratings for unrated movies) could be changed inside the code *(line 8 and 9)*:
```
topK = ... #by default it is 3
userId = ... #by default it is 35
```
Then we could run the code :
```
python recommend.py
```

**3** Recommendation algorithm for **original schema-based approach** is written in ***"recommand2.py"***, variables *threshold* (for similarity condition) and *userID* (user we want to predict its ratings for unrated movies) could be changed inside the code *(line 7 and 8)*:
```
threshold = ... #by default it is 0.5
userId = ... #by default it is 35
```
Then we could run the code :
```
python recommend.py
```

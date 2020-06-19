## Intro

This is a project for a **movies recommendation system** using **collaborative filtering** based on ***Neo4j***.

## Hardware
```
Processor: Intel(R) Core(TM) i7-7500 CPU @ 2.70 GHz 2.90 GHz
Installed memory (RAM): 8.00 GB
System type: 64-bit Operating System, x64-based processor
```

## Requirements

This project was written in ***Python v3.7***, the following Python packages are required :
```
py2neo==4.3.0
pandas==0.25.0
numpy==1.18.1
```

## Steps

**1-** For graph making, ***"insert.py"*** should be ran *(It takes* ***57 mins*** *with the hardware mentioned above)*
```
python insert.py
```

**2-** *(Optional)* If you want to perform the **metadata-based approach** for recommandation, similarity edges must be created by running ***"insert_similarity.py"*** *(It takes* ***5 hours*** *with the hardware mentioned above)*
```
python insert_similarity.py
```

**2bis-** If the step 2 was chosen, recommendation algorithm for metadata-based approach is written in ***"recommend.py"***, keep in mind that variables : ***topK*** (top number of similars) and ***userID*** (user we want to predict its ratings for unrated movies) could be changed inside the code *(line 8 and 9)*:
```
topK = ... #by default it is 3
userId = ... #by default it is 35
```
Then we could run the code :
```
python recommend.py
```

**3-** Recommendation algorithm for **original schema-based approach** is written in ***"recommend2.py"***, variables : ***threshold*** (for similarity condition) and ***userID*** (user we want to predict its ratings for unrated movies) could be changed inside the code *(line 7 and 8)*:
```
threshold = ... #by default it is 0.5
userId = ... #by default it is 35
```
Then we could run the code :
```
python recommend.py
```

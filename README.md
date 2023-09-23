# FootBall SportsBetting Aid

## Two Prediction Protocols 
Currently experimenting with two prediction protocols.
### PIGEON
Pigeon prediction protocol takes in both away and home team stats as features for predicting both home and away goals.
### SEAGULL
Seagull prediction protocol only takes in its own stats as features. E.g. to predict away goals only away stats are used as features.

## Instructions
1. Download all libraries including: sklearn, pandas, numpy, beautifulSoup, matplotlib, requests
2. Run "python pigeon_predictor.py" or "python seagull_predictor"
3. Enter home and away team making sure team name matches the format used by skysports in their urls
4. You will have the predicted scoreline

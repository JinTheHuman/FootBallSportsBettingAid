# FootBall SportsBetting Aid

Predicts scorelines for upcoming Premier League fixtures

## Two Prediction Protocols 
Currently experimenting with two prediction protocols.
### PIGEON
Pigeon prediction protocol takes in both away and home team stats as features for predicting both home and away goals.
### SEAGULL
Seagull prediction protocol only takes in its own stats as features. E.g. to predict away goals only away stats are used as features.

## Instructions
1. Download all libraries including: sklearn, pandas, numpy, beautifulSoup, matplotlib, requests
2. Run "python pigeon_predictor.py" or "python seagull_predictor.py"
4. You will have the predicted scorelines for 10 of the upcoming fixtures

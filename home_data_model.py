import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")


def make_home_predictions(inputs):
    predictions = []
    dataset = pd.read_csv("Datasets/HOME_DATA.csv")
    X = dataset.iloc[:, 1:].to_numpy()
    y = dataset["HomeGoals"]
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    for input in inputs:
        input = scaler.transform(input)
        estimator = LinearRegression()
        estimator.fit(X, y)
        predictions.append(estimator.predict(input)[0])
    return predictions


def make_away_predictions(inputs):
    predictions = []
    dataset = pd.read_csv("Datasets/PL_DATA.csv")
    dataset = dataset.drop(["HomeGoals"], axis=1)
    X = dataset.iloc[:, 1:].to_numpy()
    y = dataset["awayGoals"]
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    for input in inputs:
        input = scaler.transform(input)
        estimator = LinearRegression()
        estimator.fit(X, y)
        predictions.append(estimator.predict(input)[0])
    return predictions


def probability_analysis(predictions, results):
    total = 0
    correct = 0

    incorrect_by = [0, 0, 0, 0, 0, 0, 0, 0]

    for idx, prediction in enumerate(predictions):
        rounded_prediction = round(prediction)
        if rounded_prediction < 0:
            rounded_prediction = 0
        if rounded_prediction == results[idx]:
            correct += 1
        else:
            incorrect_by[abs(rounded_prediction - results[idx])] += 1
        total += 1

    print("Goal Predictions")
    print(correct, "out of", total)
    print("Success Rate: ", correct / total * 100, "%")
    for i in range(1, len(incorrect_by)):
        print("wrong by", i, ":", incorrect_by[i], end="")
        print(" Probability: ", incorrect_by[i] / total * 100, "%")


def plot_data(x, y, title="Goals Scored failed predictions"):
    plt.scatter(x, y)
    plt.xlabel("actual goals")
    plt.ylabel("prediction goals")
    plt.title(title)
    plt.xticks(np.arange(math.floor(min(x)), max(x) + 1, 1.0))
    plt.yticks(np.arange(math.floor(min(y)), max(y) + 1, 1.0))
    plt.tight_layout()
    plt.show()


def generate_input(dataset):
    inputs = []
    for index, row in dataset.iterrows():
        row_values = row.values[1:]
        inputs.append(np.array(row_values).reshape(1, -1))

    return inputs


if __name__ == "__main__":
    # HOME GOALS PREDICTION
    home_dataset = pd.read_csv("Datasets/HOME_DATA.csv")

    inputs = generate_input(home_dataset)

    h_predictions = make_home_predictions(inputs)
    results = home_dataset["HomeGoals"]

    probability_analysis(h_predictions, results)

    plot_data(home_dataset["HomeGoals"], h_predictions, "Home Predictions")

    # # AWAY GOALS PREDICTION
    # away_dataset = pd.read_csv("Datasets/PL_DATA.csv")

    # inputs = generate_input(away_dataset)

    # a_predictions = make_away_predictions(inputs)
    # results = away_dataset["awayGoals"]

    # probability_analysis(a_predictions, results)

    # plot_data(away_dataset["awayGoals"], a_predictions, "Away Predictions")

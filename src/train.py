# src/train.py
import os
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression

DATA_PATH = "data/data.csv"
MODEL_PATH = "model/model.pkl"


def train():
    df = pd.read_csv(DATA_PATH)

    X = df[["x"]].to_numpy().astype(float)
    y = df["y"].to_numpy().astype(float)

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Trained model saved to {MODEL_PATH}")
    print("Coefficient:", model.coef_[0], "Intercept:", model.intercept_)


if __name__ == "__main__":
    train()

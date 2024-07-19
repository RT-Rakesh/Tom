from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

def train_model(df):
    X = df.drop(columns=["Price", "Postal Code"])
    y = df["Price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    model = MLPRegressor(
        random_state=42,
        max_iter=2000,
        hidden_layer_sizes=(100, 80, 50),
        n_iter_no_change=500,
        early_stopping=True,
        verbose=True,
        validation_fraction=0.1
    )

    model.fit(X_train, y_train)

    return model, X_train, y_train, X_test, y_test

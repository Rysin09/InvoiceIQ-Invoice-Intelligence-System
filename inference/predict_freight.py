import os
import joblib
import pandas as pd

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model path
MODEL_PATH = os.path.join(
    BASE_DIR,
    "freight_cost_prediction",
    "models",
    "predict_freight_model.pkl"
)


def load_model(model_path=MODEL_PATH):
    """
    Load trained freight prediction model
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at:\n{model_path}"
        )

    return joblib.load(model_path)


def predict_freight_cost(input_data, model):
    """
    Predict freight cost for given input data
    """

    input_df = pd.DataFrame(input_data)

    predictions = model.predict(input_df)

    input_df["Predicted_Freight"] = predictions.round(2)

    return input_df


def main():

    # Sample data
    sample_data = {
        "Dollars": [18500, 9000, 3000, 2000]
    }

    try:
        model = load_model()

        predictions = predict_freight_cost(
            sample_data,
            model
        )

        print("\nFreight Cost Predictions:\n")
        print(predictions)

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()

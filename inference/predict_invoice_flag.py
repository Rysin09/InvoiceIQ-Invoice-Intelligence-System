import os
import joblib
import pandas as pd

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
MODEL_PATH = os.path.join(
    BASE_DIR,
    "invoice_flagging",
    "models",
    "predict_flag_invoice.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "invoice_flagging",
    "models",
    "scaler.pkl"
)


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def load_scaler():
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            f"Scaler file not found:\n{SCALER_PATH}"
        )

    return joblib.load(SCALER_PATH)


def predict_invoice_flag(input_data, model, scaler):

    input_df = pd.DataFrame(input_data)

    # Same features used during training
    features = [
        "invoice_quantity",
        "invoice_dollars",
        "Freight",
        "total_item_quantity",
        "total_item_dollars"
    ]

    input_scaled = scaler.transform(
        input_df[features]
    )

    predictions = model.predict(input_scaled)

    input_df["Predicted_Flag"] = predictions

    input_df["Risk_Status"] = input_df[
        "Predicted_Flag"
    ].map({
        0: "Normal",
        1: "High Risk"
    })

    return input_df


def main():

    sample_data = {
        "invoice_quantity": [100, 200],
        "invoice_dollars": [10000, 15000],
        "Freight": [150, 300],
        "total_item_quantity": [100, 180],
        "total_item_dollars": [9998, 12000]
    }

    try:

        model = load_model()
        scaler = load_scaler()

        predictions = predict_invoice_flag(
            sample_data,
            model,
            scaler
        )

        print("\nInvoice Flag Predictions:\n")
        print(predictions)

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
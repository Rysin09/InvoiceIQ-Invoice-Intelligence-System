from data_preprocessing import (
    load_invoice_data,
    apply_labels,
    split_data,
    scale_features
)

from model_evaluation import (
    train_random_forest,
    evaluate_classifier
)

import joblib
import os

FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars"
]

TARGET = "flag_invoice"


def main():

    # create models folder if not exists
    os.makedirs("models", exist_ok=True)

    # Load data
    df = load_invoice_data()
    df = apply_labels(df)

    # Prepare data
    X_train, X_test, y_train, y_test = split_data(
        df,
        FEATURES,
        TARGET
    )

    X_train_scaled, X_test_scaled = scale_features(
        X_train,
        X_test,
        "models/scaler.pkl"
    )

    # Train model
    grid_search = train_random_forest(
        X_train_scaled,
        y_train
    )

    # Evaluate model
    evaluate_classifier(
        grid_search.best_estimator_,
        X_test_scaled,
        y_test,
        "Random Forest Classifier"
    )

    # Save best model
    joblib.dump(
        grid_search.best_estimator_,
        "models/predict_flag_invoice.pkl"
    )

    print("\nModel saved successfully!")


if __name__ == "__main__":
    main()
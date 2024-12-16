import pandas as pd
import numpy as np
from gluonts.dataset.common import ListDataset
from gluonts.model.deepar import DeepAREstimator
from gluonts.mx.trainer import Trainer
from gluonts.evaluation import Evaluator
from gluonts.evaluation.backtest import make_evaluation_predictions
from datetime import timedelta
import mxnet as mx


def prepare_data(df):
    df['stock_date'] = pd.to_datetime(df['stock_date'])
    df.sort_values(by='stock_date', inplace=True)

    # Group by company ID if multiple stocks are included
    groups = []
    for company_id, group in df.groupby(['company_id']):
        groups.append({
            "target": group['close_price'].tolist(),
            "start": group['stock_date'].iloc[0],
            "feat_static_cat": [company_id]  # Use company ID as a static feature
        })

    return groups


# Example data loading
data = {
    "stock_date": [
        "2024-12-02", "2024-12-03", "2024-12-04", "2024-12-05", "2024-12-06",
        "2024-12-09", "2024-12-10", "2024-12-11",
        "2024-12-02", "2024-12-03", "2024-12-04", "2024-12-05", "2024-12-06",
        "2024-12-09", "2024-12-10", "2024-12-11"
    ],
    "close_price": [
        1880, 1892, 1889, 1935, 1922, 1924, 1949, 1974, 1754, 1750, 1758, 1775, 1777, 1786, 1795, 1795
    ],
    "company_id": [
        1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2
    ]
}

df = pd.DataFrame(data)

# Prepare the training and testing datasets
data_groups = prepare_data(df)

train_ds = ListDataset(
    [{"start": group["start"], "target": group["target"], "feat_static_cat": group["feat_static_cat"]} for group in
     data_groups],
    freq="D"
)

# Define the DeepAR model
estimator = DeepAREstimator(
    freq="D",
    prediction_length=1,  # Predict one day ahead
    trainer=Trainer(
        epochs=50,
        learning_rate=1e-3,
        batch_size=32,
        num_batches_per_epoch=50,
        context_length=7,  # Context of 7 days
    ),
    use_feat_static_cat=True,
    cardinality=[len(df['company_id'].unique())]  # Number of companies
)

# Train the model
predictor = estimator.train(train_ds)


# Forecast the next day
def forecast_tomorrow(predictor, data_groups):
    test_ds = ListDataset(
        [{"start": group["start"], "target": group["target"], "feat_static_cat": group["feat_static_cat"]} for group in
         data_groups],
        freq="D"
    )

    forecast_it, ts_it = make_evaluation_predictions(
        dataset=test_ds, predictor=predictor, num_samples=100
    )

    forecasts = list(forecast_it)
    ts = list(ts_it)

    results = []
    for i, forecast in enumerate(forecasts):
        prediction = forecast.mean[0]  # Get the predicted mean for the next day
        results.append({"company_id": i + 1, "predicted_close_price": prediction})

    return results


predictions = forecast_tomorrow(predictor, data_groups)

# Output the predictions
for prediction in predictions:
    print(f"Company ID {prediction['company_id']} predicted close price: {prediction['predicted_close_price']:.2f}")


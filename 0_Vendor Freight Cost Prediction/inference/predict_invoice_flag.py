import joblib
import pandas as pd


MODEL_PATH = "invoice_flagging/models/predict_flag_invoice.pkl"

SCALER_PATH = "invoice_flagging/models/scaler.pkl"


FEATURE_COLUMNS = [

    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars"

]


def load_model():

    return joblib.load(MODEL_PATH)


def load_scaler():

    return joblib.load(SCALER_PATH)


def predict_invoice_flag(input_data):

    model = load_model()

    scaler = load_scaler()

    input_df = pd.DataFrame(input_data)

    input_df = input_df[FEATURE_COLUMNS]

    scaled_input = scaler.transform(input_df)

    prediction = model.predict(scaled_input)

    input_df["Predicted_Flag"] = prediction

    return input_df


if __name__ == "__main__":

    sample_data = {

        "invoice_quantity":[50],

        "invoice_dollars":[352.95],

        "Freight":[1.73],

        "total_item_quantity":[162],

        "total_item_dollars":[2476.0]

    }

    print(predict_invoice_flag(sample_data))
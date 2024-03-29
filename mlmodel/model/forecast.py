import pandas as pd
from os.path import exists
from os import mkdir
from gluonts.dataset.pandas import PandasDataset
from gluonts.mx.model.deepar import DeepAREstimator
from gluonts.trainer import Trainer
from pathlib import Path
import mlflow
# from gluonts.evaluation import make_evaluation_predictions
# from gluonts.evaluation import Evaluator

def main(json):
    df = pd.DataFrame.from_dict(json,orient='index')
    if exists('model'):
        add(df)
    else:
        create(df)

def create(df):
    remote_server_uri = "http://mlflow.com"
    mlflow.set_tracking_uri(uri=remote_server_uri)
    with mlflow.start_run():
        mlflow.gluon.autolog()
        train = df.loc[df['end'] < '2023-01-01']
        valid = df.loc[df['end'] >= '2023-01-01']
        prediction_length = 30
        mlflow.log_param("prediction_length", prediction_length)

        train_ds = PandasDataset.from_long_dataframe(train, target='target', item_id='ident',
                                                     timestamp='end', freq='D')
        # https://ts.gluon.ai/stable/api/gluonts/gluonts.torch.model.deepar.estimator.html
        estimator = DeepAREstimator(freq='D', prediction_length=prediction_length, trainer = Trainer(epochs=20))
        predictor = estimator.train(train_ds, num_workers=2)

        valid_ds = PandasDataset.from_long_dataframe(valid, target='target', item_id='ident',
                                                     timestamp='end', freq='D')

        ###############################
                    # metrics
        ###############################
        # forecast_it, ts_it = make_evaluation_predictions(
        #     dataset=valid_ds,
        #     predictor=predictor,
        # )
        # forecasts = list(forecast_it)
        # tss = list(ts_it)
        # evaluator = Evaluator(quantiles=[0.1, 0.5, 0.9])
        # agg_metrics, item_metrics = evaluator(tss, forecasts)
        # # print(json.dumps(agg_metrics, indent=4))
        # mlflow.log_metric("foo", random() + 2)
        #
        mkdir('model')
        predictor.serialize(Path("./model/"))
        mlflow.log_artifacts("model")

def add(df):
    predictor = get_predicator()
    pass

def predict(df):
    # from know to future 30 day
    predictor = get_predicator()
    pass
    ###############################
    # predict predicator.predict?
    ###############################





def get_predicator():
    from gluonts.model.predictor import Predictor
    predictor_deserialized = Predictor.deserialize(Path("./model/"))
    return predictor_deserialized


import pandas as pd
from os.path import exists
from os import mkdir
from gluonts.dataset.pandas import PandasDataset
from gluonts.mx.model.deepar import DeepAREstimator
from gluonts.mx.trainer import Trainer
import numpy as np
from pathlib import Path
import optuna
import mlflow
from gluonts.evaluation import make_evaluation_predictions
from gluonts.evaluation import Evaluator
from gluonts.dataset.field_names import FieldName
def transform_data(df):
    df['end'] = pd.to_datetime(df['end'],format='%Y-%m-%d %H:%M:%S')
    df.drop(columns=['begin'],inplace=True)
    df.set_index('end',inplace=True)
    print(df.head(5))
    df = df.resample('D').mean().interpolate().reset_index()
    df_new = None
    for i in df.columns[:-2]:
        if df_new is None:
            df_new = df[[i,'end']]
            df_new['ident'] = i
            df_new['target'] = df[i]
            df_new.drop(columns=[i],inplace=True)
            continue
        df_temp = df[[i,'end']]
        df_temp['ident'] = i
        df_temp['target'] = df[i]
        df_temp.drop(columns=[i],inplace=True)
        df_new = pd.concat([df_new,df_temp])
    return df_new.dropna().sort_values('end')
remote_server_uri = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(uri=remote_server_uri)
with mlflow.start_run():
    mlflow.gluon.autolog()
    df = transform_data(pd.read_csv('output.csv'))
    train = df.loc[df['end'] < '2023-01-01']
    valid = df.loc[df['end'] >= '2023-01-01']
    train_ds = PandasDataset.from_long_dataframe(train, target='target', item_id='ident',
                                                 timestamp='end', freq='D')
    # https://ts.gluon.ai/stable/api/gluonts/gluonts.torch.model.deepar.estimator.html
    estimator = DeepAREstimator(freq='D', prediction_length=30, trainer = Trainer(epochs=1))
    predictor = estimator.train(train_ds, num_workers=2).as_symbol_block_predictor(dataset=train_ds)

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
    predictor.serialize(Path("./model/"))
    mlflow.log_artifacts("model")

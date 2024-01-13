import pandas as pd
from os.path import exists
from os import mkdir
from gluonts.dataset.pandas import PandasDataset
from gluonts.mx.model.deepar import DeepAREstimator
import numpy as np
from pathlib import Path
#https://www.kaggle.com/code/snnclsr/gluonts-deepar-model-with-validation
def main(json):
    df = pd.DataFrame.from_dict(json,orient='index')
    if exists('model'):
        add(df)
    else:
        create(df)

def create(df):
    train = df.loc[df['end'] < '2021-01-01']
    valid = df.loc[df['end'] >= '2021-01-01']

    train_ds = PandasDataset.from_long_dataframe(train, target='target', item_id='ident',
                                                 timestamp='end', freq='D')
    # https://ts.gluon.ai/stable/api/gluonts/gluonts.torch.model.deepar.estimator.html
    estimator = DeepAREstimator(freq='D', prediction_length=len(valid), num_layers=3)
    # число эпох надо настроить
    predictor = estimator.train(train_ds, num_workers=2)
    pred = list(predictor.predict(train_ds))
    all_preds = list()

    def wmape(y_true, y_pred):
        return np.abs(y_true - y_pred).sum() / np.abs(y_true).sum()

    for item in pred:
        family = item.item_id
        p = item.samples.mean(axis=0)
        p10 = np.percentile(item.samples, 10, axis=0)
        p90 = np.percentile(item.samples, 90, axis=0)
        dates = pd.date_range(start=item.start_date.to_timestamp(), periods=len(p), freq='D')
        family_pred = pd.DataFrame({'end': dates, 'ident': family, 'pred': p, 'p10': p10, 'p90': p90})
        all_preds += [family_pred]
    all_preds = pd.concat(all_preds, ignore_index=True)
    all_preds = all_preds.merge(valid, on=['end', 'ident'], how='left')
    mkdir('model')
    score = wmape(all_preds['target'], all_preds['pred'])
    predictor.serialize(Path("./model/"))

def add(df):
    pass

def predict(df):
    from gluonts.evaluation import make_evaluation_predictions
    df = PandasDataset.from_long_dataframe(pd.DataFrame.from_dict(df,orient='index'), target='target', item_id='ident',
                                                      timestamp='end', freq='D')
    forecast_it, ts_it = make_evaluation_predictions(
        dataset=df,  # test dataset
        predictor=get_predicator(),  # predictor
        num_samples=500,  # number of sample paths we want for evaluation
    )

    return list(ts_it)[0]

def get_predicator():
    from gluonts.model.predictor import Predictor
    predictor_deserialized = Predictor.deserialize(Path("./model/"))
    return predictor_deserialized
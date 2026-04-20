import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


class ProcurementTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_out = X.copy()

        if 'STATUS' in X_out.columns:
            X_out['STATUS'] = X_out['STATUS'].map({'Active': 1, 'Blacklisted': 0}).fillna(0)

        X_out['DELIVERY_DELAY'] = (X_out['RECIEVED_DATE'] - X_out['EXPECTED_DELIVERY_DATE']).dt.days
        X_out['LEAD_TIME'] = (X_out['RECIEVED_DATE'] - X_out['ORDER_DATE']).dt.days
        X_out['IS_WEEKEND'] = X_out['RECIEVED_DATE'].dt.weekday.apply(lambda x: 1 if x >= 5 else 0)

        qty = X_out['QUANTITY'].replace(0, np.nan)
        X_out['DAMAGE_RATE'] = X_out['DAMAGE_QUANTITY'] / qty
        X_out['FILL_RATE'] = X_out['RECEIVED_QUANTITY'] / qty

        cols_to_drop = [
            'PAYMENT_TERMS', 'SKU_CODE', 'ORDER_DATE', 'QUANTITY',
            'RECEIVED_QUANTITY', 'DAMAGE_QUANTITY', 'EXPECTED_DELIVERY_DATE',
            'RECIEVED_DATE', 'TOTAL_ORDERS', 'ADDRESS', 'ID'
        ]

        X_out = X_out.drop(columns=[c for c in cols_to_drop if c in X_out.columns], errors='ignore')

        return X_out.fillna(0)


pipe = Pipeline([
    ('feature_eng', ProcurementTransformer()),
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])


# Example usage (paths should be updated when running)
if __name__ == "__main__":
    df = pd.read_csv('data/vendor.csv')  # placeholder path

    date_cols = ['ORDER_DATE', 'RECIEVED_DATE', 'EXPECTED_DELIVERY_DATE']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    X_processed = pipe.fit_transform(df)

    feature_names = ['STATUS', 'DELIVERY_DELAY', 'LEAD_TIME', 'IS_WEEKEND', 'DAMAGE_RATE', 'FILL_RATE']
    df_master_clean = pd.DataFrame(X_processed, columns=feature_names)

    weights = {
        'FILL_RATE': 0.40,
        'DAMAGE_RATE': 0.30,
        'DELIVERY_DELAY': 0.20,
        'STATUS': 0.10
    }

    df_master_clean['VENDOR_SCORE'] = (
        (df_master_clean['FILL_RATE'] * weights['FILL_RATE']) +
        ((1 - df_master_clean['DAMAGE_RATE']) * weights['DAMAGE_RATE']) +
        ((1 - df_master_clean['DELIVERY_DELAY']) * weights['DELIVERY_DELAY']) +
        (df_master_clean['STATUS'] * weights['STATUS'])
    )

    print("Feature engineering module ready.")
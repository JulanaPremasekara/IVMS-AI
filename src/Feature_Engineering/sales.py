import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


class DemandForecastingTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_out = X.copy()

        if 'ORDER_DATE' in X_out.columns:
            X_out['ORDER_DATE'] = pd.to_datetime(X_out['ORDER_DATE'], errors='coerce')
            X_out['IS_WEEKEND'] = X_out['ORDER_DATE'].dt.weekday.apply(lambda x: 1 if x >= 5 else 0)
            X_out['MONTH'] = X_out['ORDER_DATE'].dt.month

        if 'INITIAL_STOCK' in X_out.columns and 'SALES_QUANTITY' in X_out.columns:
            X_out['STOCK_GAP'] = X_out['INITIAL_STOCK'] - X_out['SALES_QUANTITY']

        if 'IS_ACTIVE' in X_out.columns:
            X_out['IS_ACTIVE'] = X_out['IS_ACTIVE'].map({'TRUE': 1, 'FALSE': 0}).fillna(0).astype(int)

        if 'CATEGORY_NAME' in X_out.columns:
            X_out = pd.get_dummies(X_out, columns=['CATEGORY_NAME'], prefix='CAT')

        cols_to_drop = ['WAREHOUSE_LOCATION', 'SKU_CODE', 'ORDER_DATE', 'ORDER_QUANTITY']
        X_out = X_out.drop(columns=[c for c in cols_to_drop if c in X_out.columns], errors='ignore')

        return X_out.fillna(0)


pipe = Pipeline([
    ('feature_eng', DemandForecastingTransformer()),
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])


# Example usage (paths should be updated when running)
if __name__ == "__main__":
    df = pd.read_csv('data/inventory.csv')  # placeholder path

    X_processed = pipe.fit_transform(df)

    y_raw = df['ORDER_QUANTITY'].values.reshape(-1, 1)
    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y_raw)

    temp_df = DemandForecastingTransformer().transform(df)
    feature_names = temp_df.columns.tolist()

    df_final_clean = pd.DataFrame(X_processed, columns=feature_names)
    df_final_clean['ORDER_QUANTITY'] = y_scaled

    print("Demand feature engineering module ready.")
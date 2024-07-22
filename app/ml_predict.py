import re
import pandas as pd
import numpy as np
import pickle as pk

_model=pk.load(open('./Models/model.pkl', 'rb'))
_encoder=pk.load(open('./Models/encoder.pkl', 'rb'))
_mapping=pk.load(open('./Models/mapping.pkl', 'rb'))
_scaler=pk.load(open('./Models/scaler.pkl', 'rb'))

class property_prediction:
    def __init__(self):
        self._bedrooms = 0
        self._bathrooms = 0
        self._den = 0
        self._latitude = None
        self._longitude = None
        self._postalcode = ""
        self._neighborhood = ""
        self._df=None
        self._rental_price=None

    def set_bedrooms(self, bedrooms):
        self._bedrooms = bedrooms
        return self
    def set_bathrooms(self, bathrooms):
        self._bathrooms = bathrooms
        return self
    def set_den(self, den):
        self._den = den
        return self
    def set_latitude(self, latitude):
        self._latitude = latitude
        return self
    def set_longitude(self, longitude):
        self._longitude = longitude
        return self
    def set_postalcode(self, postalcode):
        self._postalcode = postalcode
        return self
    def find_neighborhood(self,map=_mapping):
        try:
            prefix = self._postalcode[:3]
            if prefix not in map:
                self._neighborhood=f"Neighborhood 0"
                return self
            self._neighborhood = map[prefix]
            return self
        except:
            print("Please set postal code first before finding neighborhood")

    def build_df(self):
        data = {"Bedroom": [self._bedrooms],
                "Bathroom": [self._bathrooms],
                "Den": [self._den],
                "Lat": [self._latitude],
                "Long": [self._longitude],
                "Postalcode": [self._postalcode],
                "Neighborhood": [self._neighborhood]}
        self._df = pd.DataFrame(data)
        return self

    def encode_neighborhood(self,encoder=_encoder):
        matrix = encoder.transform(self._df[["Neighborhood"]])
        # encoder_feature_names = encoder.get_feature_names_out()
        df_encoded = pd.DataFrame(data=matrix)#, columns=encoder_feature_names)
        self._df = pd.merge(self._df, df_encoded, left_index=True, right_index=True)
        self._df.drop(columns=["Neighborhood"], inplace=True)
        self._df.columns=self._df.columns.astype(str)
        return self

    def scale_features(self,scaler=_scaler):
        features_to_scale = ['Bedroom', 'Bathroom', 'Den', 'Lat', 'Long']
        self._df[features_to_scale] = scaler.transform(self._df[features_to_scale])
        return self

    def find_rental_price(self,model=_model):
        df=self._df.drop(columns=["Postalcode"])
        self._rental_price=model.predict(df)
        return self















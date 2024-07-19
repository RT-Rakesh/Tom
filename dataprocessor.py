import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import re


class DataProcessor:
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def parse_address(self, address):
        street_number_pattern = r'^(\d+)'
        street_name_pattern = r'^\d+\s+(.+?),'
        city_province_pattern = r',\s*([A-Za-z\s]+),\s*([A-Za-z]{2})'
        postal_code_pattern = r'([A-Za-z]\d[A-Za-z] \d[A-Za-z]\d)'
        country_pattern = r'Canada$'

        street_number = re.search(street_number_pattern, address)
        street_name = re.search(street_name_pattern, address)
        city_province = re.search(city_province_pattern, address)
        postal_code = re.search(postal_code_pattern, address)
        country = re.search(country_pattern, address)

        street_number = street_number.group(1).strip() if street_number else ''
        street_name = street_name.group(1).strip() if street_name else ''
        city = city_province.group(1).strip() if city_province else ''
        province = city_province.group(2).strip() if city_province else ''
        postal_code = postal_code.group(1).strip() if postal_code else ''
        country = 'Canada' if country else ''

        return street_number, street_name, city, province, postal_code, country

    def categorize_postal_codes(self, postal_codes):
        neighborhood_mapping = {}
        neighborhood_counter = 1
        categorized_neighborhoods = []

        for postal_code in postal_codes:
            prefix = postal_code[:3]

            if prefix not in neighborhood_mapping:
                neighborhood_mapping[prefix] = f"Neighborhood {neighborhood_counter}"
                neighborhood_counter += 1

            categorized_neighborhoods.append(neighborhood_mapping[prefix])
        return categorized_neighborhoods

    def clean_data(self):
        self.data['Street Number'], self.data['Street'], self.data['City'], self.data['Province'], self.data[
            'Postal Code'], self.data['Country'] = zip(*self.data['Address'].apply(self.parse_address))

        self.data['Price'] = self.data['Price'].str.replace('$', '').str.replace(',', '').astype(float)
        self.data = self.data.drop(columns=['Address', 'Street Number', 'Street', 'City', 'Province', 'Country'])

        for column in self.data.columns:
            if self.data[column].dtype == 'object':
                self.data[column] = self.data[column].replace(r'^\s*$', np.nan, regex=True)

        self.data = self.data.dropna()

        postal_codes = self.data['Postal Code'].tolist()
        neighborhoods = self.categorize_postal_codes(postal_codes)
        self.data['Neighborhood'] = neighborhoods

        self.data = self.data[self.data['Price'] <= 10000]

    def transform_data(self):
        categorical_features = ["Neighborhood"]
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        matrix = encoder.fit_transform(self.data[categorical_features])
        encoder_feature_names = encoder.get_feature_names_out()
        df_encoded = pd.DataFrame(data=matrix, columns=encoder_feature_names)
        self.data = pd.merge(self.data, df_encoded, left_index=True, right_index=True)
        self.data.drop(columns=categorical_features, inplace=True)

        features_to_scale = ['Bedroom', 'Bathroom', 'Den', 'Lat', 'Long', 'Price']
        scaler = StandardScaler()
        self.data[features_to_scale] = scaler.fit_transform(self.data[features_to_scale])

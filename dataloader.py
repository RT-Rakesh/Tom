import pandas as pd

class DataLoader:
    def load_data(self, file_path):
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

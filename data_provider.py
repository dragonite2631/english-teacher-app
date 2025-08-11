# file: data_provider.py
import pandas as pd
import os

class UnitDataProvider:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder

    def get_unit_data(self, unit_number: int) -> dict | None:
        filename = f"unit_{unit_number}_data.csv"
        filepath = os.path.join(self.data_folder, filename)
        try:
            df = pd.read_csv(filepath)
            return df.iloc[0].to_dict()
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file dữ liệu tại '{filepath}'")
            return None
        except Exception as e:
            print(f"Lỗi khi đọc file '{filepath}': {e}")
            return None
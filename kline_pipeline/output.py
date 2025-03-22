import os
import pandas as pd

class KLineSaver:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, kline, symbol, period):
        filename = os.path.join(self.output_dir, f'{symbol}_{period}.csv')
        tmp_file = filename + ".tmp"
        if os.path.exists(filename):
            print(f"已存在，跳过：{filename}")
            return
        kline.to_csv(tmp_file, index=False)
        os.rename(tmp_file, filename)
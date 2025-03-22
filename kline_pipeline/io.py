import dask.dataframe as dd
import pandas as pd

def load_csv_with_dask(file_path):
    """使用 Dask 加速加载 CSV 文件并转换为 Pandas DataFrame"""
    ddf = dd.read_csv(file_path, dtype={
        'szWindCode': 'string',
        'nTime': 'int64',
        'nTradingDay': 'int32',
        'nMatch': 'float32'
    }, blocksize="64MB", assume_missing=True)
    return ddf.compute()
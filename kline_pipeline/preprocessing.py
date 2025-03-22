import pandas as pd

class TimeParser:
    """负责解析 nTime 为 datetime"""
    def parse(self, df):
        nTime_str = df['nTime'].astype(str).str.zfill(9)
        hh = nTime_str.str[:2].astype(int)
        mm = nTime_str.str[2:4].astype(int)
        ss = nTime_str.str[4:6].astype(int)
        ms = nTime_str.str[6:9].astype(int)

        df['nTime'] = pd.to_datetime(df['nTradingDay'].astype(str), format='%Y%m%d') + \
                      pd.to_timedelta(hh, unit='h') + \
                      pd.to_timedelta(mm, unit='m') + \
                      pd.to_timedelta(ss, unit='s') + \
                      pd.to_timedelta(ms, unit='ms')
        return df
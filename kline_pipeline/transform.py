class KLineResampler:
    """负责按周期重采样生成K线数据"""
    def resample(self, df, period):
        df = df.set_index('nTime')
        kline = df.resample(period).agg({
            'nMatch': ['first', 'max', 'min', 'last'],
            'nTradingDay': 'first'
        }).dropna()
        kline.columns = ['open', 'high', 'low', 'close', 'nTradingDay']
        kline.reset_index(inplace=True)
        return kline
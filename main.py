import argparse
import time
from multiprocessing import Pool, cpu_count

from kline_pipeline.io import load_csv_with_dask
from kline_pipeline.preprocessing import TimeParser
from kline_pipeline.transform import KLineResampler
from kline_pipeline.output import KLineSaver
from kline_pipeline.state import KLineStatusTracker


def process_symbol_batch(batch, periods, saver, tracker):
    resampler = KLineResampler()
    for symbol, group in batch:
        for period in periods:
            if tracker.is_processed(symbol, period):
                print(f"已记录，跳过：{symbol} - {period}")
                continue
            try:
                kline = resampler.resample(group.copy(), period)
                saver.save(kline, symbol, period)
                tracker.mark_processed(symbol, period)
                print(f"{symbol} - {period} saved")
            except Exception as e:
                print(f"{symbol} - {period} error: {e}")


def batch_symbols(df, batch_size=500):
    batch = []
    for symbol, group in df.groupby('szWindCode'):
        batch.append((symbol, group))
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='kline_output')
    parser.add_argument('--periods', nargs='+', default=['1min', '5min', '10min', '30min'])
    args = parser.parse_args()

    print("使用 Dask 加速读取 CSV...")
    df = load_csv_with_dask(args.input)

    print("解析时间字段...")
    df = TimeParser().parse(df)

    tracker = KLineStatusTracker()
    saver = KLineSaver(args.output)

    print("启动多进程处理...")
    start_time = time.time()

    batches = list(batch_symbols(df))
    with Pool(processes=cpu_count()) as pool:
        for batch in batches:
            pool.apply_async(process_symbol_batch, args=(batch, args.periods, saver, tracker))
        pool.close()
        pool.join()

    elapsed = time.time() - start_time
    m, s = divmod(elapsed, 60)
    print(f"全部处理完成，总耗时：{int(m)} 分 {s:.2f} 秒")


if __name__ == '__main__':
    main()
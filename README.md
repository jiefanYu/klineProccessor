# K-Line Pipeline 工具

一个用于 A 股市场数据的高性能 K 线合成工具，支持：

- 支持 1min / 5min / 10min / 30min 等任意周期
- 基于 Dask + 多进程加速大数据处理
- SQLite 状态跟踪，支持断点续跑
- Exactly-once 写入逻辑，防止重复生成

## 安装方式
```bash
pip install -e .
```

## 🚀 使用方式
```bash
python main.py \
  --input ./md_20221110.csv \
  --output ./kline_output \
  --periods 1min 5min 10min 30min
```

## 模块说明
| 模块 | 功能 |
|------|------|
| `kline_pipeline.io` | 使用 Dask 读取大型 CSV 文件 |
| `kline_pipeline.preprocessing` | 转换时间字段为 datetime 类型 |
| `kline_pipeline.transform` | 使用 pandas `resample` 合成 K 线 |
| `kline_pipeline.output` | 写入本地 CSV，确保原子写 |
| `kline_pipeline.state` | SQLite 记录每个 symbol+period 的处理状态 |

## 进阶特性
- 可随时中断，重启自动跳过已完成项
- 可集成进 CI / 自动化任务中
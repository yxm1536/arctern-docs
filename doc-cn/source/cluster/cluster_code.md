# 代码迁移

Arctern 是一个快速可扩展的时空数据分析框架。可扩展性的其中一个挑战是从单机到集群和云，跨平台实现一致的数据分析和处理接口。我们基于 Spark 开发 `GeoSeries` 和 `GeoDataFame` 的分布式版本并借助 Koalas 接口实现和单机版一致的 `GeoDataFrame` 和 `GeoSeries` 接口。

本文列举一些典型的代码示例，展示如何将单机版本下的代码进行微小修改即可在分布式环境下运行。


## 快速开始
单机版本下的 `GeoSeries` 和 `GeoDataFrame` 位于 `arctern` Python 包，对应的分布式版本的数据结构则位于 `arctern_spark` Python 包。
因此大多数情况下只需要将 `GeoSeries` 和 `GeoDataFrame` 的 import 方式修改即可。就像如下代码所示：

```python
# 单机 Python 环境
from arctern.geoseries import GeoSeries
data = ["POLYGON((0 0,1 0,1 1,0 1,0 0))",
        "POLYGON((1 3, 6 3, 3 6, 1 3))",
        "MULTILINESTRING ((0 0,4 0),(5 0,6 0))",
        "POLYGON((0 0,0 8,8 8,8 0,0 0))"]

data = GeoSeries(data)
rst = data.area
print(rst)
```

```python
# 分布式 Spark 环境
from arctern_spark.geoseries import GeoSeries
data = ["POLYGON((0 0,1 0,1 1,0 1,0 0))",
        "POLYGON((1 3, 6 3, 3 6, 1 3))",
        "MULTILINESTRING ((0 0,4 0),(5 0,6 0))",
        "POLYGON((0 0,0 8,8 8,8 0,0 0))"]

data = GeoSeries(data)
rst = data.area
print(rst)
```

## 构造

`arctern.GeoSeries` 可根据 `list`, `koalas.GeoSereis` 以及 `pandas.GeoSeries` 来构造。

```python
from arctern_spark.geoseries import GeoSeries
import databricks.koalas as ks
import pandas as pd

list_data = ["POLYGON((0 0,1 0,1 1,0 1,0 0))", "POLYGON((0 0,0 8,8 8,8 0,0 0))"]
pser = pd.Series(list_data, name="geometry_p")
kser = ks.Series(list_data, name="geometry_k")

aser = GeoSeries(list_data, name="geometry")
print(aser.area)
aser = GeoSeries(pser)
print(aser.area)
aser = GeoSeries(kser)
print(aser.area)
```


## 数据处理



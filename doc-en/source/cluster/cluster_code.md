# Code migration

Arctern is a fast and scalable spatiotemporal data analysis framework. A challenge of scalability is to implement consistent data analysis and processing APIs across platforms from standalone systems to clustered systems and clouds. With the help of the Koalas APIs, We have developed a Spark-based distributed version of GeoSeries and GeoDataFame, which are similar to their counterparts in the standalone version.

This article describes how to modify the codes in the standalone version so that you can run them in a distributed environment.

The standalone GeoSeries and GeoDataFrame are located in the `arctern` Python package, and the corresponding distributed classes are located in the `arctern_spark` Python package. In most cases, you only need to modify the import methods of GeoSeries and GeoDataFrame to migrate your codes:

```python
>>> # Standalone Python environment
>>> from arctern.geoseries import GeoSeries
>>> data = ["POLYGON((0 0,1 0,1 1,0 1,0 0))",
...     "POLYGON((1 3, 6 3, 3 6, 1 3))",
...     "MULTILINESTRING ((0 0,4 0),(5 0,6 0))",
...     "POLYGON((0 0,0 8,8 8,8 0,0 0))"]
>>> data = GeoSeries(data)
>>> rst = data.area
>>> print(rst)
```

```python
# Distributed Spark environment
>>> from arctern_spark.geoseries import GeoSeries
>>> data = ["POLYGON((0 0,1 0,1 1,0 1,0 0))",
...     "POLYGON((1 3, 6 3, 3 6, 1 3))",
...     "MULTILINESTRING ((0 0,4 0),(5 0,6 0))",
...     "POLYGON((0 0,0 8,8 8,8 0,0 0))"]
>>> data = GeoSeries(data)
>>> rst = data.area
>>> print(rst)
```

`arctern_spark.GeoSeries` can be constructed from `list-like` type data and `koalas.Series`. `list-like` types include list, tuple, set, numpy.array and pandas.Series.

```python
>>> from arctern_spark.geoseries import GeoSeries
>>> import databricks.koalas as ks
>>> import pandas as pd
>>>
>>> list_data = ["POLYGON((0 0,1 0,1 1,0 1,0 0))", "POLYGON((0 0,0 8,8 8,8 0,0 0))"]
>>> pser = pd.Series(list_data, name="geometry_p")
>>> kser = ks.Series(list_data, name="geometry_k")
>>>
>>> aser = GeoSeries(list_data, name="geometry")
>>> print(aser.area)
>>> aser = GeoSeries(pser)
>>> print(aser.area)
>>> aser = GeoSeries(kser)
>>> print(aser.area)
```


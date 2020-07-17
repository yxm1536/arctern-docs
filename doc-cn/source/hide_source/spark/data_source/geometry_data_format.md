# Geometry 数据格式

Arctern 在导入和导出数据时支持 [Well Know Text (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) 和 [Well Know Binary (WKB)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) 两种格式的几何体数据。相较于 WKB 格式的数据，WKT 格式的数据更方便人工阅读，但是计算机对其处理的效率较低并且占用的存储空间也更大。

目前，Arctern API 仅支持 WKB 格式的几何体数据作为输入参数和返回参数。如下例所示，如果数据源使用 WKT 格式的数据，在导入数据后需要调用 `ST_GeomFromText` 函数将数据转换为 WKB 格式；相应的，在导出数据后也需要调用 `ST_GeomFromText` 函数将数据转换回 WKT 格式。数据形式的转换将带来额外的数据开销。因此，如果你对几何体数据的可读性要求不高，建议将数据存储为 WKB 格式。

## 示例

导入和导出 WKT 格式的数据：

```python
'''
CSV 文件内容：
geos
POINT (30 10)
POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))
POLYGON ((1 2, 3 4, 5 6, 1 2))
POLYGON ((1 1, 3 1, 3 3, 1 3, 1 1))
'''
>>> from pyspark.sql import SparkSession
>>> from arctern_pyspark import register_funcs
>>>
>>> # 创建 SparkSession 并对其进行配置
>>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
>>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
>>>
>>> # 注册 Arctern-Spark 提供的函数
>>> register_funcs(spark_session)
>>>
>>> # 导入数据
>>> df = spark_session.read.format('csv').options(header='true',sep='|').load("/path/to/geos.csv")
>>>
>>> # 为导入数据创建数据表 ‘geos’ 并对其进行处理
>>> df.createOrReplaceTempView("geos")
>>>
>>> # 在处理数据进行之前，使用 ST_GeomFromText 将数据转换为 WKB 格式；在导出数据之前，使用 ST_AsText 将数据转换为 WKT 格式
>>> make_valid_df = spark_session.sql("select ST_AsText(ST_MakeValid(ST_GeomFromText(geos))) from geos")
>>>
>>> # 导出数据
>>> df.select("geos").write.save("/path/to/new_geos.csv", format="csv")
```

导入和导出 WKB 格式的数据：

```python
'''
CSV 文件内容：
geos
b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00$@'
b'\x01\x03\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x00D@\x00\x00\x00\x00\x00\x00D@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00\x00\x00D@\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00$@'
b'\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@\x00\x00\x00\x00\x00\x00\x14@\x00\x00\x00\x00\x00\x00\x18@\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@'
b'\x01\x03\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\xf0?'
'''
>>> from pyspark.sql import SparkSession
>>> from arctern_pyspark import register_funcs
>>>
>>> # 创建 SparkSession 并对其进行配置
>>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
>>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
>>>
>>> # 注册 Arctern-Spark 提供的函数
>>> register_funcs(spark_session)
>>>
>>> # 数据导入
>>> df = spark_session.read.format('csv').options(header='true',sep='|').load("/path/to/geos.csv")
>>>
>>> # 为导入数据创建数据表 ‘geos’ 并对其进行处理
>>> df.createOrReplaceTempView("geos")
>>>
>>> # 无需进行数据格式转换
>>> make_valid_df = spark_session.sql("select ST_MakeValid(geos) from geos")
>>>
>>> # 数据导出
>>> df.select("geos").write.save("/path/to/new_geos.csv", format="csv")
```
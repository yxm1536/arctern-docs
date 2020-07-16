# 文件的导入与导出

Arctern RESTful 服务借助 Spark 的文件读写功能完成数据的导入和导出。Spark 支持多种数据格式文件导入，以下是针对 CSV、PARQUET、JSON、ORC 等数据格式文件的导入导出例子。更多的文件格式支持请查看 [Spark 官方文档](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html)

```python
>>> # 导入 CSV 文件，导出 PARQUET 文件
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
>>> # 数据导入
>>> df = spark_session.read.format('csv').options(header='true',sep='|').load("/path/to/geos.csv")
>>> df.show(100,0)
+---------------------------------------------+
|geos                                         |
+---------------------------------------------+
|POINT (30 10)                                |
|POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))|
|POLYGON ((1 2, 3 4, 5 6, 1 2))               |
|POLYGON ((1 1, 3 1, 3 3, 1 3, 1 1))          |
+---------------------------------------------+
>>> 
>>> # 为导入数据创建数据表 ‘simple’ 并对其进行处理
>>> df.createOrReplaceTempView("simple")
>>> spark_session.sql("select ST_IsSimple(ST_GeomFromText(geos)) from simple").show(100,0)
+----------------------------------+                                            
|ST_IsSimple(ST_GeomFromText(geos))|
+----------------------------------+
|true                              |
|true                              |
|false                             |
|true                              |
+----------------------------------+
>>> 
>>> # 数据导出
>>> df.select("geos").write.save("/path/to/geos.parquet", format="parquet")
>>> 
>>> # 导入 PARQUET 文件，导出 JSON 文件
>>> df = spark_session.read.format('parquet').options(header='true',sep='|').load("/path/to/geos.parquet")
>>> df.show(100,0)
+---------------------------------------------+
|geos                                         |
+---------------------------------------------+
|POINT (30 10)                                |
|POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))|
|POLYGON ((1 2, 3 4, 5 6, 1 2))               |
|POLYGON ((1 1, 3 1, 3 3, 1 3, 1 1))          |
+---------------------------------------------+
>>>
>>> df.createOrReplaceTempView("simple")
>>> spark_session.sql("select ST_IsSimple(ST_GeomFromText(geos)) from simple").show(100,0)
+----------------------------------+                                            
|ST_IsSimple(ST_GeomFromText(geos))|
+----------------------------------+
|true                              |
|true                              |
|false                             |
|true                              |
+----------------------------------+
>>> 
>>> df.select("geos").write.save("/path/to/geos.json", format="json")
>>> 
>>> # 导入 JSON 文件，导出 ORC 文件
>>> df = spark_session.read.format('json').options(header='true',sep='|').load("/path/to/geos.json")
>>> df.show(100,0)
+---------------------------------------------+
|geos                                         |
+---------------------------------------------+
|POINT (30 10)                                |
|POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))|
|POLYGON ((1 2, 3 4, 5 6, 1 2))               |
|POLYGON ((1 1, 3 1, 3 3, 1 3, 1 1))          |
+---------------------------------------------+
>>> 
>>> df.createOrReplaceTempView("simple")
>>> spark_session.sql("select ST_IsSimple(ST_GeomFromText(geos)) from simple").show(100,0)
+----------------------------------+                                            
|ST_IsSimple(ST_GeomFromText(geos))|
+----------------------------------+
|true                              |
|true                              |
|false                             |
|true                              |
+----------------------------------+
>>> 
>>> df.write.save("/path/to/geos.orc", format="orc")
>>> 
>>> # 导入 ORC 文件，导出 CSV 文件
>>> df = spark_session.read.format('orc').options(header='true',sep='|').load("/path/to/geos.orc")
>>> df.show(100,0)
+---------------------------------------------+
|geos                                         |
+---------------------------------------------+
|POINT (30 10)                                |
|POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))|
|POLYGON ((1 2, 3 4, 5 6, 1 2))               |
|POLYGON ((1 1, 3 1, 3 3, 1 3, 1 1))          |
+---------------------------------------------+
>>> 
>>> df.createOrReplaceTempView("simple")
>>> spark_session.sql("select ST_IsSimple(ST_GeomFromText(geos)) from simple").show(100,0)
+----------------------------------+                                            
|ST_IsSimple(ST_GeomFromText(geos))|
+----------------------------------+
|true                              |
|true                              |
|false                             |
|true                              |
+----------------------------------+
>>> 
>>> df.select("geos").write.save("/path/to/geos.csv", format="csv")
```
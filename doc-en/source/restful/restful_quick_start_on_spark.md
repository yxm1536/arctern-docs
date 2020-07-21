# 快速开始（PySpark 后台）

本文以纽约出租车数据集为例，以 PySpark 作为数据处理后台，说明如何通过 Arctern RESTful API 完成数据的导入、运算和展示。

> **注意：** 本章所有示例代码均默认在 Python 3.7 环境中运行。若要在其他 Python 环境下运行，你可能需要适当修改代码内容。

## 服务器端的启动和配置

### 服务器启动

在调用 Arctern RESTful API 之前请先启动服务，具体步骤见 [服务器启动](../install/webserver_installation_config.md)。

### 数据准备

在后续示例中，你需要使用纽约出租车数据集。该数据集包含 2009 年纽约市出租车的运营记录，各字段的含义如下：

| 名称                  | 含义                       | 类型   |
| :-------------------- | :------------------------- | :----- |
| VendorID              | 运营商名称                 | string |
| tpep_pickup_datetime  | 上车时间                   | string |
| tpep_dropoff_datetime | 下车时间                   | string |
| passenger_count       | 乘客数量                   | long   |
| trip_distance         | 行程距离                   | double |
| pickup_longitude      | 上车地点的经度              | double |
| pickup_latitude       | 上车地点的纬度              | double |
| dropoff_longitude     | 下车地点的经度              | double |
| dropoff_latitude      | 下车地点的纬度              | double |
| fare_amount           | 行程费用                   | double |
| tip_amount            | 小费                       | double |
| total_amount          | 总费用                     | double |
| buildingid_pickup     | 上车地点所在建筑的 id      | long   |
| buildingid_dropoff    | 下车地点所在建筑的 id      | long   |
| buildingtext_pickup   | 上车地点所在建筑的轮廓描述 | string |
| buildingtext_dropoff  | 下车地点所在建筑的轮廓描述 | string |

> **注意：** 该数据集有 200000 行，其中时间格式为：`yyyy-MM-dd HH:mm::ss XXXXX`，如“2009-04-12 03:16:33 +00:00”。

下载纽约出租车数据集：

```bash
$ wget https://media.githubusercontent.com/media/arctern-io/arctern-resources/benchmarks/benchmarks/dataset/nyc_taxi/0_2M_nyc_taxi_and_building/0_2M_nyc_taxi_and_building.csv
```

查看是否下载成功：

```bash
$ wc -l 0_2M_nyc_taxi_and_building.csv
```

### 安装依赖

本文示例代码使用 Python 的 `requests` 库调用 Arctern RESTful API，执行以下命令安装 `requests`：

```bash
$ pip install requests
```

## API 调用

下述示例中，假设服务器 IP 地址为 `127.0.0.1`，RESTful 服务端口为`8080`。如果你在启动 arctern-server 时指定了 IP 与端口，则使用指定的 IP 与端口。

### 数据导入

使用 `/loadfile` 接口导入纽约出租车数据集，将其对应的数据表命名为`raw_data`。

> **注意：** 你需要将示例中的 `file_path` 替换为数据文件的绝对路径。

```python
>>> import requests
>>> import json
>>> 
>>> file_path = "/example/data/0_2M_nyc_taxi_and_building.csv"
>>> payload = {
... "tables": [
...     {
...         "name": "raw_data",
...         "format": "csv",
...         "path": file_path,
...         "options": {
...             "header": "True",
...             "delimiter": ","
...         },
...         "schema": [
...             {"VendorID": "string"},
...             {"tpep_pickup_datetime": "string"},
...             {"tpep_dropoff_datetime": "string"},
...             {"passenger_count": "long"},
...             {"trip_distance": "double"},
...             {"pickup_longitude": "double"},
...             {"pickup_latitude": "double"},
...             {"dropoff_longitude": "double"},
...             {"dropoff_latitude": "double"},
...             {"fare_amount": "double"},
...             {"tip_amount": "double"},
...             {"total_amount": "double"},
...             {"buildingid_pickup": "long"},
...             {"buildingid_dropoff": "long"},
...             {"buildingtext_pickup": "string"},
...             {"buildingtext_dropoff": "string"}
...         ]
...     }
... ]
... }
>>> 
>>> r = requests.post(url="http://127.0.0.1:8080/loadfile", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
>>> r.json()
{
    'code': 200,
    'message': 'load table successfully!',
    'status': 'success'
}
```

### 查询数据表信息

你已经在后台创建了一张名为 `raw_data` 的数据表。接着，使用 `/table/schema` 接口可查询该表中各字段的名称以及对应的数据类型。

```python
>>> import requests
>>> r = requests.get(url="http://127.0.0.1:8080/table/schema?table=raw_data")
>>> r.json()
{
    "code": 200,
    "schema": [
        {
            "col_name": "VendorID",
            "data_type": "string"
        },
        {
            "col_name": "tpep_pickup_datetime",
            "data_type": "string"
        },
        {
            "col_name": "tpep_dropoff_datetime",
            "data_type": "string"
        },
        {
            "col_name": "passenger_count",
            "data_type": "bigint"
        },
        {
            "col_name": "trip_distance",
            "data_type": "double"
        },
        {
            "col_name": "pickup_longitude",
            "data_type": "double"
        },
        {
            "col_name": "pickup_latitude",
            "data_type": "double"
        },
        {
            "col_name": "dropoff_longitude",
            "data_type": "double"
        },
        {
            "col_name": "dropoff_latitude",
            "data_type": "double"
        },
        {
            "col_name": "fare_amount",
            "data_type": "double"
        },
        {
            "col_name": "tip_amount",
            "data_type": "double"
        },
        {
            "col_name": "total_amount",
            "data_type": "double"
        },
        {
            "col_name": "buildingid_pickup",
            "data_type": "bigint"
        },
        {
            "col_name": "buildingid_dropoff",
            "data_type": "bigint"
        },
        {
            "col_name": "buildingtext_pickup",
            "data_type": "string"
        },
        {
            "col_name": "buildingtext_dropoff",
            "data_type": "string"
        }
    ],
    "status": "success",
    "table": "raw_data"
}
```

### SQL 查询

使用 `/query` 接口可完成数据表的创建、查询和删除操作。

#### 创建数据表

将 `raw_data` 数据表中的时间信息从 String 类型转换为 Timestamp 类型，并移除与后续操作无关的字段，保存为一张新的 `nyc_taxi` 数据表。

```python
>>> import requests
>>> import json
>>> 
>>> sql = "create table nyc_taxi as (select VendorID, to_timestamp(tpep_pickup_datetime,'yyyy-MM-dd HH:mm:ss XXXXX') as tpep_pickup_datetime, to_timestamp(tpep_dropoff_datetime,'yyyy-MM-dd HH:mm:ss XXXXX') as tpep_dropoff_datetime, passenger_count, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, fare_amount, tip_amount, total_amount, buildingid_pickup, buildingid_dropoff, buildingtext_pickup, buildingtext_dropoff from raw_data where (pickup_longitude between -180 and 180) and (pickup_latitude between -90 and 90) and (dropoff_longitude between -180 and 180) and  (dropoff_latitude between -90 and 90))"
>>> payload = {
... "input_data": {
... "sql": sql
... },
... "collect_result": "0"
... }
>>> 
>>> r = requests.post(url="http://127.0.0.1:8080/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
>>> r.json()
{
    'code': 200,
    'message': 'execute sql successfully!',
    'status': 'success'
}
```

#### 查询数据

查询 `nyc_taxi` 数据表的行数。

```python
>>> import requests
>>> import json
>>> 
>>> sql = "select count(*) as num_rows from nyc_taxi"
>>> payload = { 
... "input_data":{
...     "sql": sql
... },
... "collect_result": "0"
... }
>>> 
>>> r = requests.post(url="http://127.0.0.1:8080/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
>>> r.json()
{
    'code': 200,
    'message': 'execute sql successfully!',
    'result': [
        {'num_rows': 199999}
    ],
    'status': 'success'
}
```

#### 删除数据表

删除原始的 `raw_data` 数据表。

> **注意：** `Arctern RESTful` 服务不会主动删除数据表，请务必删除不再使用的数据表释放服务器资源。

```python
>>> import requests
>>> import json
>>> 
>>> sql = "drop table if exists raw_data"
>>> payload = {
... "input_data":{
...     "sql": sql
... },
... "collect_result": "0"
... }
>>> 
>>> r = requests.post(url="http://127.0.0.1:8080/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
>>> r.json()
{
    'code': 200,
    'message': 'execute sql successfully!',
    'status': 'success'
}
```

### 绘制热力图

使用 `/heatmap` 接口根据乘客的下车地点以及行程费用绘制热力图。其中，费用高的区域为红色，费用低的区域为绿色。热力图的具体参数说明请见 [热力图 RESTful API 说明](./api/function/heatmap.html)。

```python
>>> import requests
>>> import json
>>> 
>>> payload = {
... "input_data": {
...     "sql": "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi GROUP BY point"
... },
... "params": {
...     "width": 512,
...     "height": 448,
...     "bounding_box": [
...         -74.01556543545699,
...         40.69354738164881,
...         -73.9434424136598,
...         40.780921656427836
...     ],
...     "coordinate_system": "EPSG:4326",
...     "map_zoom_level": 10,
...     "aggregation_type": "sum"
... }
... }
>>> 
>>> r = requests.post(url="http://127.0.0.1:8080/heatmap", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
>>> 
>>> import base64
>>> with open("/tmp/heatmap.png", "wb") as f:
...     f.write(base64.b64decode(r.json()['result']))
```

热力图的绘制结果如下：

![热力图](./img/heatmap_spark.png)

### 删除数据表

使用 `query` 接口删除 `nyc_taxi` 数据表，释放服务器资源。

> **注意：** `Arctern RESTful` 服务不会主动删除数据表，请务必删除不再使用的数据表释放服务器资源。

```python
>>> import requests
>>> import json
>>> 
>>> sql = "drop table if exists nyc_taxi"
>>> payload = {
... "input_data": {
...    "sql": sql 
... },
... "collect_result": "0"
... }
>>> 
>>> r = requests.post(url="http://127.0.0.1:8080/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
>>> r.json()
{
    'code': 200,
    'message': 'execute sql successfully!',
    'status': 'success' 
}
```
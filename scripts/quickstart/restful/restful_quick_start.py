#!/usr/bin/env python

import requests
import json
import base64

print("请输入 Arctern Server 的 IP：", end='')
host = input()
print("请输入 Arctern Server 的端口号：", end='')
port = input()
url_prefix = "http://" + host + ":" + port

print("创建作用域")
payload = {
    "scope": "nyc_taxi",
}
r = requests.post(url=url_prefix + "/scope", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# print(r.json())

print("加载数据文件")
file_path = "/example/data/0_2M_nyc_taxi_and_building.csv"
print("请输入数据文件所在的绝对路径：", end='')
file_path = input()
payload = {
    "scope": "nyc_taxi",
    "tables": [
        {
            "name": "raw_data",
            "format": "csv",
            "path": file_path,
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [
                {"VendorID": "string"},
                {"tpep_pickup_datetime": "string"},
                {"tpep_dropoff_datetime": "string"},
                {"passenger_count": "long"},
                {"trip_distance": "double"},
                {"pickup_longitude": "double"},
                {"pickup_latitude": "double"},
                {"dropoff_longitude": "double"},
                {"dropoff_latitude": "double"},
                {"fare_amount": "double"},
                {"tip_amount": "double"},
                {"total_amount": "double"},
                {"buildingid_pickup": "long"},
                {"buildingid_dropoff": "long"},
                {"buildingtext_pickup": "string"},
                {"buildingtext_dropoff": "string"}
            ]
        }
    ]
}
r = requests.post(url=url_prefix + "/loadfile", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# print(r.json())

print("查询原始表 schema")
r = requests.get(url=url_prefix + "/table/schema?scope=nyc_taxi&table=raw_data")
# print(r.json())

print("SQL 查询")

print("case 1: 创建表 nyc_taxi")
payload = {
    "scope": "nyc_taxi",
    "session": "spark",
    "sql": "create table nyc_taxi as (select VendorID, to_timestamp(tpep_pickup_datetime,'yyyy-MM-dd HH:mm:ss XXXXX') as tpep_pickup_datetime, to_timestamp(tpep_dropoff_datetime,'yyyy-MM-dd HH:mm:ss XXXXX') as tpep_dropoff_datetime, passenger_count, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, fare_amount, tip_amount, total_amount, buildingid_pickup, buildingid_dropoff, buildingtext_pickup, buildingtext_dropoff from raw_data where (pickup_longitude between -180 and 180) and (pickup_latitude between -90 and 90) and (dropoff_longitude between -180 and 180) and  (dropoff_latitude between -90 and 90))",
    "collect_result": "0"
}
r = requests.post(url=url_prefix + "/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# print(r.json())

print("case 2: 查询表 nyc_taxi 的行数")
sql = "select count(*) as num_rows from nyc_taxi"
payload = {
    "scope": "nyc_taxi",
    "sql": sql,
    "collect_result": "1"
}
r = requests.post(url=url_prefix + "/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# print(r.json())

print("case 3: 删除原始表 raw_data")
sql = "drop table if exists raw_data"
payload = {"scope": "nyc_taxi", "sql": sql, "collect_result": "0"}
r = requests.post(url=url_prefix + "/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# print(r.json())


print("绘制点图")
payload = {
    "scope": "nyc_taxi",
    "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point from nyc_taxi where ST_Within(ST_Point(pickup_longitude, pickup_latitude), ST_GeomFromText('POLYGON ((-73.998427 40.730309, -73.954348 40.730309, -73.954348 40.780816 ,-73.998427 40.780816, -73.998427 40.730309))'))",
    "params": {
         "width": 1024,
         "height": 896,
        "bounding_box": [-73.998427, 40.730309, -73.954348, 40.780816],
        "coordinate_system": "EPSG:4326",
        "point_color": "#2DEF4A",
        "point_size": 3,
        "opacity": 0.5
    }
}
r = requests.post(url=url_prefix + "/pointmap", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# 保存为 PNG 图片
with open("/tmp/pointmap.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

print("绘制带权点图")
payload = {
    "scope": "nyc_taxi",
    "session": "spark",
    "sql": "SELECT ST_Point (pickup_longitude, pickup_latitude) AS point, total_amount AS color FROM nyc_taxi",
    "type": "weighted",
    "params": {
        "width": 512,
        "height": 448,
        "bounding_box": [
            -73.9616334766551,
            40.704739019597156,
            -73.94232850242967,
            40.728133570887906
        ],
        "opacity": 0.8,
        "coordinate_system": "EPSG:4326",
        "size_bound": [
            10
        ],
        "color_bound": [
            2.5,
            20
        ],
        "color_gradient": [
            "#115f9a",
            "#d0f400"
        ]
    }
}
r = requests.post(url=url_prefix + "/weighted_pointmap", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# 保存为 PNG 图片
with open("/tmp/weighted_pointmap.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

print("绘制热力图")
payload = {
    "scope": "nyc_taxi",
    "session": "spark",
    "sql": "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi GROUP BY point",
    "params": {
        "width": 512,
        "height": 448,
        "bounding_box": [
            -74.01556543545699,
            40.69354738164881,
            -73.9434424136598,
            40.780921656427836
        ],
        "coordinate_system": "EPSG:4326",
        "map_zoom_level": 10,
        "aggregation_type": "sum"
    }
}
r = requests.post(url=url_prefix + "/heatmap", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# 保存为 PNG 图片
with open("/tmp/heatmap.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

print("绘制轮廓图")
payload = {
    "scope": "nyc_taxi",
    "session": "spark",
    "sql": "SELECT ST_GeomFromText(buildingtext_dropoff) AS wkt, avg(tip_amount) AS w FROM nyc_taxi WHERE ((buildingtext_dropoff!='')) GROUP BY wkt",
    "params": {
        "width": 512,
        "height": 448,
        "bounding_box": [
            -74.00235068563725,
            40.735104211264684,
            -73.96739189659048,
            40.77744332808598
        ],
        "coordinate_system": "EPSG:4326",
        "color_gradient": [
            "#115f9a",
            "#d0f400"
        ],
        "color_bound": [
            0,
            5
        ],
        "opacity": 1,
        "aggregation_type": "mean"
    }
}
r = requests.post(url=url_prefix + "/choroplethmap", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# 保存为 PNG 图片
with open("/tmp/choroplethmap.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

print("绘制图标图")
# 下面 icon_path 的路径填写待显示图标所在的绝对路径，
# 本例中的图标文件可通过如下命令获取：
# wget https://github.com/zilliztech/arctern-docs/raw/branch-0.1.x/img/icon/icon-viz.png
icon_path = "/path/to/icon_example.png"
print("请输入图标文件所在的绝对路径：", end='')
icon_path = input()
payload = {
    "scope": "nyc_taxi",
    "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point from nyc_taxi where ST_Within(ST_Point(pickup_longitude, pickup_latitude), ST_GeomFromText('POLYGON ((-73.9616334766551 40.704739019597156, -73.94232850242967 40.704739019597156, -73.94232850242967 40.728133570887906 ,-73.9616334766551 40.728133570887906, -73.9616334766551 40.704739019597156))')) limit 25",
    "params": {
        "width": 512,
        "height": 448,
        "bounding_box": [
            -73.9616334766551,
            40.704739019597156,
            -73.94232850242967,
            40.728133570887906
        ],
        "coordinate_system": "EPSG:4326",
        "icon_path": icon_path,
        "icon_size": [17, 33]
    }
}
r = requests.post(url=url_prefix + "/icon_viz", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# 保存为 PNG 图片
with open("/tmp/icon_viz.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

print("绘制渔网图")
payload = {
    "scope": "nyc_taxi",
    "sql": "SELECT ST_Point (pickup_longitude, pickup_latitude) AS point, total_amount AS color FROM nyc_taxi where ST_Within(ST_Point(pickup_longitude, pickup_latitude), ST_GeomFromText('POLYGON ((-73.9616334766551 40.704739019597156, -73.94232850242967 40.704739019597156, -73.94232850242967 40.728133570887906 ,-73.9616334766551 40.728133570887906, -73.9616334766551 40.704739019597156))'))",
    "params": {
        "width": 512,
        "height": 448,
        "bounding_box": [
            -73.9616334766551,
            40.704739019597156,
            -73.94232850242967,
            40.728133570887906
        ],
        "opacity": 1,
        "coordinate_system": "EPSG:4326",
        "cell_size": 4,
        "cell_spacing": 1,
        "color_gradient": [
            "#115f9a",
            "#d0f400"
        ],
        "aggregation_type": "sum"
    }
}
r = requests.post(url=url_prefix + "/fishnetmap", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# 保存为 PNG 图片
with open("/tmp/fishnetmap.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

print("删除数据表 nyc_taxi\n")
sql = "drop table if exists nyc_taxi"
payload = {
    "scope": "nyc_taxi",
    "sql": sql,
    "collect_result": "0"
}
r = requests.post(url=url_prefix + "/query", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
# print(r.json())

print("删除作用域\n")
r = requests.delete(url=url_prefix + "/scope/nyc_taxi")
# print(r.json())

print("\033[1;32;40m点图：/tmp/pointmap.png\033[0m")
print("\033[1;32;40m带权点图：/tmp/weighted_pointmap.png\033[0m")
print("\033[1;32;40m热力图：/tmp/heatmap.png\033[0m")
print("\033[1;32;40m轮廓图：/tmp/choroplethmap.png\033[0m")
print("\033[1;32;40m图标图：/tmp/icon_viz.png\033[0m")
print("\033[1;32;40m渔网图：/tmp/fishnetmap.png\033[0m")

from pyspark.sql.types import *
from arctern_pyspark import register_funcs
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()

spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "5000")
register_funcs(spark)

nyc_schema = StructType([ \
        StructField("VendorID",StringType(),True), \
        StructField("tpep_pickup_datetime",StringType(),True), \
        StructField("tpep_dropoff_datetime",StringType(),True), \
        StructField("passenger_count",LongType(),True), \
        StructField("trip_distance",DoubleType(),True), \
        StructField("pickup_longitude",DoubleType(),True), \
        StructField("pickup_latitude",DoubleType(),True), \
        StructField("dropoff_longitude",DoubleType(),True), \
        StructField("dropoff_latitude",DoubleType(),True), \
        StructField("fare_amount",DoubleType(),True), \
        StructField("tip_amount",DoubleType(),True), \
        StructField("total_amount",DoubleType(),True), \
        StructField("buildingid_pickup",LongType(),True), \
        StructField("buildingid_dropoff",LongType(),True), \
        StructField("buildingtext_pickup",StringType(),True), \
        StructField("buildingtext_dropoff",StringType(),True) \
    ])

origin_df = spark.read.format("csv") \
                          .option("header",True) \
                          .option("delimiter",",") \
                          .schema(nyc_schema) \
                          .load("/path/to/0_2M_nyc_taxi_and_building.csv") \
                          .createOrReplaceTempView("origin_nyc_taxi")

spark.sql("select count(*) from origin_nyc_taxi").show()

nyc_sql = "select VendorID, " \
                      "to_timestamp(tpep_pickup_datetime,'yyyy-MM-dd HH:mm:ss XXXXX') as tpep_pickup_datetime, " \
                      "to_timestamp(tpep_dropoff_datetime,'yyyy-MM-dd HH:mm:ss XXXXX') as tpep_dropoff_datetime, " \
                      "passenger_count, " \
                      "trip_distance, " \
                      "pickup_longitude, " \
                      "pickup_latitude, " \
                      "dropoff_longitude, " \
                      "dropoff_latitude, " \
                      "fare_amount, " \
                      "tip_amount, " \
                      "total_amount, " \
                      "buildingid_pickup, " \
                      "buildingid_dropoff, " \
                      "buildingtext_pickup, " \
                      "buildingtext_dropoff " \
                "from origin_nyc_taxi where " \
                      "(pickup_longitude between -180 and 180) and (pickup_latitude between -90 and 90) and " \
                      "(dropoff_longitude between -180 and 180) and  (dropoff_latitude between -90 and 90)"
nyc_taxi_df = spark.sql(nyc_sql).cache()
nyc_taxi_df.createOrReplaceTempView("nyc_taxi")

spark.sql("select tpep_pickup_datetime,tpep_dropoff_datetime from nyc_taxi limit 10").show()

spark.sql("select st_astext(st_point(pickup_longitude, pickup_latitude)) from nyc_taxi limit 10").show(10,0)

spark.sql("select " \
                  "st_astext(" 
                      "st_point(pickup_longitude, pickup_latitude)) as epsg_4326," \
                  "st_astext(" \
                      "st_transform(" \
                          "st_point(pickup_longitude, pickup_latitude), 'epsg:4326', 'epsg:3857')) as epsg_3857 " \
              "from nyc_taxi " \
              "limit 10").show(10,0)

from arctern.util import save_png
from arctern.util.vega import vega_pointmap, vega_weighted_pointmap, vega_heatmap, vega_choroplethmap, vega_icon, vega_fishnetmap
from arctern_pyspark import pointmap
from arctern_pyspark import weighted_pointmap
from arctern_pyspark import heatmap
from arctern_pyspark import choroplethmap
from arctern_pyspark import icon_viz
from arctern_pyspark import fishnetmap
pos1=(-73.991504, 40.770759)
pos2=(-73.945155, 40.783434)
limit_num=200

# 绘制图层

pickup_sql = f"select st_point(pickup_longitude, pickup_latitude) as point from nyc_taxi where (pickup_longitude between {pos1[0]} and {pos2[0]}) and (pickup_latitude between {pos1[1]} and {pos2[1]}) limit {limit_num}"
pickup_df = spark.sql(pickup_sql)
# 根据查询结果绘制点图图层。点大小为 10，点颜色为 #2DEF4A，点不透明度为 1.0。
vega = vega_pointmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], point_size=10, point_color="#2DEF4A", opacity=1, coordinate_system="EPSG:4326")
res = pointmap(vega, pickup_df)
save_png(res, '/tmp/arctern_pointmap.png')


# 在指定地理区域（经度范围：-73.991504 至 -73.945155；纬度范围：40.770759 至 40.783434）中随机选取 200 个坐标点，并将 fare_amount 作为颜色权重、total_amount 作为大小权重。
pickup_sql = f"select st_point(pickup_longitude, pickup_latitude) as point, fare_amount as color_weight, total_amount as size_weight from nyc_taxi where (pickup_longitude between {pos1[0]} and {pos2[0]}) and (pickup_latitude between {pos1[1]} and {pos2[1]}) limit {limit_num}"
pickup_df = spark.sql(pickup_sql)
# 根据查询结果绘制带权点图图层。点的颜色根据 color_weight 在 "#115f9a" ~ "#d0f400" 之间变化，点的大小根据 size_weight 在 3 ~ 15 之间变化。
vega = vega_weighted_pointmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], color_gradient=["#115f9a", "#d0f400"], color_bound=[1, 50], size_bound=[3, 15], opacity=1.0, coordinate_system="EPSG:4326")
res = weighted_pointmap(vega, pickup_df)
save_png(res, "/tmp/arctern_weighted_pointmap.png")


# 在指定地理区域（经度范围：-73.991504 至 -73.945155；纬度范围：40.770759 至 40.783434）中随机选取 200 个坐标点，并将 fare_amount 作为热力值。
pickup_sql = f"select st_point(pickup_longitude, pickup_latitude) as point, fare_amount as weight from nyc_taxi where (pickup_longitude between {pos1[0]} and {pos2[0]}) and (pickup_latitude between {pos1[1]} and {pos2[1]}) limit {limit_num}"
pickup_df = spark.sql(pickup_sql)
# 根据查询结果绘制热力图图层。
vega = vega_heatmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], map_zoom_level=13.0, coordinate_system="EPSG:4326")
res = heatmap(vega, pickup_df)
save_png(res, "/tmp/arctern_heatmap.png")


# 在指定地理区域（经度范围：-73.991504 至 -73.945155；纬度范围：40.770759 至 40.783434）中随机选取 200 个坐标点，并将 fare_amount 作为颜色权重。
pickup_sql = f"select ST_GeomFromText(buildingtext_pickup) as buildings, fare_amount as color_weight from nyc_taxi where (pickup_longitude between {pos1[0]} and {pos2[0]}) and (pickup_latitude between {pos1[1]} and {pos2[1]}) and (buildingtext_pickup!='') limit {limit_num}"
pickup_df = spark.sql(pickup_sql)
# 根据查询结果绘制轮廓图图层。轮廓的填充颜色根据 color_weight 在 "#115f9a" ~ "#d0f400" 之间变化。
vega = vega_choroplethmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5, 5], opacity=1.0, coordinate_system="EPSG:4326")
res = choroplethmap(vega, pickup_df)
save_png(res, "/tmp/arctern_choroplethmap.png")


# 在指定地理区域（经度范围：-73.991504 至 -73.945155；纬度范围：40.770759 至 40.783434）中随机选取 25 个坐标点。
pickup_sql = f"select st_point(pickup_longitude, pickup_latitude) from nyc_taxi where (pickup_longitude between {pos1[0]} and {pos2[0]}) and (pickup_latitude between {pos1[1]} and {pos2[1]}) limit 25"
pickup_df = spark.sql(pickup_sql)
# 根据查询结果绘制图标图图层。
# 注意： 请将 /path/to/icon.png 改为 png 文件所在的绝对路径
vega = vega_icon(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], icon_path='/path/to/icon.png', icon_size=[25, 25], coordinate_system="EPSG:4326")
res = icon_viz(vega, pickup_df)
save_png(res, "/tmp/arctern_iconviz.png")


# 在指定地理区域（经度范围：-73.991504 至 -73.945155；纬度范围：40.770759 至 40.783434）中随机选取 200 个坐标点，并将 fare_amount 作为颜色权重。
pickup_sql = f"select st_point(pickup_longitude, pickup_latitude) as point, fare_amount as weight from nyc_taxi where (pickup_longitude between {pos1[0]} and {pos2[0]}) and (pickup_latitude between {pos1[1]} and {pos2[1]}) limit {limit_num}"
pickup_df = spark.sql(pickup_sql)
# 根据查询结果绘制渔网图图层。
vega = vega_fishnetmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], cell_size=8, cell_spacing=1, opacity=1.0, coordinate_system="EPSG:4326")
res = fishnetmap(vega, pickup_df)
save_png(res, "/tmp/arctern_fishnetmap.png")
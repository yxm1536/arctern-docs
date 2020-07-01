import pandas as pd

nyc_schema={
 "VendorID":"string",
 "tpep_pickup_datetime":"string",
 "tpep_dropoff_datetime":"string",
 "passenger_count":"int64",
 "trip_distance":"double",
 "pickup_longitude":"double",
 "pickup_latitude":"double",
 "dropoff_longitude":"double",
 "dropoff_latitude":"double",
 "fare_amount":"double",
 "tip_amount":"double",
 "total_amount":"double",
 "buildingid_pickup":"int64",
 "buildingid_dropoff":"int64",
 "buildingtext_pickup":"string",
 "buildingtext_dropoff":"string",
}


df=pd.read_csv("/path/to/0_2M_nyc_taxi_and_building.csv",
dtype=nyc_schema,
date_parser=pd.to_datetime,
parse_dates=["tpep_pickup_datetime","tpep_dropoff_datetime"])

pos1=(-73.991504, 40.770759)
pos2=(-73.945155, 40.783434)
limit_num=200
df=df.dropna()
pickup_df = df[(df.pickup_longitude>pos1[0]) & (df.pickup_longitude<pos2[0]) & (df.pickup_latitude>pos1[1]) & (df.pickup_latitude<pos2[1])]
pickup_df = pickup_df.head(limit_num)

from arctern import *

ST_AsText(ST_Point(pickup_df.pickup_longitude, pickup_df.pickup_latitude)).head()

ST_AsText(ST_Transform(ST_Point(pickup_df.pickup_longitude, pickup_df.pickup_latitude),'epsg:4326', 'epsg:3857')).head()

from arctern.util import save_png
from arctern.util.vega import vega_pointmap, vega_weighted_pointmap, vega_heatmap, vega_choroplethmap, vega_icon, vega_fishnetmap

vega = vega_pointmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], point_size=10, point_color="#2DEF4A", opacity=1, coordinate_system="EPSG:4326")
png = point_map_layer(vega, ST_Point(pickup_df.pickup_longitude, pickup_df.pickup_latitude))
save_png(png, '/tmp/arctern_pointmap_pandas.png')

vega = vega_weighted_pointmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], color_gradient=["#115f9a", "#d0f400"], color_bound=[1, 50], size_bound=[3, 15], opacity=1.0, coordinate_system="EPSG:4326")
png = weighted_point_map_layer(vega, ST_Point(pickup_df.pickup_longitude, pickup_df.pickup_latitude), color_weights=df.head(limit_num).fare_amount, size_weights=df.head(limit_num).total_amount)
save_png(png, "/tmp/arctern_weighted_pointmap_pandas.png")

vega = vega_heatmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], map_zoom_level=13.0, coordinate_system="EPSG:4326")
png = heat_map_layer(vega, ST_Point(pickup_df.pickup_longitude, pickup_df.pickup_latitude), df.head(limit_num).fare_amount)
save_png(png, "/tmp/arctern_heatmap_pandas.png")

vega = vega_choroplethmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5, 5], opacity=1.0, coordinate_system="EPSG:4326")
png = choropleth_map_layer(vega, ST_GeomFromText(pickup_df.buildingtext_pickup), df.head(limit_num).fare_amount)
save_png(png, "/tmp/arctern_choroplethmap_pandas.png")

vega = vega_icon(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], icon_path='/path/to/arctern-color.png', icon_size=[17, 33], coordinate_system="EPSG:4326")
png = icon_viz_layer(vega, ST_Point(pickup_df.head(25).pickup_longitude, pickup_df.head(25).pickup_latitude))
save_png(png, "/tmp/arctern_iconviz_pandas.png")

vega = vega_fishnetmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], cell_size=8, cell_spacing=1, opacity=1.0, coordinate_system="EPSG:4326")
png = fishnet_map_layer(vega, ST_Point(pickup_df.pickup_longitude, pickup_df.pickup_latitude), df.head(limit_num).fare_amount)
save_png(png, "/tmp/arctern_fishnetmap_pandas.png")

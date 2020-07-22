# Heat map

根据相关画图参数绘制热力图，将绘图结果以 Base64 编码方式返回。

## Request description

- Method: `POST`
- URL: `/heatmap`
- Headers:
    - `Content-Type: application/json`
- Body: See [Body example](#Body-example)。

## Body example

Parameter description:

- `input_data`: 输入数据描述，需为已定义的变量名称或可执行的 Python 语句。
    - `points`: 点的位置，格式为 WKB 的 pandas.Series。
    - `weights`: 热力值，为 float64 或 int64 类型的 pandas.Series。
- `params`: 绘图参数。
    - `width`: 图片宽度。
    - `height`: 图片高度。
    - `bounding_box`: 渲染图片所表示的地理范围 [x_min, y_min, x_max, y_max]。
    - `coordinate_system`: 输入数据的坐标系统，详见 [World Geodetic System](https://en.wikipedia.org/wiki/World_Geodetic_System)。
    - `map_zoom_level`: 地图放大比例，取值范围 [1, 15]。
    - `aggregation_type`: 聚合类型。

### Python backend

The example for Python backend is as follows:

```json
{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "weights": "raw_data.fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "map_zoom_level": 10,
        "aggragation_type": "sum"
    }
}
```

### PySpark backend

If you use the PySpark backend, you only need to change the `input_data` in the example of Python backend to the following SQL query:

```
"sql": "select ST_Point(pickup_longitude, pickup_latitude) as point, fare_amount as weights from raw_data"
```

## Request example

### Python

The example uses Python's `requests` library to call `Arctern RESTful API`. Run the following command to install `requests`:

```bash
pip install requests
```

Here is an example of calling the `heatmap` API:

```python
import requests
import json

url = "http://localhost:8080/heatmap"

payload = {
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "weights": "raw_data.fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "map_zoom_level": 10,
        "aggregation_type": "sum"
    }
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request POST 'http://localhost:8080/heatmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "weights": "raw_data.fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "map_zoom_level": 10,
        "aggregation_type": "sum"
    }
}'
```

## Response example

```json
{
    "status": "success",
    "code": "200",
    "result": "使用 Base64 编码后的热力图数据"
}
```

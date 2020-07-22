# Choropleth map

Draws the choropleth map according to the relevant parameters and returns a Base64 image.

## Request description

- Method: `POST`
- URL: `/choroplethmap`
- Headers:
    - `Content-Type: application/json`
- Body: See [Body example](#Body-example).

## Body example

Parameter description:

- `input_data`: 输入数据描述，需为已定义的变量名称或可执行的 Python 语句。
    - `region_boundaries`: 轮廓的位置，格式为 WKB 的 pandas.Series。
    - `weights`: 轮廓权重，为 float64 或 int64 类型的 pandas.Series。
- `params`: 绘图参数。
    - `width`: 图片宽度。
    - `height`: 图片高度。
    - `bounding_box`: 渲染图片所表示的地理范围 [x_min, y_min, x_max, y_max]。
    - `coordinate_system`: 输入数据的坐标系统，详见 [World Geodetic System](https://en.wikipedia.org/wiki/World_Geodetic_System)。
    - `color_gradient`: 轮廓的颜色渐变范围，即轮廓的颜色从左边渐变到右边。
    - `color_bound`: 轮廓颜色的取值范围，与 `color_gradient` 配合使用。
    - `opacity`: 轮廓的不透明度。
    - `aggregation_type`: 聚合类型。

### Python backend

The example for Python backend is as follows:

```json
{
    "input_data": {
        "region_boundaries": "ST_GeomFromText(raw_data.dropna().buildingtext_pickup)",
        "weights": "raw_data.dropna().fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "color_gradient": ["#0000FF", "#FF0000"],
        "color_bound": [2.5, 5],
        "opacity": 1,
        "aggregation_type": "sum"
    }
}
```

### PySpark backend

If you use the PySpark backend, you only need to change the `input_data` in the example of Python backend to the following SQL query:

```
"sql": "select ST_GeomFromText(buildingtext_pickup) as polygon, fare_amount as count from raw_data where buildingtext_pickup!=''"
```

## Request example

### Python

The example uses Python's `requests` library to call `Arctern RESTful API`. Run the following command to install `requests`:

```bash
pip install requests
```

Here is an example of calling the `choroplethmap` API:

```python
import requests
import json

url = "http://localhost:8080/choroplethmap"

payload  = {
    "input_data": {
        "region_boundaries": "ST_GeomFromText(raw_data.dropna().buildingtext_pickup)",
        "weights": "raw_data.dropna().fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "color_gradient": ["#0000FF", "#FF0000"],
        "color_bound": [2.5, 5],
        "opacity": 1,
        "aggregation_type": "mean"
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
curl --location --request POST 'http://localhost:8080/choroplethmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "region_boundaries": "ST_GeomFromText(raw_data.dropna().buildingtext_pickup)",
        "weights": "raw_data.dropna().fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "color_gradient": ["#0000FF", "#FF0000"],
        "color_bound": [2.5, 5],
        "opacity": 1,
        "aggregation_type": "mean"
    }
}'
```

## Response example

```json
{
    "status": "success",
    "code": "200",
    "result": "使用 Base64 编码后的轮廓图数据"
}
```
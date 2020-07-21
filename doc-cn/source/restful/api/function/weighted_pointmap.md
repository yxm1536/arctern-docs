# 带权点图

根据相关画图参数绘制权重图，将绘图结果以 Base64 编码方式返回。

## 请求说明

- Method: `POST`
- URL: `/weighted_pointmap`
- Headers:
    - `Content-Type: application/json`
- Body: 见 [Body 示例](#Body-示例)。

## Body 示例

参数说明：

- `input_data`: 输入数据描述，需为已定义的变量名称或可执行的 Python 语句。
    - `points`: 点的位置，格式为 WKB 的 pandas.Series。
    - color_weights: 点的颜色权重，为 float64 或 int64 类型的 pandas.Series。
    - size_weights: 点的大小权重，为 float64 或 int64 类型的 pandas.Series。
- `params`: 绘图参数。
    - `width`: 图片宽度。
    - `height`: 图片高度。
    - `bounding_box`: 渲染图片所表示的地理范围 [x_min, y_min, x_max, y_max]。
    - `coordinate_system`: 输入数据的坐标系统，详见 [World Geodetic System](https://en.wikipedia.org/wiki/World_Geodetic_System)。
    - `color_gradient`: 点的颜色渐变范围，即点的颜色从左边渐变到右边。
    - `color_bound`: 点颜色的取值范围，与 `color_gradient` 配合使用。
    - `opacity`: 点的不透明度。
    - `size_bound`: 点大小的取值范围。

### Python 后台

如果数据处理后台为 Python，则示例 JSON 如下：

```json
{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "color_weights": "raw_data.fare_amount",
        "size_weights": "raw_data.total_amount"
    },
    "params": {
            "width": 1024,
            "height": 896,
            "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
            "color_gradient": ["#0000FF", "#FF0000"],
            "color_bound": [0, 2],
            "size_bound": [0, 10],
            "opacity": 1.0,
            "coordinate_system": "EPSG:4326"
    }
}
```

### PySpark 后台

如果数据处理后台为 PySpark，你只需将上面 Python 后台的示例代码中的 `input_data` 改为相应的 SQL 查询语句，示例如下：

```
"sql": "select ST_Point(pickup_longitude, pickup_latitude) as point, fare_amount as count1, total_amount as count2 from raw_data"
```

## 请求示例

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern RESTful API`，执行以下命令安装 `requests`：

```bash
pip install requests
```

调用示例：

```python
import requests
import json

url = "http://localhost:8080/weighted_pointmap"

payload = {
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "color_weights": "raw_data.fare_amount",
        "size_weights": "raw_data.total_amount"
    },
    "params": {
            "width": 1024,
            "height": 896,
            "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
            "color_gradient": ["#0000FF", "#FF0000"],
            "color_bound": [0, 2],
            "size_bound": [0, 10],
            "opacity": 1.0,
            "coordinate_system": "EPSG:4326"
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
curl --location --request POST 'http://localhost:8080/weighted_pointmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "color_weights": "raw_data.fare_amount",
        "size_weights": "raw_data.total_amount"
    },
    "params": {
            "width": 1024,
            "height": 896,
            "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
            "color_gradient": ["#0000FF", "#FF0000"],
            "color_bound": [0, 2],
            "size_bound": [0, 10],
            "opacity": 1.0,
            "coordinate_system": "EPSG:4326"
    }
}'
```

## 响应示例

```json
{
    "status": "success",
    "code": "200",
    "result": "使用 Base64 编码后的权重图数据"
}
```

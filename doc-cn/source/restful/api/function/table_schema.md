# 获取表的列信息

获取数据表各列的名称与数据类型信息。

## 请求说明

- HTTP方法: **GET**
- 请求URL: /table/schema?table=table_name

- table：表名。

## 请求样例

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern RESTful API`，执行以下命令安装 `requests`：

```bash
pip install requests
```

调用示例

```python
import requests

url = "http://localhost:8080/table/schema?table=table_name"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request GET 'http://localhost:8080/table/schema?table=table_name'
```

## 响应样例

```json
{
    "table": "table_name",
    "schema": [
        {"column0": "string"},
        {"column1": "double"},
        {"column2": "int"}
    ],
    "num_rows": 500
}
```

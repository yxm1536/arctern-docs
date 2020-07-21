# Table schema

获取数据表各列的名称与数据类型信息。

## Request description

- Method: `GET`
- URL: `/table/schema?table=table_name`
- table: 表名。

## Request example

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern RESTful API`，执行以下命令安装 `requests`：

```bash
pip install requests
```

Here is an example of calling the `table/schema` API:

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

## Response example

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

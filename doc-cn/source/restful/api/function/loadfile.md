# 加载文件

加载数据文件。当前支持的文件格式详见 [RESTful 文件的导入导出](../../file_data.md)。

## 请求说明

- HTTP方法: **POST**
- 请求URL: `/loadfile`
- Headers:
    - `Content-Type: application/json`
- Body:
```json
{
    "tables": [
        {
            "name": "table_name",
            "format": "csv",
            "path": "/path/to/data.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [
                {"column0": "string"},
                {"column1": "double"},
                {"column2": "int"}
            ]
        }
    ]
}
```

参数说明：

- tables：创建数据表的描述信息。该字段为一个列表，系统将会按照列表中的顺序依次进行建表操作。
    - name：数据表名称。
    - format：待加载文件的文件格式。
    - path：文件路径。
    - options：加载文件时的指定选项，使用 `key-value` 形式提供。
    - schema：各列数据的名称和类型描述。schema 字段是一个列表，顺序需要和文件中各列的实际存储顺序保持一致。

## 请求样例

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern RESTful API`，执行以下命令安装 `requests`：

```bash
pip install requests
```

调用示例：

```python
import requests
import json

url = "http://localhost:8080/loadfile"

# /path/to/data.csv文件内容样例如下：
"""
column0, column1, column2
str1, 0.1, 1
str2, 0.2, 2
str3, 0.3, 3
"""
payload = {
    "tables": [
        {
            "name": "table_name",
            "format": "csv",
            "path": "/path/to/data.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [
                {
                    "column0": "string"
                },
                {
                    "column1": "double"
                },
                {
                    "column2": "int"
                }
            ]
        }
    ]
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request POST 'http://localhost:8080/loadfile' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tables": [
        {
            "name": "table_name",
            "format": "csv",
            "path": "/path/to/data.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [
                {
                    "column0": "string"
                },
                {
                    "column1": "double"
                },
                {
                    "column2": "int"
                }
            ]
        }
    ]
}'
```

## 响应样例

```json
{
    "status": "success",
    "code": "200",
    "message": "create table successfully!"
}
```

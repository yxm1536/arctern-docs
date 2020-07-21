# 保存文件

执行数据查询操作并将结果存入指定文件。仅当数据处理后台为 PySpark 时可用。当数据处理后台为 Python 时请使用 `command` 接口保存文件。参见 [代码执行接口说明](command.md)。

## 请求说明

- Method: `POST`
- URL: `/savefile`
- Headers:
    - `Content-Type: application/json`
- Body:

    ```json
    {
        "tables": [
            {
                "sql": "select * from table_name",
                "format": "csv",
                "path": "/path/to/data.csv",
                "options": {
                    "header": "True",
                    "delimiter": ","
                }
            }
        ]
    }
    ```

    参数说明：

    - `tables`: 将数据保存为文件时的描述信息。该字段为一个列表，系统将会按照列表中的顺序依次进行文件保存操作。
        - `sql`: 待执行的 SQL 查询语句，该语句的结果将作为要保存的表。
        - `format`: 待保存的文件格式。
        - `path`: 文件路径。
        - `options`: 保存文件时的指定选项，使用 `key-value` 形式提供。

## 请求示例

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern RESTful API`，执行以下命令安装 `requests`：

```bash
pip install requests
```

调用示例

```python
import requests
import json

url = "http://localhost:8080/savefile"

payload = {
    "tables": [
        {
            "sql": "select * from table_name",
            "format": "csv",
            "path": "/path/to/data.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            }
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
curl --location --request POST 'http://localhost:8080/savefile' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tables": [
        {
            "sql": "select * from table_name",
            "format": "csv",
            "path": "/path/to/data.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            }
        }
    ]
}'
```

## 响应示例

```json
{
    "status": "success",
    "code": "200",
    "message": "save table successfully!"
}
```

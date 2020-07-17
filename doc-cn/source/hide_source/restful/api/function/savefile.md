# 保存文件

执行数据查询操作并将结果存入指定文件。

## 请求说明

- Method: `POST`
- URL: `/savefile`
- Headers:
    - `Content-Type: application/json`
- Body:
```json
{
    "scope": "scope_name",
    "session": "session_name", 
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

- scope：执行保存文件操作的作用域名称；
- session：可选参数，执行保存文件操作的 `SparkSession` 名称；
- tables：将数据保存为文件时的描述信息，该字段为一个列表( `list` )，系统将会按照列表中的顺序依次进行文件保存操作，以下为列表中每个元素的具体参数说明：
    - sql：待执行的 SQL 查询语句，该语句的结果将作为要保存的表；
    - format：待保存的文件格式；
    - path：文件路径；
    - options：保存文件时的指定选项，使用 `key-value` 形式提供。具体的选项内容参见 [Arctern-Spark 文件的导入导出](../../../spark/data_source/file_data.md)；

## 示例

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern Restful API`，使用下面的命令安装 `requests`：

```bash
pip install requests
```

调用示例

```python
import requests
import json

url = "http://localhost:8080/savefile"

payload = {
    "scope": "scope_name",
    "session": "session_name", 
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
    "scope": "scope_name",
    "session": "session_name", 
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

## 返回说明

成功示例：

```json
{
    "status": "success",
    "code": "200",
    "message": "save table successfully!"
}
```

失败示例：

```json
{
    "status": "error",
    "code": "-1",
    "message": "scope not found!"
}
```


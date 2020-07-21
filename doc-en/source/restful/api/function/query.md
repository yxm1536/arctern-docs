# Query

执行给定的 SQL 查询语句。仅当数据处理后台为 PySpark 时可用。

## Request description

- Method: `POST`
- URL: `/query`
- Headers:
    - `Content-Type: application/json`
- Body:

    - 数据查询：

    ```json
    {
        "sql": "select * from table_name limit 1",
        "collect_result": "1"
    }
    ```

    - 创建数据表：

    ```json
    {
        "sql": "create table new_table as (select * from table_name)",
        "collect_result": "0"
    }
    ```

    参数说明：

    - `sql`: 待执行的 SQL 查询语句。
    - `collect_result`: 可选参数，默认值为 1。
        - 1: 将 SQL 语句的查询结果用 JSON 格式返回。
        - 0: 仅在后台执行查询语句不返回执行结果。

## Request example

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern RESTful API`，执行以下命令安装 `requests`：

```bash
pip install requests
```

Here is an example of calling the `query` API:

```python
import requests
import json

url = "http://localhost:8080/query"

payload = {
    "sql": "select * from table_name limit 1",
    "collect_result": "1"
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

```python
import requests
import json

url = "http://localhost:8080/query"

payload = {
    "sql": "create table new_table as (select * from table_name)",
    "collect_result": "0"
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request POST 'http://localhost:8080/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sql": "select * from table_name limit 1",
    "collect_result": "1"
}'
```

```bash
curl --location --request POST 'http://localhost:8080/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sql": "create table new_table as (select * from table_name)",
    "collect_result": "0"
}'
```

## Response example

```json
{
    "status": "succuss",
    "code": "200",
    "result": [
        ["col1", 0.5, 2]
    ],
    "message": "execute sql successfully!"
}
```

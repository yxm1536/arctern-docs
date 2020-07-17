# 查询

执行给定的 SQL 查询语句。

## 请求说明

- Method: `POST`
- URL: `/query`
- Headers:
    - `Content-Type: application/json`
- Body:

数据查询：

```json
{
    "scope": "scope_name",
    "session": "session_name",
    "sql": "select * from table_name limit 1",
    "collect_result": "1"
}
```

创建数据表：

```json
{
    "scope": "scope_name",
    "session": "session_name",
    "sql": "create table new_table as (select * from table_name)",
    "collect_result": "0"
}
```

参数说明：

- scope：执行查询操作的作用域名称；
- session：可选参数，执行 SQL 的 `SparkSession` 名称；
- sql：待执行的 SQL 查询语句；
- collect_result：可选参数，默认值为 `1`。`1` 表示将 SQL 语句的查询结果用 `json` 格式返回，`0` 表示仅在后台执行查询语句不返回执行结果。

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

url = "http://localhost:8080/query"

payload = {
    "scope": "scope_name",
    "session": "session_name",
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
    "scope": "scope_name",
    "session": "session_name",
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
    "scope": "scope_name",
    "session": "session_name",
    "sql": "select * from table_name limit 1",
    "collect_result": "1"
}'
```

```bash
curl --location --request POST 'http://localhost:8080/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "scope": "scope_name",
    "session": "session_name",
    "sql": "create table new_table as (select * from table_name)",
    "collect_result": "0"
}'
```

## 返回说明

示例：

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

失败示例：

```json
{
    "code": -1,
    "message": "Table or view not found: error_table; line 1 pos 14;\n'Project [*]\n+- 'UnresolvedRelation [error_table]\n",
    "status": "error"
}
```


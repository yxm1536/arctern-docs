# 创建scope

Arctern Restful Server 使用作用域（`scope`）为你分配服务器资源。每个作用域拥有独享的上下文信息，如载入的文件数据和创建的数据表。

在创建 `scope` 的同时，Arctern  Restful Server 会为 `scope` 创建一个名为 `spark` 的 SparkSession。在调用 `/loadfile`、`/query`、`/pointmap` 等 API 时如未传入 `session` 字段，则会默认使用该 SparkSession 进行操作。如需创建自定义的 SparkSession，请使用 [`/command` 接口](./command.md)。

## 请求说明

- Method: `POST`
- URL: `/scope`
- Headers:
    - `Content-Type: application/json`
- Body:
```json
{
    "scope": "scope_name"
}
```

参数说明：

- scope：可选参数，若不指定 `scope`，则请求的 `headers` 字段可以省略，服务器将产生一个随机字符串作为新建 `scope` 的名称，并将其返回。

## 示例

### Python

本文示例代码使用 Python 的 `requests` 库调用 `Arctern Restful API`，使用下面的命令安装 `requests`：

```bash
pip install requests
```

调用示例：

```python
import requests
import json

url = "http://localhost:8080/scope"

payload = {
    'scope': 'scope_name'
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request POST 'http://localhost:8080/scope' \
--header 'Content-Type: application/json' \
--data-raw '{
	"scope":"scope_name"
}'
```

## 返回说明

成功示例：

```json
{
    "status": "success",
    "code": "200",
    "message": "create scope successfully!",
    "scope": "scope_name"
}
```

失败示例：

```json
{
    "status": "error",
    "code": "-1",
    "message": "scope already exist!"
}
```


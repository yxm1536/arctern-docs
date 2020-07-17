# 代码执行

在指定作用域( `scope` )内执行给定的 python 代码。`scope`  用于隔离Python代码执行的上下文，使用不同 `scope` 执行代码，则代码中的变量相互不影响。如需在先后执行的代码中保持相同的上下文，则需使用相同的`scope`。

## 请求说明

- Method: `POST`
- URL: `/command`
- Headers:
    - `Content-Type: application/json`
- Body:
```json
{
    "scope": "scope_name",
    "command": "import sys\nprint(len(sys.argv))"
}
```

参数说明：

- scope：该字段指明在哪一个作用域内执行 command；
- command：待执行的 `python` 代码。

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

url = "http://localhost:8080/command"

payload = {
    "scope": "scope_name",
    "command": "import sys\nprint(len(sys.argv))"
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request POST 'http://localhost:8080/command' \
--header 'Content-Type: application/json' \
--data-raw '{
	"scope":"scope_name",
	"comamnd":"import sys\nprint(len(sys.argv))"
}'
```

## 返回说明

正常执行：

```json
{
    "status": "success",
    "code": "200",
    "message": "execute command successfully!"
}
```

执行对应代码出现异常：

```json
{
    "status": "error",
    "code": "400",
    "message": "cannot import package1"
}
```


# 代码执行

执行给定的 Python 代码。

## 请求说明

- Method: **POST**
- URL: `/command`
- Headers:
    - `Content-Type: application/json`
- Body:
```json
{
    "command": "import sys\nprint(len(sys.argv))"
}
```

参数说明：

- command：待执行的 Python 代码。

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

url = "http://localhost:8080/command"

payload = {
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
	"command":"import sys\nprint(len(sys.argv))"
}'
```

## 响应样例

```json
{
    "status": "success",
    "code": "200",
    "message": "execute command successfully!"
}
```

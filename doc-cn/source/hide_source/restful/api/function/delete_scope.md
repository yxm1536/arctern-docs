# 删除scope

删除指定的 `scope`，你完成操作后需要使用该接口显式释放所占用的服务器资源。 

> <font color="#dd0000">注意：</font>`Arctern Restful` 服务不会主动释放你申请的作用域，完成操作后请务必删除申请的所有作用域。

## 请求说明

- Method: **DELETE**
- URL: `/scope/<scope>`

参数说明：

- scope：作用域名称。

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

url = "http://localhost:8080/scope/scope_name"

payload = {}
headers= {}

response = requests.request("DELETE", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
```

### curl

```bash
curl --location --request DELETE 'http://localhost:8080/scope/scope_name'
```

## 返回说明

成功示例：

```json
{
    "status": "success",
    "code": "200",
    "message": "delete scope successfully!",
    "scope": "scope_name"
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


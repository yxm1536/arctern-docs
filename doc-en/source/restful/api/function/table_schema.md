# Table schema

获取数据表各列的名称与数据类型信息。

## Request description

- Method: `GET`
- URL: `/table/schema?table=table_name`
- table: 表名。

## Request example

### Python

The example uses Python's `requests` library to call `Arctern RESTful API`. Run the following command to install `requests`:

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

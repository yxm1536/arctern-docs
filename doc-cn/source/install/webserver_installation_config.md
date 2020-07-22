# Arctern RESTful Server 安装与配置

## 安装 Arctern 后台

Arctern RESTful Server 仅负责接收和解析 RESTful 请求，实际操作由 Arctern 后台执行。在安装 Arctern RESTful Server 前，你需要事先安装 Arctern 后台系统。目前，Arctern RESTful Server 支持基于 Python 和基于 Spark 的两种 Arctern 后台。你可以任选一种安装使用。

### 安装基于 Python 的 Arctern 后台

请参考如下链接：

* [安装 Arctern](./standalone_installation.md)

### 安装基于 Spark 的 Arctern 后台

请参考如下链接：

* [在 Spark 上安装 Arctern](./install_arctern_on_spark_cn.md)

## 安装 Arctern RESTful Server

为 Arctern RESTful Server 构建 Conda 环境：

> **注意：** 此处使用的环境名为 `arctern_server_env`，你可根据需求自行选择合适的名称。

```bash
$ conda create -n arctern_server_env -c conda-forge -c arctern arctern-webserver
```

> **注意：** 如果你在同一台计算机上安装 Arctern 后台系统和 Arctern RESTful Server，建议二者使用不同的 Conda 环境。例如，为 Arctern 后台创建名为 `arctern_env` 的环境，为 Arctern RESTful Server 的创建名为 `arctern_server_env` 的环境。

## 设置 Workspace

进入 `arctern_server_env` 虚拟环境：

```bash
$ conda activate arctern_server_env
```

Workspace 文件夹用于存放 Arctern RESTful Server 所依赖的第三方工具、插件、系统配置文件等信息。在初次启动 RESTful Server 前，你需要通过 `bootstrap` 命令设置 workspace。

> **注意：** 此处 `workspace` 指定为 `/home/usr/arctern_server/`，你可根据需求自行选择合适的路径。

```bash
arctern-server bootstrap --workspace=/home/usr/arctern_server/
```

## 配置 Arctern RESTful Server

Arctern RESTful Server 为用户开放了一组系统配置项，包括服务端口、IP 地址、数据处理后台等。其中，Python 或 PySpark 等不同的数据处理后台的选择由 `interpreter_type` 选项控制。

如果选用 Python 作为后台，请依照以下命令示例进行配置，配置项解释详见 [Arctern RESTful Server 配置选项](../restful/restful_config.md)：

```bash
arctern-server config --arctern_server_host=127.0.0.1 --arctern_server_port=8080 --interpreter_type=python --interpreter_name=arcternpython --interpreter_python_path="</path/to/python>"
```

如果选用 Spark 作为后台，请依照以下命令示例进行配置，配置项解释详见 [Arctern RESTful Server 配置选项](../restful/restful_config.md)：

```bash
arctern-server config --arctern_server_host=127.0.0.1 --arctern_server_port=8080 --interpreter_type=pyspark --interpreter_name=arcternpyspark --interpreter_pyspark_python="</path/to/python>" --interpreter_pyspark_driver_python=</path/to/python> --interpreter_spark_home="</path/to/spark>" --interpreter_master=local
```

> **注意：**
> * 你需要将 `</path/to/python>` 替换为 Arctern 所在 Conda 环境的 Python 绝对路径，如何获取该路径请参考 [FAQ](#faq)。
> * 你还需要将 `</path/to/spark>` 替换为 Spark 的 HOME 路径。

## 启动

```bash
arctern-server start --mode=release
```

`mode` 可选 `release` 或 `debug`。`debug` 模式会提供更准确的提示信息，但比 `release` 模式的执行效率低。

## FAQ

### 如何获取 Arctern Conda 环境的 Python 路径

进入 Arctern 所在的 Conda 环境：

```bash
$ conda activate arctern_env
```

获取 python 的路径：

```bash
$ which python
```

### 使用 HTTP 代理对 Arctern RESTful Server 的影响

使用 HTTP 代理可能会导致 RESTful API 无法被正常调用，请关闭 HTTP 代理然后重启 Arctern RESTful Server。
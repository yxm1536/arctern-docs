# 安装

本文档介绍 Spark3.0 和 Arctern 的安装步骤，以及如何配置 Arctern 运行在 Spark 上。

## 安装 Arctern

请参考如下链接：

* [在线安装 Arctern Python 后台](../python/installation_and_deployment/install_arctern_on_python.md)

## Spark 安装要求

|  名称    |   版本     |
| :---------- | :------------ |
| 操作系统 |Ubuntu LTS 18.04, Centos 7|
| JDK    | JDK 8 |


## 安装并配置 Spark

以下对 local 模式的 Spark 安装和配置流程进行介绍。
> **注意：** 若需要以集群模式安装 Spark,请参考 [Spark 官方文档](https://spark.apache.org/docs/latest/) 。

下载 [spark-3.0.0编译包](https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz) 并解压 Spark 压缩包：

```bash
$ wget https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz
$ tar -xvzf spark-3.0.0-bin-hadoop2.7.tgz
```

配置 SPARK_HOME变量:

执行 `vim ~/.bashrc` 以编辑 **bashrc** 文件。 在该文件中添加以下内容:

```bash
export SPARK_HOME=<path/to/spark-3.0.0-bin-hadoop2.7>
export PATH=$SPARK_HOME/bin:$PATH
```
> **注意：** 你需要将 `<path/to/spark-3.0.0-bin-hadoop2.7>` 替换为本地文件夹 spark-3.0.0-bin-hadoop2.7 的路径。

创建 spark-defaults.conf 以及 spark-env.sh 文件：

```bash
$ cd spark-3.0.0-bin-hadoop2.7/conf
$ cp spark-defaults.conf.template spark-defaults.conf
$ cp spark-env.sh.template spark-env.sh
```

在文件 spark-defaults.conf 的最后添加以下内容：

> **注意：** 你需要将 `<conda_prefix>` 替换为本地 Conda 环境的安装路径。如何获取 conda 环境的安装路径请参考FAQ

```bash
spark.driver.extraClassPath <conda_prefix>/jars/arctern_assembly-0.3.0.jar
spark.executorEnv.PROJ_LIB <conda_prefix>/share/proj
spark.executorEnv.GDAL_DATA <conda_prefix>/share/gdal
spark.executor.extraClassPath <conda_prefix>/jars/arctern_assembly-0.3.0.jar
```

在文件 spark-env.sh 的最后添加以下内容：

```bash
$ export PYSPARK_PYTHON=<conda_prefix>/bin/python
```

### 确认路径配置是否成功

执行以下命令进入 PySpark 交互界面。

```bash
$ pyspark
```

在交互界面中输入以下内容打印 PySpark 的 Python 路径。

```python
>>> import sys
>>> print(sys.prefix)
```

如果终端打印的内容是 Conda 环境的本地安装路径，说明 PySpark 的 Python 路径配置成功。

## 测试样例

执行以下命令下载测试文件：

```bash
$ wget https://raw.githubusercontent.com/arctern-io/arctern/branch-0.3.x/spark/pyspark/examples/gis/spark_udf_ex.py
```

执行以下命令提交 Spark 任务：

> **注意：** 你需要将 `<path/to/your/spark>` 替换为 Spark 的本地安装路径，将 `<path/to/spark_udf_ex.py>` 替换为本地测试文件的路径。

local 模式：

```bash
$ spark-submit <path/to/spark_udf_ex.py>
```

若最后打印结果包含以下内容，则表示通过测试样例。
```bash
All tests of arctern have passed!
```

## FAQ

### 如何获取 Conda 环境的安装路径

进入 Conda 环境：

```bash
$ conda activate arctern_env
```
运行以下命令获取当前 conda 环境的安装路径：

```bash
 $ echo $CONDA_PREFIX
```
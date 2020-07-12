# 安装

本文档介绍 Spark 3.0 和 Arctern 的安装步骤，以及如何配置 Arctern 并在 Spark 上运行 Arctern。

## 安装 Arctern

请参考如下链接：

* [安装 Arctern](./standalone_installation.md)

## 安装并配置 Spark

### Spark 安装要求

|  名称    |   版本     |
| :---------- | :------------ |
| 操作系统 |Ubuntu LTS 18.04, Centos 7|
| JDK    | JDK 8 |

## 安装并配置 Spark

以下对 local 模式的 Spark 安装和配置流程进行介绍。
> **注意：** 若需要以集群模式安装 Spark ，请参考 [Spark 官方文档](https://spark.apache.org/docs/latest/) 。
同时也可以参考 [在 Spark 集群上安装部署 Arctern](./cluster_installation.md) 。

### 下载 spark 预编译包

下载 [spark-3.0.0编译包](https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz) 并解压：

```bash
$ wget https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz
$ tar -xvzf spark-3.0.0-bin-hadoop2.7.tgz
```

### 配置 Spark

执行 `vim ~/.bashrc` 以编辑 **bashrc** 文件，配置 `SPARK_HOME` 变量。在该文件中添加以下内容:
> **注意：** 你需要将 `<path/to/spark-3.0.0-bin-hadoop2.7>` 替换为本地文件夹 spark-3.0.0-bin-hadoop2.7 的路径。

```bash
export SPARK_HOME=<path/to/spark-3.0.0-bin-hadoop2.7>
export PATH=$SPARK_HOME/bin:$PATH
```

> **注意：** 你需要将 `<path/to/spark-3.0.0-bin-hadoop2.7>` 替换为本地文件夹 **spark-3.0.0-bin-hadoop2.7** 的路径。

创建 **spark-defaults.conf** 以及 **spark-env.sh** 文件：

```bash
$ cd spark-3.0.0-bin-hadoop2.7/conf
$ cp spark-defaults.conf.template spark-defaults.conf
$ cp spark-env.sh.template spark-env.sh
```

在文件 spark-defaults.conf 的最后添加以下内容：

> **注意：** 你需要将 `<conda_prefix>` 替换为本地 Conda 环境的安装路径。如何获取 conda 环境的安装路径请参考本文档末尾的 [FAQ](#FAQ)部分。

```bash
spark.driver.extraClassPath <conda_prefix>/jars/arctern_assembly-0.3.0.jar
spark.executorEnv.PROJ_LIB <conda_prefix>/share/proj
spark.executorEnv.GDAL_DATA <conda_prefix>/share/gdal
spark.executor.extraClassPath <conda_prefix>/jars/arctern_assembly-0.3.0.jar
```

在文件 spark-env.sh 的最后添加以下内容：
> **注意：** 你需要将 `<conda_prefix>` 替换为本地 Conda 环境的安装路径。如何获取 conda 环境的安装路径请参考本文档末尾的 [FAQ](#FAQ)部分。

```bash
$ export PYSPARK_PYTHON=<conda_prefix>/bin/python
```

### 编译安装 PySpark Python 包
如果需要使用 `python <file>` 的方式在 Spark 上运行 python 模块，则需要在 conda 环境中编译安装 pyspark 包。

进入 Conda 环境：

```bash
$ conda activate arctern_env
```

使用以下命令编译安装 pyspark 包:
```bash
$ cd $SPAKR_HOME/python
$ python setup.py install
```

安装完毕后，使用以下命令验证是否成功安装 pyspark：

```bash
$ python -c "import pyspark"
```
如果上述命令没有任何错误信息输出，则表示安装成功。


## 测试样例

### 下载测试模块

执行以下命令下载测试模块：

```bash
$ wget https://raw.githubusercontent.com/arctern-io/arctern/branch-0.3.x/spark/pyspark/examples/gis/spark_udf_ex.py
```

### spark submit 方式提交任务

执行以下命令提交 Spark 任务：

> **注意：** 你需要将 `<path/to/your/spark>` 替换为 Spark 的本地安装路径，将 `<path/to/spark_udf_ex.py>` 替换为本地测试文件的路径。
> **注意：** 此种方式不强制要求进入 Conda 环境。

```bash
$ spark-submit <path/to/spark_udf_ex.py>
```

若最后结果输出包含以下内容，则表示通过测试样例。

```bash
All tests of arctern have passed!
```

### 直接运行测试模块

使用以下命令可以直接运行测试文件:
> **注意：** 你需要将 `<path/to/your/spark>` 替换为 Spark 的本地安装路径，将 `<path/to/spark_udf_ex.py>` 替换为本地测试文件的路径。
> **注意：** 此种方式要求进入 Conda 环境。

```bash
$ python <path/to/spark_udf_ex.py>
```

若最后结果输出包含以下内容，则表示通过测试样例。
```bash
All tests of arctern have passed!
```

# FAQ

## 如何获取 Conda 环境的安装路径

进入 Conda 环境：

```bash
$ conda activate arctern_env
```

运行以下命令获取当前 conda 环境的安装路径：

```bash
 $ echo $CONDA_PREFIX
```
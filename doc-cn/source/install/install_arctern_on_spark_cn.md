# 在 Spark 上安装 Arctern

本文档介绍 Spark 3.0.0 和 Arctern 的安装步骤，以及如何在 Spark 上运行 Arctern。

## 安装 Arctern

请参考如下链接：

* [安装 Arctern](./standalone_installation.md)

## 安装并配置 Spark

以下对 **local** 模式的 Spark 安装和配置流程进行介绍。

> **注意：** 若需要以集群模式安装 Spark ，请参考 [Spark 官方文档](https://spark.apache.org/docs/latest/) 。同时也可以参考 [在 Spark 集群上安装部署 Arctern](./cluster_installation.md)。

### Spark 安装要求

|  名称    |   版本     |
| :---------- | :------------ |
| 操作系统 |Ubuntu LTS 18.04, Centos 7|
| JDK    | JDK 8 |

### 下载 Spark 预编译包

下载 [spark-3.0.0 编译包](https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz) 并解压：

```bash
$ wget https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz
$ tar -xvzf spark-3.0.0-bin-hadoop2.7.tgz
```

### 配置 Spark

执行 `vim ~/.bashrc` 以编辑 **bashrc** 文件。在该文件中添加以下内容:

```bash
export SPARK_HOME=<path/to/spark-3.0.0-bin-hadoop2.7>
export PATH=$SPARK_HOME/bin:$PATH
export SPARK_LOCAL_HOSTNAME=localhost
```

> **注意：**
> * 你需要将 `<path/to/spark-3.0.0-bin-hadoop2.7>` 替换为本地文件夹 **spark-3.0.0-bin-hadoop2.7** 的路径。
> * 你需要重启终端以使上面的设置生效。

创建 **spark-defaults.conf**、**spark-env.sh** 和 **hive-site.xml** 文件：

```bash
$ cd spark-3.0.0-bin-hadoop2.7/conf
$ cp spark-defaults.conf.template spark-defaults.conf
$ cp spark-env.sh.template spark-env.sh
$ touch hive-site.xml
```

在文件 **spark-defaults.conf** 的最后添加以下内容：

> **注意：** 你需要将 `<conda_prefix>` 替换为本地 Conda 环境的安装路径。如何获取 conda 环境的安装路径请参考 [FAQ](#faq)。

```bash
spark.driver.extraClassPath <conda_prefix>/jars/arctern_scala-assembly-0.3.0.jar
spark.executorEnv.PROJ_LIB <conda_prefix>/share/proj
spark.executorEnv.GDAL_DATA <conda_prefix>/share/gdal
spark.executor.extraClassPath <conda_prefix>/jars/arctern_scala-assembly-0.3.0.jar
```

在文件 **spark-env.sh** 的最后添加以下内容：

> **注意：** 你需要将 `<conda_prefix>` 替换为本地 Conda 环境的安装路径。如何获取 conda 环境的安装路径请参考 [FAQ](#faq)。

```bash
$ export PYSPARK_PYTHON=<conda_prefix>/bin/python
```

在文件 **hive-site.xml** 中添加如下内容：

```xml
<configuration>
    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>${user.home}/hive/warehouse</value>
        <description>location of default database for the warehouse</description>
    </property>
</configuration>
```

### 编译安装 PySpark 包

进入 Conda 环境：

```bash
$ conda activate arctern_env
```

编译安装 pyspark 包：

```bash
$ cd $SPAKR_HOME/python
$ python setup.py install
```

验证是否成功安装 pyspark：

```bash
$ python -c "import pyspark"
```
如果上述命令没有错误信息输出，则表示安装成功。

## 测试示例

### 下载测试模块

```bash
$ wget https://raw.githubusercontent.com/arctern-io/arctern/branch-0.3.x/spark/pyspark/examples/gis/spark_udf_ex.py
```

### 提交测试任务

提交 Spark 任务：

> **注意：**
> * 你需要将 `<path/to/your/spark>` 替换为 Spark 的本地安装路径，将 `<path/to/spark_udf_ex.py>` 替换为本地测试文件的路径。
> * 此种方式不强制要求进入 Conda 环境。

```bash
$ spark-submit --master local <path/to/spark_udf_ex.py>
```

若最后结果输出包含以下内容，则表示通过测试示例。

```bash
All tests of arctern have passed!
```

### 直接运行测试模块

你也可以直接运行测试文件：

> **注意：**
> * 你需要将 `<path/to/your/spark>` 替换为 Spark 的本地安装路径，将 `<path/to/spark_udf_ex.py>` 替换为本地测试文件的路径。
> * 此种方式要求进入 Conda 环境。

```bash
$ python <path/to/spark_udf_ex.py>
```

若最后结果输出包含以下内容，则表示通过测试示例：

```bash
All tests of arctern have passed!
```

# FAQ

## 如何获取 Conda 环境的安装路径

进入 Conda 环境：

```bash
$ conda activate arctern_env
```

获取当前 Conda 环境的安装路径：

```bash
 $ echo $CONDA_PREFIX
```
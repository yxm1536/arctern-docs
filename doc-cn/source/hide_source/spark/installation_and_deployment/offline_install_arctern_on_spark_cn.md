# 离线安装

本文档介绍在 Spark 环境中离线安装 Arctern 的步骤。

## 安装要求

| 名称     | 版本              |
| :-------- | :----------------- |
| 操作系统 | Ubuntu LTS 18.04  |

## <span id = "installdependencies">安装依赖项</span>

### 下载离线安装文件

执行以下命令在联网环境中分别下载 Arctern-Spark 的系统依赖、Spark 和 Miniconda 安装文件,并将其拷贝至需要安装 Arctern-Spark 的离线环境。

```bash
$ git clone -b offline https://github.com/zilliztech/arctern-resources.git
$ wget "http://mirror.bit.edu.cn/apache/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz"
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh  
```

> **注意：** 后续工作需在安装 Arctern-Spark 的离线环境中执行。

### 安装系统依赖

在 `arctern-resources` 文件夹所在目录下执行以下指令安装 Arctern-Spark 的系统依赖：

```bash
$ cd arctern-resources/arctern_dependencies/ubuntu_dependencies
$ ./install_packages.sh gl      # 安装gl-mesa库
$ ./install_packages.sh jdk     # 安装java8
```

### 安装 Spark

在 `spark-3.0.0-preview2-bin-hadoop2.7.tgz` 文件所在目录下执行以下命令，将文件解压到指定目录：

```bash
$ mkdir -p ${spark_install_path} && tar zxvf spark-3.0.0-preview2-bin-hadoop2.7.tgz -C ${spark_install_path}
```

### 安装 Miniconda

执行以下命令安装 Miniconda：

```bash
$ /bin/bash ~/miniconda.sh -b -p ${conda_install_path}
```

## 创建 Arctern Conda 离线环境

### 创建 Conda 虚拟环境

执行以下命令创建 Arctern Conda 环境。此处假设环境名称为 `arctern_env`，你可根据需求自行选择合适的环境名称。

```bash
$ . ${conda_install_path}/etc/profile.d/conda.sh
$ conda config --set offline True
$ conda create -n arctern_env
```

创建成功后，可以通过 `conda env list` 命令查看所有 Conda 环境，其输出结果应包含 Arctern 环境，类似如下：

```bash
conda environments:
base         ...
arctern_env      ...
...
```

 进入 Arctern 环境：

```bash
$ conda activate arctern_env
```


> **注意：** 后续工作必须在 conda 虚拟环境 (arctern_env) 中进行。


## 安装 Arctern-Spark

执行以下命令在 Conda 环境中安装 Arctern-Spark：

```bash
$ conda install -n arctern_env -c file:///[path/to/channel] arctern-spark --offline   --override-channels
```

其中， `[path/to/channel]`为 `arctern-resources` 文件夹下 `arctern-resources/arctern_dependencies/conda_dependencies/channel` 目录所在路径，例如:

```bash
$ conda install -n arctern_env -c file:///tmp/arctern-resources/arctern_dependencies/conda_dependencies/channel arctern-spark   --offline --override-channels
```


## 安装验证

进入 Python 环境，尝试导入 `arctern` 和 `arctern_pyspark` 验证安装是否成功。

```python
Python 3.7.6 | packaged by conda-forge | (default, Jan 29 2020, 14:55:04)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import arctern
>>> import arctern_pyspark
```

## 配置 Spark 的 Python 路径

在 `conf/spark-default.conf` 的最后添加以下内容。其中 `[path/to/your/conda]` 为 Conda 的安装路径。

```bash
spark.executorEnv.PROJ_LIB [path/to/your/conda]/envs/arctern_env/share/proj
spark.executorEnv.GDAL_DATA [path/to/your/conda]/envs/arctern_env/share/gdal
```

在文件 `conf/spark-env.sh` 的最后添加以下内容。其中 `[path/to/your/conda]` 为 Conda 的安装路径。

```bash
$ export PYSPARK_PYTHON=[path/to/your/conda]/envs/arctern_env/bin/python
```

### 确认路径配置是否成功

执行以下命令进入 PySpark 交互界面，其中 `[path/to/your/spark]` 为 Spark 的安装路径。

```bash
$ [path/to/your/spark]/bin/pyspark
```

在交互界面中输入以下内容打印 PySpark 的 Python 路径。
```python
>>> import sys
>>> print(sys.prefix)
```

如果终端打印了以下内容，说明 PySpark 的 Python 路径配置成功。

```bash
[path/to/your/conda]/envs/arctern_env
```

## 测试示例

使用测试文件检验 Arctern-Spark 是否安装成功,执行以下命令提交 Spark 任务。

```bash
$ cd arctern-resources/arctern_dependencies/example

# local mode
$ [path/to/your/spark]/bin/spark-submit spark_udf_ex.py

# standalone mode
$ [path/to/your/spark]/bin/spark-submit --master [spark service address] spark_udf_ex.py

# hadoop/yarn mode
$ [path/to/your/spark]/bin/spark-submit --master yarn spark_udf_ex.py
```

如果测试示例运行无误，将在终端打印如下信息：

```
All tests of arctern have passed!
```

## 卸载

在 Conda 环境中执行以下命令可卸载 Arctern-Spark：

```bash
$ conda uninstall libarctern arctern arctern-spark
```

## FAQ

### 对 Spark 的支持

Arctern-Spark 可以运行在 Spark 的各种模式下，需要在每台运行 Spark 的机器上，执行如下操作：

* 创建 Conda 虚拟环境
* 安装 Arctern-Spark
* 配置 Spark 环境变量

如果 Spark 运行在 `standalone` 集群模式下，提交任务机器的 Spark 环境需要与集群的 Spark 环境完全一致，包括以下几点：

* Spark 安装的绝对路径与集群中每台机器完全一致
* Conda 安装的绝对路径与集群中每个机器完全一致
* Conda 虚拟环境名与集群中每个机器完全一致

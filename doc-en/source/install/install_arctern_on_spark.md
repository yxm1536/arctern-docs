# Install Arctern on Spark

This article describes how to install Spark 3.0.0 and Arctern and run Arctern on Spark.

## Install Arctern

See the article below:

* [Install Arctern](./standalone_installation.md)

## Install and configure Spark

The following describes how to install and configure Spark in the **local** mode.

> **Note:** If you need to install Spark in cluster mode, please see [Spark documentation](https://spark.apache.org/docs/latest/). You can also see [Install and deploy Arctern on a Spark cluster](./cluster_installation.md).

### Spark installation requirements

|  Name    |   Version     |
| :---------- | :------------ |
| Operating system | Ubuntu LTS 18.04, Centos 7|
| JDK    | JDK 8 |

### Download Spark pre-compiled package

Download [spark-3.0.0 TGZ file](https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz) and unzip it:

```bash
$ wget https://mirrors.sonic.net/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz
$ tar -xvzf spark-3.0.0-bin-hadoop2.7.tgz
```

### Configure Spark

Run `vim ~/.bashrc` to edit the **bashrc** file. Add the following to the file:

```bash
export SPARK_HOME=<path/to/spark-3.0.0-bin-hadoop2.7>
export PATH=$SPARK_HOME/bin:$PATH
export SPARK_LOCAL_HOSTNAME=localhost
```

> **Note:** 
> * You need to replace `<path/to/spark-3.0.0-bin-hadoop2.7>` with the path to the local folder **spark-3.0.0-bin-hadoop2.7**.
> * You need to restart the terminal for the above settings to take effect.

Create **spark-defaults.conf**, **spark-env.sh** and **hive-site.xml** files:

```bash
$ cd spark-3.0.0-bin-hadoop2.7/conf
$ cp spark-defaults.conf.template spark-defaults.conf
$ cp spark-env.sh.template spark-env.sh
$ touch hive-site.xml
```

Add the following at the end of the **spark-defaults.conf** file:

> **Note:** You need to replace `<conda_prefix>` with the installation path to the local Conda environment. See [FAQ](#faq) for how to obtain the installation path to the conda environment.

```bash
spark.driver.extraClassPath <conda_prefix>/jars/arctern_scala-assembly-0.3.0.jar
spark.executorEnv.PROJ_LIB <conda_prefix>/share/proj
spark.executorEnv.GDAL_DATA <conda_prefix>/share/gdal
spark.executor.extraClassPath <conda_prefix>/jars/arctern_scala-assembly-0.3.0.jar
```

Add the following content at the end of the file **spark-env.sh**:

> **Note:** You need to replace `<conda_prefix>` with the installation path to the local Conda environment. See [FAQ](#faq) for how to obtain the installation path to conda environment.

```bash
$ export PYSPARK_PYTHON=<conda_prefix>/bin/python
```

Add the following content to the file **hive-site.xml**:

```xml
<configuration>
    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>${user.home}/hive/warehouse</value>
        <description>location of default database for the warehouse</description>
    </property>
</configuration>
```

### Compile and install PySpark package

Enter the Conda environment:

```bash
$ conda activate arctern_env
```

Compile and install the pyspark package:

```bash
$ cd $SPAKR_HOME/python
$ python setup.py install
```

Check if PySpark is successfully installed:

```bash
$ python -c "import pyspark"
```

If you do not see any error message, then the installation is successful.


## Test example

### Download the test module

```bash
$ wget https://raw.githubusercontent.com/arctern-io/arctern/branch-0.3.x/spark/pyspark/examples/gis/spark_udf_ex.py
```

### Submit the test task

Submit the Spark task:

> **Note:**
> * You need to replace `<path/to/your/spark>` with the local installation path to Spark, and `<path/to/spark_udf_ex.py>` with the path to the local test file.
> * You are not required to enter the Conda environment.

```bash
$ spark-submit --master local <path/to/spark_udf_ex.py>
```

若最后结果输出包含以下内容，则表示通过测试示例。

```bash
All tests of arctern have passed!
```

### Run the test module directly

You can also run the test file directly:

> **Note:**
> * You need to replace `<path/to/your/spark>` with the local installation path to Spark, and `<path/to/spark_udf_ex.py>` with the path to the local test file.
> * You need to enter the Conda environment.

```bash
$ python <path/to/spark_udf_ex.py>
```

If you see the following message, it means that the test example is passed:

```bash
All tests of arctern have passed!
```

# FAQ

## How to get the installation path of Conda environment

Enter the Conda environment:

```bash
$ conda activate arctern_env
```

Get the installation path to the current Conda environment:

```bash
 $ echo $CONDA_PREFIX
```
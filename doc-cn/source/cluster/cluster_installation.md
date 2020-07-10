# 在 Spark 集群上安装部署 Arctern

本文介绍使用 Docker 技术在一台主机上启动三个容器，并将它们组织成一个 **Standalone** 模式的 Spark 集群。之后，你将在该集群上运行 CPU 版本的 Arctern。三个容器的信息如下：

| Host name |IP address | Container name | Type |
| :--- | :--- | :--- | :--- |
| node_master | 172.18.0.20 | node_master | master |
| node_slave1 | 172.18.0.21 | node_slave1 | worker |
| node_slave2 | 172.18.0.22 | node_slave2 | worker |

## 创建 Docker 子网

创建一个名为 `arcternet` 的 Docker 子网：

```bash
$ docker network create --subnet=172.18.0.0/16 arcternet
```

## 创建集群的共享目录

在 `HOME` 目录下创建 `arcternas`文件夹作为集群的共享目录：

```bash
$ mkdir $HOME/arcternas
```

## 启动容器

使用以下命令启动容器并设置目录 **$HOME/arcternas** 映射到容器内的 **/arcternas**：

```bash
$ docker run -d -ti --name node_master --hostname node_master --net arcternet --ip 172.18.0.20 --add-host node_master:172.18.0.21 --add-host node_master:172.18.0.22 -v $HOME/arcternas:/arcternas ubuntu:16.04 bash
$ docker run -d -ti --name node_slave1 --hostname node_slave1 --net arcternet --ip 172.18.0.21 --add-host node_slave1:172.18.0.20 --add-host node_slave1:172.18.0.22 -v $HOME/arcternas:/arcternas ubuntu:16.04 bash
$ docker run -d -ti --name node_slave2 --hostname node_slave2 --net arcternet --ip 172.18.0.22 --add-host node_slave2:172.18.0.20 --add-host node_slave2:172.18.0.21 -v $HOME/arcternas:/arcternas ubuntu:16.04 bash
```

## 安装基础库和工具

本文使用的Docker 镜像是 `ubuntu:16.04`， 为了方便后续安装操作，需要安装一些基础库和工具。下面以 `node_master` 为例展示如何安装库和工具。

> **注意：** 你需要对 `node_slave1` 和 `node_slave2` 重复下方所述的操作。

使用以下命令进入 Docker 节点：

```bash
$ docker exec -it node_master bash
```

使用以下命令安装基础依赖库和工具:

```bash
apt update
apt install -y wget openjdk-8-jre openssh-server vim
service ssh start
```

使用以下命令新建用户和设置密码:

```
$ useradd -m arcterner -s /bin/bash
$ echo -e "arcterner\narcterner" | passwd arcterner
$ chown -R arcterner:arcterner /arcternas
```
创建了名为 arcterner 的用户，并且密码设置为 arcterner 。


## 设置免密登录

> **注意：** 此操作只在 `node_master` 上执行。

以 `arcterner` 用户登录 `node_master`：

```bash
$ docker exec -it -u arcterner node_master bash
```
使用以下命令设置 ‵node_master` 到所有节点免密登录：

```bash
# 生成 ssh-key，用于免密登录
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
$ ssh-copy-id node_master
$ ssh-copy-id node_slave1
$ ssh-copy-id node_slave2
```

## 在 Spark 上安装 Arctern


## 配置主节点

登录 `node_master`：

```bash
docker exec -it node_master bash
```

执行 `vim ~/spark-3.0.0-bin-hadoop2.7/conf/spark-defaults.conf` 以编辑 **spark-defaults.conf** 文件。文件内容如下:

```txt
spark.executorEnv.PROJ_LIB         /home/arcterner/miniconda3/envs/arctern_env/share/proj
spark.executorEnv.GDAL_DATA        /home/arcterner/miniconda3/envs/arctern_env/share/gdal
spark.executor.memory              2g
spark.executor.cores               1
```

结合 `spark-env.sh` 和 `spark.defaults.conf` 可知，当前的 Spark 集群一共有 `2×3=6` 个 CPU，`4g×3=12g` 内存，并且每个 executor 使用 1 个`cpu`，2 G 内存，一共有 6 个 executor。

执行 `vim ~/spark-3.0.0-bin-hadoop2.7/conf/slaves` 以编辑 **slaves** 文件。文件内容如下:

```txt
node_master
node_slave1
node_slave2
```

## 启动 Spark 集群

启动 `master`：
```bash
$SPARK_HOME/sbin/start-master.sh
```
关闭浏览器代理，在浏览器中输入 `http://172.18.0.20:8080/`，验证 `master` 是否正确启动：

![查看 master](./img/standalone-cluster-start-master.png)

启动 `slaves`：
```bash
$SPARK_HOME/sbin/start-slaves.sh
```

![启动 slaves](./img/standalone-cluster-start-slaves.png)

## 测试 Arctern

新建 **gen.py** 文件用于生成测试数据，内容如下：

```python
from random import random
cnt=1000000
print("idx,pos")
for i in range(0, cnt):
    lng = random()*360 - 180
    lat = random()*180 - 90
    print(i,"point({} {})".format(lng,lat),sep=',')
```

生成测试数据，并将测试数据存入 **/arcternas**：

```bash
python gen.py > /arcternas/pos.csv
```

新建 **st_transform_test.py**，内容如下：

```python
from pyspark.sql import SparkSession
from arctern_pyspark import register_funcs

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("st_transform test") \
        .getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    register_funcs(spark)

    df=spark.read.format("csv").option("header",True).option("delimiter",",").schema("idx long, pos string").load("/arcternas/pos.csv")
    df.printSchema()
    df.createOrReplaceTempView("pos")
    rst = spark.sql("select idx,pos,st_transform(pos, 'epsg:4326', 'epsg:3857') from pos")
    rst.write.mode("append").csv("/arcternas/st_transform/")
    spark.stop()
```

向 Spark 提交 **st_transform_test.py**：

```bash
$SPARK_HOME/bin/spark-submit --master spark://node20:7077 st_transform_test.py
```

检查上述程序的运行结果：

```bash
ls -lh /arcternas/st_transform/
```
你也可以在浏览器中检查上述程序的运行情况：

![运行情况](./img/standalone-cluster-submit-task.png)

## 参考文献

- https://spark.apache.org/docs/latest/spark-standalone.html
- https://www.programcreek.com/2018/11/install-spark-on-ubuntu-standalone-mode/
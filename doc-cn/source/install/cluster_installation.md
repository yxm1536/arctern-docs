# 在 Spark 集群上安装部署 Arctern

本文介绍使用 Docker 技术在一台主机上启动三个容器，并将它们组织成一个 **Standalone** 模式的 Spark 集群。之后，你将在该集群上运行 CPU 版本的 Arctern。三个容器的信息如下：

| Host name |IP address | Container name | Type |
| :--- | :--- | :--- | :--- |
| node-master | 172.18.0.20 | node-master | master |
| node-slave1 | 172.18.0.21 | node-slave1 | worker |
| node-slave2 | 172.18.0.22 | node-slave2 | worker |

## 创建 Docker 子网

创建一个名为 `arcternet` 的 Docker 子网：

```bash
$ docker network create --subnet=172.18.0.0/16 arcternet
```

如果你看到以下提示，则表示该子网已经存在，无需创建子网。你也可以删除现有子网，然后重新创建子网；或者尝试创建其它网段的子网。

```
Error response from daemon: Pool overlaps with other one on this address space
```

创建完毕后，可以通过以下命令查看创建的子网：

```bash
$ docker network ls
```

## 启动容器

```bash
$ docker run -d -ti --name node-master --hostname node-master --net arcternet --ip 172.18.0.20 --add-host node-slave1:172.18.0.21 --add-host node-slave2:172.18.0.22  ubuntu:18.04 bash
$ docker run -d -ti --name node-slave1 --hostname node-slave1 --net arcternet --ip 172.18.0.21 --add-host node-master:172.18.0.20 --add-host node-slave2:172.18.0.22  ubuntu:18.04 bash
$ docker run -d -ti --name node-slave2 --hostname node-slave2 --net arcternet --ip 172.18.0.22 --add-host node-master:172.18.0.20 --add-host node-slave1:172.18.0.21  ubuntu:18.04 bash
```

## 安装基础库和工具

本文使用的 Docker 镜像是 `ubuntu:18.04`，需要安装一些基础库和工具。下面以 `node-master` 为例介绍安装步骤。

> **注意：** 你需要对 `node-slave1` 和 `node-slave2` 重复下方所述的操作。

进入 `node-master` 节点：

```bash
$ docker exec -it node-master bash
```

使用以下命令安装基础依赖库和工具：

```bash
$ apt update
$ apt install -y wget openjdk-8-jre openssh-server vim sudo
$ service ssh start
```

新建用户 `arcterner` 并将密码设置为 `arcterner`：

```
$ useradd -m arcterner -s /bin/bash -G sudo
$ echo -e "arcterner\narcterner" | passwd arcterner
```

## 设置免密登录

> **注意：** 此操作只在 `node-master` 上执行。

以 `arcterner` 用户登录 `node-master`：

```bash
$ docker exec -it -u arcterner node-master bash
```

设置 `node-master` 到所有节点免密登录：

```bash
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
$ ssh-copy-id node-master
$ ssh-copy-id node-slave1
$ ssh-copy-id node-slave2
```

## 部署 Spark 和 Arctern

> **注意：** 你需要以 `arcterner` 用户登录所有 Docker 节点部署 Spark 和 Arctern。

参考以下方式：

* [在 Spark 上安装 Arctern](./install_arctern_on_spark_cn.md)

## 配置 Spark 集群

以 `arcterner` 用户登录 `node-master` 。执行 `vim ~/spark-3.0.0-bin-hadoop2.7/conf/slaves` 以编辑 **slaves** 文件。文件内容如下：

```
node-master
node-slave1
node-slave2
```

执行 `vim ~/spark-3.0.0-bin-hadoop2.7/conf/spark-defaults.conf` 以编辑 **spark-defaults.conf** 文件。在该文件中添加以下内容：

```bash
spark.master  spark://node-master:7077
```

## 启动 Spark 集群

以 `arcterner` 用户登录 `node-master` 并启动集群：

```bash
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh
```

关闭 `node-master` 宿主机的 HTTP 代理，在宿主机的浏览器中输入 `http://172.18.0.20:8080/`，验证 Spark 集群是否正确启动：

![查看集群](./img/check_cluster.png)

## 验证部署

以 `arcterner` 用户登录 `node-master`，并进入 Conda 环境：

```bash
$ conda activate arctern_env
```

验证是否部署成功：

```bash
$ export PYSPARK_PYTHON=$CONDA_PREFIX/bin/python
$ python -c "from arctern_spark import examples;examples.run_geo_functions_test()"
```

若输出结果包含以下内容，则表示通过测试示例。

```bash
All tests have passed!
```

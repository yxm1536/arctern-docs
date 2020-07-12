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
如果提示
```
Error response from daemon: Pool overlaps with other one on this address space
```
则需表示已经有该子网，则无需创建子网，或者删除现有子网重新创建，或者尝试创建其它网段的子网。

创建完毕后，可以通过以下命令查看创建的子网：
```bash
$ docker network ls
```

## 创建集群的共享目录

在 `HOME` 目录下创建 `arcternas`文件夹作为集群的共享目录：

```bash
$ mkdir $HOME/arcternas
```

## 启动容器

使用以下命令启动容器并设置目录 **$HOME/arcternas** 映射到容器内的 **/arcternas**：

```bash
$ docker run -d -ti --name node_master --hostname node_master --net arcternet --ip 172.18.0.20 --add-host node_slave1:172.18.0.21 --add-host node_slave2:172.18.0.22 -v $HOME/arcternas:/arcternas ubuntu:18.04 bash
$ docker run -d -ti --name node_slave1 --hostname node_slave1 --net arcternet --ip 172.18.0.21 --add-host node_master:172.18.0.20 --add-host node_slave2:172.18.0.22 -v $HOME/arcternas:/arcternas ubuntu:18.04 bash
$ docker run -d -ti --name node_slave2 --hostname node_slave2 --net arcternet --ip 172.18.0.22 --add-host node_master:172.18.0.20 --add-host node_slave1:172.18.0.21 -v $HOME/arcternas:/arcternas ubuntu:18.04 bash
```

## 安装基础库和工具

本文使用的 Docker 镜像是 `ubuntu:18.04`，需要安装一些基础库和工具。下面以 `node_master` 为例介绍安装步骤。

> **注意：** 你需要对 `node_slave1` 和 `node_slave2` 重复下方所述的操作。

使用以下命令进入 `node_master` 节点：

```bash
$ docker exec -it node_master bash
```

使用以下命令安装基础依赖库和工具:

```bash
$ apt update
$ apt install -y wget openjdk-8-jre openssh-server vim sudo
$ service ssh start
```

使用以下命令新建用户 `arcterner` 并将密码设置为 `arcterner`:

```
$ useradd -m arcterner -s /bin/bash -G sudo
$ echo -e "arcterner\narcterner" | passwd arcterner
$ chown -R arcterner:arcterner /arcternas
```

## 设置免密登录

> **注意：** 此操作只在 `node_master` 上执行。

以 `arcterner` 用户登录 `node_master`：
```bash
$ docker exec -it -u arcterner node_master bash
```

使用以下命令设置 ‵node_master` 到所有节点免密登录：
```bash
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
$ ssh-copy-id node_master
$ ssh-copy-id node_slave1
$ ssh-copy-id node_slave2
```

## 部署 Spark 和 Arctern

> **注意：** 你需要以 `arcterner` 用户登录所有 Docker 节点并部署 Spark 和 Arctern。

参考以下方式：

* [在 Spark 上部署 Arctern](./install_arctern_on_spark_cn.md)

## 配置 Spark 集群

以 `arcterner` 用户登录 `node_master` 并执行 `vim ~/spark-3.0.0-bin-hadoop2.7/conf/slaves` 以编辑 **slaves** 文件。文件内容如下:

```
node_master
node_slave1
node_slave2
```



## 启动 Spark 集群

以 `arcterner` 用户登录 `node_master` 并执行以下命令来启动集群：

```bash
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh
```

关闭`node_master`宿主机的浏览器代理，在宿主机的浏览器中输入 `http://172.18.0.20:8080/`，验证 spark 集群是否正确启动：

![查看 master](./img/standalone-cluster-start-master.png)
![启动 slaves](./img/standalone-cluster-start-slaves.png)

## 验证部署

以 `arcterner` 用户登录 `node_master`：

```bash
$ docker exec -it -u arcterner node_master bash
```

进入 Conda 环境：

```bash
$ conda activate arctern_env
```

使用以下命令验证是否部署成功：

```bash
$ python -c "from arctern_spark import examples;examples.run_geo_functions_test()"
```

若输出结果包含以下内容，则表示通过测试样例。

```bash
All tests have passed!
```
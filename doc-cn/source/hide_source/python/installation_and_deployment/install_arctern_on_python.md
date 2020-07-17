# 安装部署

本文档引导你在 Python 环境中安装 Arctern。

## 安装要求

* CPU 版本

|  名称    |   版本     |
| :---------- | :------------ |
| 操作系统 |Ubuntu LTS 18.04|
| Conda  | Miniconda Python3  |

* GPU 版本

|  名称    |   版本     |
| :---------- | :------------ |
| 操作系统 |Ubuntu LTS 18.04|
| Conda | Miniconda Python3  |
|CUDA|10.0|
|Nvidia driver|4.30|

## 安装依赖库

* CPU 版本

执行以下命令安装 Arctern CPU 版本的依赖库：

```bash
$ sudo apt install libgl-dev libosmesa6-dev libglu1-mesa-dev
```

* GPU 版本

执行以下命令安装 Arctern GPU 版本的依赖库：

```bash
$ sudo apt install libgl1-mesa-dev libegl1-mesa-dev
```

## 创建 Arctern Conda 环境

执行以下命令创建 Arctern Conda 环境。此处假设环境名称为 `arctern_env`，你可根据需求自行选择合适的环境名称。

```bash
$ conda create -n arctern_env -c conda-forge python=3.7.6
```

成功创建 Conda 环境后，你可以通过 `conda env list` 命令查看所有 Conda 环境，其输出结果应包含 Arctern 环境，类似如下：
  
```bash
conda environments:
base                ...
arctern_env      ...
...
```

进入 Arctern 环境：

```bash
$ conda activate arctern_env
```

> **注意：** 后续工作必须在 Arctern Conda 环境中进行。

## 安装 Arctern

* CPU 版本
  
执行以下命令在 Conda 环境中安装 Arctern CPU 版本：

```bash
$ conda install -c arctern -c conda-forge arctern
```

* GPU版本
  
执行以下命令在 Conda 环境中安装 Arctern GPU 版本：

```bash
$ conda install -c arctern/label/cuda10.0 -c conda-forge libarctern 
$ conda install -c arctern -c conda-forge arctern
```

## 安装验证

进入 Python 环境，尝试导入 `arctern` 并确认版本是否正确。

```python
>>> import arctern
>>> arctern.version()
```

## 测试示例

```bash
# 安装 py.test
$ conda install pytest

# 下载测试文件
$ wget https://raw.githubusercontent.com/zilliztech/arctern/v0.1.0/python/tests/geo/geo_test.py

# 执行测试文件
$ py.test [/path/to/]geo_test.py
33 passed, 1 warning in 0.58s
```

## 卸载

```bash
$ conda uninstall libarctern arctern
```

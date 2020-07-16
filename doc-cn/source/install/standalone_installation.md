# 安装部署

本文档将引导你在单机模式下安装 Arctern。

## 系统要求

* CPU 版本

| 名称     | 版本              |
| :------- | :---------------- |
| 操作系统 | Ubuntu LTS 18.04  |
| Conda    | Miniconda Python3 |

* GPU 版本

| 名称          | 版本              |
| :------------ | :---------------- |
| 操作系统      | Ubuntu LTS 18.04, Centos 7  |
| Conda         | Miniconda Python3 |
| CUDA          | 10.0              |
| NVIDIA driver | 4.30              |

> **注意：** 你可以到 [NVIDIA 官网](https://developer.nvidia.com/cuda-gpus) 查询你的 GPU 是否支持 CUDA 功能。

## 安装依赖库

### Ubuntu

* CPU 版本

```bash
$ sudo apt install libgl-dev libosmesa6-dev libglu1-mesa-dev
```

* GPU 版本

```bash
$ sudo apt install libgl1-mesa-dev libegl1-mesa-dev
```

> **注意：** 如果安装失败，请先执行 `sudo apt update` 再执行以上命令。

### Centos

```bash
$ sudo yum install mesa-libGLU-devel mesa-libOSMesa-devel
```

## 安装 Miniconda

安装 [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install)：

```
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh -b
$ echo "source $HOME/miniconda3/etc/profile.d/conda.sh" >> $HOME/.bashrc
```

关闭当前终端，并重新打开一个新的终端。在新终端中打印所有 Conda 环境。若出现 `base` 环境，则 Conda 安装成功。

```bash
$ conda env list
base                   * /home/arcterner/miniconda3
```

## 安装 Arctern

安装 Arctern 并创建名为 `arctern_env` 的 Conda 环境：

* CPU 版本

```bash
$ conda create -n arctern_env -c conda-forge -c arctern arctern
```

* GPU版本

```bash 
$ conda create -n arctern_env -c conda-forge -c arctern/label/cuda10.0 arctern
```

进入 Conda 环境：

```bash
$ conda activate arctern_env
```

## 安装验证

进入 Python 环境，尝试导入 `arctern` 并确认版本是否正确。

```python
>>> import arctern
>>> arctern.__version__
>>> arctern.version(verbose=True)
```

## 卸载 Arctern

```bash
$ conda deactivate
$ conda remove -n arctern_env --all
```

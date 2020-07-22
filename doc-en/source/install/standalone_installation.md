# Installation

This article describes how to install Arctern in standalone mode.

## System requirements

* CPU version

| Name             | Version           |
| :--------------- | :---------------- |
| Operating system | Ubuntu LTS 18.04  |
| Conda            | Miniconda Python3 |

* GPU version

| Name             | Version           |
| :--------------- | :---------------- |
| Operating system | Ubuntu LTS 18.04, Centos 7  |
| Conda            | Miniconda Python3 |
| CUDA             | 10.0              |
| NVIDIA driver    | 4.30              |

> **Note:** You can go to the [NVIDIA website](https://developer.nvidia.com/cuda-gpus) to check whether you have a CUDA-enabled GPU.

## Installing dependencies

### Ubuntu

* CPU version

```bash
$ sudo apt install libgl-dev libosmesa6-dev libglu1-mesa-dev
```

* GPU version

```bash
$ sudo apt install libgl1-mesa-dev libegl1-mesa-dev
```

> **Note:** If the installation fails, please run `apt update` and then run the above commands again.

### Centos

```bash
$ sudo yum install mesa-libGLU-devel mesa-libOSMesa-devel
```

## Installing Miniconda

Install [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install)：

```
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh -b
$ echo "source $HOME/miniconda3/etc/profile.d/conda.sh" >> $HOME/.bashrc
```

Close the current terminal. Then, open a new terminal and run the commands below to list all Conda environments in it. Conda installation is successful if the `base` environment is printed.

```bash
$ conda env list
base                   * /home/arcterner/miniconda3
```

## Installing Arctern

Install Arctern and create a Conda environment named `arctern_env`:

* CPU version

```bash
$ conda create -n arctern_env -c conda-forge -c arctern arctern
```

* GPU version

```bash 
$ conda create -n arctern_env -c conda-forge -c arctern/label/cuda10.0 arctern
```

Enter the Conda environment:

```bash
$ conda activate arctern_env
```

## Installation verification

In the Python environment, try to import `arctern` and check whether it is the latest version:

```python
>>> import arctern
>>> print(arctern.version())
version : 0.2.0
```

## Uninstalling Arctern

```bash
$ conda deactivate
$ conda remove -n arctern_env --all
```

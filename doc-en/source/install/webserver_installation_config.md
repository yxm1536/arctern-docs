# Install and deploy Arctern RESTful server

## Install Arctern backend

Arctern RESTful Server only takes charge of receiving and parsing RESTful requests. Actual operations are performed by the Arctern backend. Before installing Arctern RESTful Server, you need to install the Arctern backend in advance. Currently, Arctern RESTful Server supports two Arctern backend systems, which are based on Python and Spark respectively. You can choose to install and use one type of backend.

### Install Python-based Arctern backend

See the following article:

* [Install Arctern](./standalone_installation.md)

### Install Spark-based Arctern backend

See the following article:

* [Install Arctern on Spark](./install_arctern_on_spark.md)

## Install Arctern RESTful server

Build a Conda environment for Arctern RESTful server:

> **Note:** Here we name the environment `arctern_server_env`. You can use another name according to your needs.

```bash
$ conda create -n arctern_server_env -c conda-forge -c arctern arctern-webserver
```

> **Note:** If you want to install the Arctern backend and Arctern RESTful server on the same computer, it is recommended that they use different Conda environments. For example, create an environment called `arctern_env` for the Arctern backend and an environment called `arctern_server_env` for the Arctern RESTful server.

## Set up workspace

Enter the `arctern_server_env` virtual environment:

```bash
$ conda activate arctern_server_env
```

The workspace folder is used to store the third-party tools, extensions, and system configuration files that Arctern RESTful server depends on. Before starting RESTful Server for the first time, you need to set the workspace through the `bootstrap` command.

> **Note:** Here we specify `workspace` as `/home/usr/arctern_server/`, you can choose the appropriate path according to your needs.

```bash
arctern-server bootstrap --workspace=/home/usr/arctern_server/
```

## Configure Arctern RESTful server

Arctern RESTful server provides a set of system configurations, including service port, IP address, data processing backend, and so on. The `interpreter_type` option controls the selection of different data processing backends (such as Python or PySpark).

If you choose Python as the backend, you can configure it according to the following command. For detailed information about configurations, please refer to [Arctern RESTful server configurations](../restful/restful_config.md):

```bash
arctern-server config --arctern_server_host=127.0.0.1 --arctern_server_port=8080 --interpreter_type=python --interpreter_name=arcternpython --interpreter_python_path="</path/to/python>"
```

If you choose Spark as the backend, you can configure it according to the following command. For detailed information about configurations, please refer to [Arctern RESTful server configurations](../restful/restful_config.md):

```bash
arctern-server config --arctern_server_host=127.0.0.1 --arctern_server_port=8080 --interpreter_type=pyspark --interpreter_name=arcternpyspark --interpreter_pyspark_python="</path/to/python>" --interpreter_pyspark_driver_python=</path/to/python> --interpreter_spark_home="</path/to/spark>" --interpreter_master=local
```

> **Note:**
> * You need to replace `</path/to/python>` with the absolute path to Python in the Arctern Conda environment. See [FAQ](#faq) for details about how to obtain the path.
> * You also need to replace `</path/to/spark>` with Spark's HOME path.

## Start Arctern RESTful server

```bash
arctern-server start --mode=release
```

`mode` can be `release` or `debug`. The `debug` mode provides more accurate information, but it is less efficient than the `release` mode.

## FAQ

### How to get the path to Python in the Arctern Conda environment

Enter the Arctern Conda environment:

```bash
$ conda activate arctern_env
```

Get the path to python:

```bash
$ which python
```

### The impact of using HTTP proxy on Arctern RESTful server

Using the HTTP proxy may cause the failure of calling RESTful APIs. Please close the HTTP proxy and restart Arctern RESTful Server.
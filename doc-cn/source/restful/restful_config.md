# Arctern RESTful Server 配置项

* `interpreter`： Arctern 数据分析后台的相关配置。
    - `interpreter_type`： 解释器类型，可选类型包括 `python` 和 `pyspark`。
    - `interpreter_name`： 自定义的解释器名称，如 `python3`。
    - `interpreter_python_path`: Python 解释器所在的绝对路径。
    - `interpreter_spark_home`： Spark 所在的绝对路径。
    - `interpreter_master`： Spark master 节点模式，可选模式包括 `local` 和 `standalone`。

        > **注意：** 
        > * 在 local 模式下，Spark 在一个物理节点内运行。配置示例如 `--interpreter_master=local[8]`，其中 `[8]` 表示使用 8 个 CPU。
        > * 在 standalone 模式下，你需要指定 maseter url。配置示例如 `--interpreter_master=spark://IP:PORT`。
        
    - `interpreter_pyspark_python`： Spark executor 的 Python 解释器的绝对路径。
    - `interpreter_pyspark_driver_python`： Spark driver 的 Python 解释器的绝对路径。

* `arctern server`: Arctern RESTful Server 的相关配置。
   - `arctern_server_host`: Arctern RESTful Server 的 IP 地址。
   - `arctern_server_port`: Arctern RESTful Server 的端口号。

* `zepplin`： Arctern RESTful Server 所使用的 Zeppelin 系统的相关配置。
    - `zeppelin_port`： Zeppelin 的端口号。
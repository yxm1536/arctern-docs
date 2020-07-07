#!/bin/bash -e

function compile_arctern() {
  cd / && \
  wget https://github.com/Kitware/CMake/releases/download/v3.16.8/cmake-3.16.8-Linux-x86_64.tar.gz && \
  tar vxf cmake-3.16.8-Linux-x86_64.tar.gz && \
  export PATH=/cmake-3.16.8-Linux-x86_64/bin:$PATH && \
  cd / && git clone https://github.com/arctern-io/arctern.git -b ${1} && cd arctern && \
  cd cpp && mkdir build && cd build && \
  cmake .. -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} -DCMAKE_BUILD_TYPE=Release -DBUILD_UNITTEST=ON && \
  make && make install && \
  cd ../../python && \
  python setup.py build build_ext && python setup.py install && \
  cd ../spark/pyspark && \
  ./build.sh && cd ../../ && \
  cd scala/ && /opt/sbt/bin/sbt "set test in assembly := {}" clean assembly && \
  cd ../spark/ && python setup.py install
}

function compile_arctern_docs {
  pip install sphinx && \
  pip install sphinx_automodapi && \
  pip install sphinx_rtd_theme && \
  pip install --upgrade recommonmark && \
  pip install sphinx-markdown-tables==0.0.3 && \
  pip install sphinx-intl && \
  pip install pyspark && \
  cd /arctern-docs/doc-cn && \
  mkdir build && python create_html.py && mv build build-cn && \
  cd /arctern-docs/doc-en && \
  python compile.py && \
  make doctest && \
  mv build build-en
}

source /opt/conda/etc/profile.d/conda.sh
conda env create -n arctern-doc -f /arctern-docs/docker/arctern-conda-dep.yml && \
conda activate arctern-doc && \
ARCTERN_BRANCH=`cat /arctern-docs/version.json | jq -r .arctern_compile_branch` && \
export SPARK_HOME=/opt/spark-3.0.0-bin-hadoop2.7 && \
export PATH=/opt/spark-3.0.0-bin-hadoop2.7/bin:$PATH && \
export PYSPARK_PYTHON=/opt/conda/envs/arctern-doc/bin/python && \
export PYSPARK_DRIVER_PYTHON=/opt/conda/envs/arctern-doc/bin/python && \
compile_arctern ${ARCTERN_BRANCH} && \
cd /opt/spark-3.0.0-bin-hadoop2.7/conf && \
cp spark-defaults.conf.template spark-defaults.conf && \
echo "spark.driver.extraClassPath /arctern/scala/target/scala-2.12/arctern_scala-assembly-$(echo 0.1).jar" >> spark-defaults.conf && \
echo "spark.executor.extraClassPath /arctern/scala/target/scala-2.12/arctern_scala-assembly-$(echo 0.1).jar" >> spark-defaults.conf && \
compile_arctern_docs && \
python -c "import arctern;print(arctern.version())"

#!/bin/bash -e

function compile_arctern() {
  cd / && \
  wget https://github.com/Kitware/CMake/releases/download/v3.16.8/cmake-3.16.8-Linux-x86_64.tar.gz && \
  tar vxf cmake-3.16.8-Linux-x86_64.tar.gz && \
  export PATH=/cmake-3.16.8-Linux-x86_64/bin:$PATH && \
  cd / && git clone https://github.com/xiaocai2333/arctern.git -b czs_0.3.x && cd arctern && \
  cd cpp && mkdir build && cd build && \
  cmake .. -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} -DCMAKE_BUILD_TYPE=Release -DBUILD_UNITTEST=ON && \
  make && make install && \
  cd ../../python && \
  python setup.py build build_ext && python setup.py install && \
  cd ../spark/pyspark && \
  ./build.sh && cd ../../ && \
  cd scala/ && sbt "set test in assembly := {}" clean assembly && \
  cd ../spark/ && python setup.py install
}

function compile_arctern_docs {
  # arctern-docs dependencies
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
  make doctest && rm -rf build && \
  mkdir build && python compile.py && mv build build-en
}

source /opt/conda/etc/profile.d/conda.sh
conda env create -n arctern-doc -f /arctern-docs/docker/arctern-conda-dep.yml && \
conda activate arctern-doc && \
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list && \
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add && \
sudo apt-get update && \
sudo apt-get install sbt && \
ARCTERN_BRANCH=`cat /arctern-docs/version.json | jq -r .arctern_compile_branch` && \
compile_arctern ${ARCTERN_BRANCH} && \
export PYSPARK_PYTHON="/opt/conda/envs/arctern-doc/bin/python" && \
export PYSPARK_DRIVER_PYTHON="/opt/conda/envs/arctern-doc/bin/python" && \
cd /opt/spark-3.0.0-bin-hadoop2.7/conf && \
cp spark-defaults.conf.template spark-defaults.conf && \
echo "spark.driver.extraClassPath /arctern/scala/target/scala-2.12/arctern_scala-assembly-0.1.jar" >> spark-defaults.conf && \
echo "spark.executor.extraClassPath /arctern/scala/target/scala-2.12/arctern_scala-assembly-0.1.jar" >> spark-defaults.conf && \
compile_arctern_docs && \
python -c "import arctern;print(arctern.version())"

#!/bin/bash -e
source /opt/conda/etc/profile.d/conda.sh
conda create -n arctern-doc -c conda-forge -c arctern arctern && \
conda activate arctern-doc

# arctern-docs dependencies
pip install sphinx && \
pip install sphinx_automodapi && \
pip install sphinx_rtd_theme && \
pip install --upgrade recommonmark && \
pip install sphinx-markdown-tables==0.0.3 && \
pip install sphinx-intl && \
pip install pyspark && \
cd / && echo "--------" && tree -d /arctern-docs && echo "--------" && \
cd /arctern-docs/doc-cn && \
mkdir build && python create_html.py && mv build build-cn &&\
cd /arctern-docs/doc-en && \
mkdir build && python compile.py && mv build build-en &&\
tree -d build-en

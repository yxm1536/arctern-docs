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
pip install pyspark

# compile arctern-doc-cn
cd / && echo "--------" && tree /arctern-docs && echo "--------" && \
cd /arctern-docs/doc-cn && \
mkdir build && python create_html.py && mv build build-cn &&\
git config --global user.email "Arctern-doc-bot@zilliz.com" && \
git config --global user.name "Arctern-doc-bot"&& \
git status && \
git remote -v && \
git branch && \
cd /arctern-docs && \
git checkout -b `cat version.json | jq -r .version` && git add . && \
git commit -m "Arctern-bot release doc" && \
git push -f origin HEAD:`cat version.json | jq -r .version`
# cd /arctern-docs/doc-en && \
# mkdir build && python compile.py && mv build build-en &&\
# tree build-en
# git push

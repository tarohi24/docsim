#/bin/bash

DIR="../../data/ntcir/orig/collection"
for file in ${DIR}/*.txt;
do
    perl tagger.perl ${file} > ${DIR}/tagged/$(basename ${file})
done

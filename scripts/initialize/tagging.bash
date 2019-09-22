#/bin/bash

DIR="../../data/ntcir/orig/collection"
ls ${DIR}/*.txt | xargs -n 1 -I {} perl tagger.perl {} > ${DIR}/tagged/$(basename {})

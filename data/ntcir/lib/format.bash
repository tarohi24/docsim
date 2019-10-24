RAWDATA_DIR="~/ntcir"
OUTDIR="${HOME}/docsim/data/ntcir/orig/collection/formatted"
for year in {1993..2002};
do
    echo ${year};
    mkdir -p "${OUTDIR}/${year}";
    INFILE="${RAWDATA_DIR}/tcdata_patent_DIC10012_${year}.txt.gz";
    # accept from stdin
    perl tagger.perl ${INFILE} | split - -l 50 -d "${OUTDIR}/${year}/";
done

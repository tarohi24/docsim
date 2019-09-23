for year in {1993..2002};
do
    infile="../../../data/ntcir/orig/collection/tagged/tcdata_patent_DIC10012_${year}.txt"
    outdir="../../../data/ntcir/orig/collection/splitted/${year}"
    python split_file.py -i ${infile} -o ${outdir};
done;

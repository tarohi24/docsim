import json


with open('gt.qrel') as fin:
    lines = [line.split() for line in fin.read().splitlines()]

with open('name_mapping.json') as fin:
    dic = json.load(fin)

with open('../../results/ir/ntcir/gt.qrel', 'w') as fout:
    for line in lines:
        fout.write(' '.join([
            dic[line[0]].replace('-', ''),
            line[1],
            line[2][15:].replace('-', ''),
            line[3]]))
        fout.write('\n')

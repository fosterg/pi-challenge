#!/usr/bin/env python

# Read a tsv version of Pierre's spreadsheet on stdin and write a version for
# upload to Crowdflower in which system columns have been randomized.

# Input 9 fields: id, ling issue, question|comment, source, [4 x system outputs], reference
# output 13 fields: id, ling issue, question, source, reference, [4 x randomized system outputs], [4 x system ids]

import sys
import random

# process header
header = sys.stdin.readline().rstrip()
fields = header.split('\t')
assert len(fields) == 9, "expecting 9 fields"
for i in range(len(fields)):
   if fields[i] == 'COMMENT':
      fields[i] = 'QUESTION'
sys_ids = fields[4:8]

# write new header
out_header = ['ID'] + fields[1:4] + ['REFERENCE'] + \
    ['System%d' % i for i in xrange(1,5)] + \
    ['System%d id' % i for i in xrange(1,5)]
print "\t".join(out_header)

for line in sys.stdin:
    line = line.rstrip()
    if line == "":
        continue
    fields = line.split('\t')

    # randomize system outputs
    outputs = fields[4:8]
    for i in xrange(len(outputs)):
        outputs[i] = outputs[i] + '\t' + sys_ids[i]
        outputs[i] = outputs[i].replace('[', '').replace(']', '')
    random.shuffle(outputs)
    ids = [t.split('\t')[1] for t in outputs]
    outputs = [t.split('\t')[0] for t in outputs]

    # create and print new record
    outputs = fields[0:4] + [fields[-1]] + outputs + ids
    # fill in missing ling. issue and question values
    for i in xrange(1,3):
        if outputs[i].strip() == "":
            outputs[i] = old_outputs[i]
    print "\t".join(outputs)

    old_outputs = outputs

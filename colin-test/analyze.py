#!/usr/bin/env python

import json
import sys

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: analyze.py json-download"
    sys.exit(1)

# TODO: more systematic utf8 conversion

questions = []
with open(sys.argv[1]) as f:
    for line in f:
        res = json.loads(line)
        res_utf8 = dict((key.encode("UTF-8"), value) for (key,value) in res.items())
        data = res_utf8['data']
        res_utf8['data'] = dict((key.encode("UTF-8"), value.encode("UTF-8")) for (key,value) in data.items())
        questions.append(res_utf8)

print questions[0]

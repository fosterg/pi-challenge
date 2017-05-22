#!/usr/bin/env python

import json
import sys

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: analyze.py json-download"
    sys.exit(1)


def print_hier(x, prefix):
    if isinstance(x, dict):
        for k in x.keys():
            print prefix + k + ':'
            print_hier(x[k], prefix + "   ")
    else:
        print prefix, x

# report = "report1"
# report = "report2"
# report = "agree"
report = "sys_scores"

if report == "report2":
    print "%s\t%s\t%s\t%s\t%s" % ("question id", "NRC PBMT", "NRC PBMT2", "NRC's NMT", "Google's NMT (March 2017)")

# [full, two-way, not]
agreement = {
    'all': [0, 0, 0],
    "NRC PBMT" : [0, 0, 0],
    "NRC PBMT2" : [0, 0, 0],
    "NRC's NMT" : [0, 0, 0],
    "Google's NMT (March 2017)" : [0, 0, 0],
    "MorphoSyn" : [0, 0, 0],
    "LexSyn" : [0, 0, 0],
    "Syn" : [0, 0, 0],
}
for i in range(1, 26+1):
    agreement["S" + str(i)] = [0, 0, 0]

sys_scores = {}
for s in ["NRC PBMT", "NRC PBMT2", "NRC's NMT", "Google's NMT (March 2017)"]:
   sys_scores[s] = {}
   for c in ["tot", "MorphoSyn", "LexSyn", "Syn"]:
      sys_scores[s][c] = [0, 0]  # yes, no

with open(sys.argv[1]) as f:
    for line in f:
        res = json.loads(line)
        assert(len(res['results']['judgments']) == 3)  # order is Eric, Cyril, Michel

        judgments = res['results']['judgments']
        question_data = judgments[0]['unit_data']
        question_id = question_data['id']
        answers = {}
        answers[question_data['system1_id']] = []
        answers[question_data['system2_id']] = []
        answers[question_data['system3_id']] = []
        answers[question_data['system4_id']] = []

        for worker in range(3):
            answers[question_data['system1_id']].append(judgments[worker]['data']['r1'])
            answers[question_data['system2_id']].append(judgments[worker]['data']['r2'])
            answers[question_data['system3_id']].append(judgments[worker]['data']['r3'])
            answers[question_data['system4_id']].append(judgments[worker]['data']['r4'])

        # Eric's post-hoc changes
        # 19b, NRC's NMT: Not applicable -> No
        # 19c, 1st three systems: Not applicable -> No
        # 19d, 1st two systems: Not applicable -> No
        # 19f, NRC's NMT: Not applicable -> No
        if question_id == 'S19b':
            answers["NRC's NMT"][0] = "No"
        elif question_id == 'S19c':
            answers["NRC PBMT"][0] = "No"
            answers["NRC PBMT2"][0] = "No"
            answers["NRC's NMT"][0] = "No"
        elif question_id == 'S19d':
            answers["NRC PBMT"][0] = "No"
            answers["NRC PBMT2"][0] = "No"
        elif question_id == 'S19f':
            answers["NRC's NMT"][0] = "No"

        out = question_id
        for s in ["NRC PBMT", "NRC PBMT2", "NRC's NMT", "Google's NMT (March 2017)"]:
            if report == "report1":
                out += '\t' + s + '\t' + ','.join(answers[s])
            elif report == "report2":
                out += '\t' + ','.join(answers[s])

            if answers[s][0] == answers[s][1] == answers[s][2]:
                ag = 0          # full agreement
            elif answers[s][0] != answers[s][1] and answers[s][1] != answers[s][2]:
                ag = 2          # no agreement
            else:
                ag = 1          # partial agreement
            agreement['all'][ag] += 1
            agreement[s][ag] += 1
            
            qprefix = question_id
            for i in range(0, len(qprefix)):
                if qprefix[i] in "abcdefghijklmnopqrstuvwxyz":
                    qprefix = qprefix[:i]
                    break
            agreement[qprefix][ag] += 1

            snum = int(qprefix[1:])
            if snum in range(1, 8):
               c = "MorphoSyn"
               agreement["MorphoSyn"][ag] += 1
            elif snum in range(9, 16):
               c = "LexSyn"
               agreement["LexSyn"][ag] += 1
            else:
               c = "Syn"
               agreement["Syn"][ag] += 1

            for a in [0, 1, 2]:
               if answers[s][a] == "Yes":
                  ii = 0
               elif answers[s][a] == "No":
                  ii = 1
               else:
                  continue  # don't count n/a scores
               sys_scores[s]["tot"][ii] += 1
               sys_scores[s][c][ii] += 1

        if report in ["report1", "report2"]:
            print out

if report == "agree":
    for k in ['all', "NRC PBMT", "NRC PBMT2", "NRC's NMT", "Google's NMT (March 2017)", "MorphoSyn", "LexSyn", "Syn"]:
        print "%s: full=%d partial=%d none=%d agreement=%3.2f" % (k, agreement[k][0], agreement[k][1], agreement[k][2], 100.0 * agreement[k][0] / sum(agreement[k]))
    for i in range(1, 26+1):
        k = "S" + str(i)
        print "%s: full=%d partial=%d none=%d agreement=%3.2f" % (k, agreement[k][0], agreement[k][1], agreement[k][2], 100.0 * agreement[k][0] / sum(agreement[k]))
        
if report == "sys_scores":
   for s in sys_scores:
      for k in sys_scores[s]:
         print s, k, sys_scores[s][k][0], "/", sum(sys_scores[s][k]), "=", 100 * sys_scores[s][k][0] / float(sum(sys_scores[s][k]))

# ----

# for j in res['results']['judgments']:
#     print j['worker_id'],
       
        
# for x in res['results']['judgments']:
#     print_hier(x, "")
#    break

# print_hier(res, "")
        
#        res_utf8 = dict((key.encode("UTF-8"), value) for (key,value) in res.items())
#        data = res_utf8['data']
#        res_utf8['data'] = dict((key.encode("UTF-8"), value.encode("UTF-8")) for (key,value) in data.items())
#        questions.append(res_utf8)


# print questions[0].keys()
# print questions[0]['results']['r1']
# print questions[0]['data'].keys()
# print " ".join([str(q['agreement']) for q in questions])


#!/usr/bin/env python3

# fantasy name generator
# (c) 2017 kiilas@eluron.com

from itertools import chain
import getopt
import random
import sys

ruleset = {}

def clear_ruleset():
    ruleset.clear()

# returns a (random) transformation of a symbol
def transform_symbol(s):

    # a symbol with no derivation rules yields itself
    if s not in ruleset:
        return [s]

    # pick a random transformation, using weights
    total = 0
    for _, prob in ruleset[s]:
        total += prob
    rnd = random.random() * total
    for t, prob in ruleset[s]:
        rnd -= prob
        if rnd <= 0:
            return t

# returns a (random) transformation of a sentence
def transform_sentence(s):
    return list(chain.from_iterable(map(transform_symbol, s)))

# repeatedly transforms a sentence until resolution or maximum iterations
def repeat_transform(s, max_iter=256):
    i = 0
    while i < max_iter:
        i += 1
        s2 = transform_sentence(s)
        if s == s2:
            break
        s = s2
    return s2

# merges the rule into the current ruleset
def merge_rule(symb_pred, symbs_derived, derive_prob):
    if symb_pred not in ruleset:
        ruleset[symb_pred] = [(symbs_derived, derive_prob)]
        return
    ruleset[symb_pred].append((symbs_derived, derive_prob))

# parses a single definition line
# adds the content to current ruleset
# returns whether parse was successful
def parse_line(line):
    tokens = line.strip().split()
    
    # try parsing as an empty line
    if not tokens:
        return True

    # try parsing the line as a comment
    if tokens[0][0] == '#':
        return True

    # try parsing the line as a derivation rule
    if len(tokens) >= 3 and tokens[1] == '>':
        symb_pred = tokens[0]
        symbs_derived = [tokens[2]]
        derive_prob = 1
        i = 3
        okay = True
        # look for '+ <SYMB>' and '* <probability>' modifiers
        while okay and len(tokens) >= i+2:
            if tokens[i] == '+':
                symbs_derived.append(tokens[i+1])
            elif tokens[i] == '*':
                try:
                    derive_prob *= float(tokens[i+1])
                except:
                    okay = False
            elif tokens[i] == '#': # rest is comment
                i = len(tokens)
                break
            else:
                okay = False
            i += 2
        if i != len(tokens):
            okay = False
        if okay:
            merge_rule(symb_pred, symbs_derived, derive_prob)
            return True

    # all parsers failed
    print('ERROR: could not parse: ' + line.strip())
    return False
        

# loads the definition file
# adds the parsed contents to current ruleset
# use clear_ruleset() first for a fresh state
# returns whether load was successful
def load_def(filename):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
    except:
        print('ERROR: could not read file: ' + filename)
        return False
    for line in lines:
        if not parse_line(line):
            print('ERROR: could not parse file: ' + filename)
            return False
    return True

# returns a string from a sentence
def compile_sentence(s):
    res = ''
    uppercase = False
    geminate = False
    for symb in s:
        if symb == '[null]':
            continue
        if symb == '[space]':
            res += ' '
            continue
        if symb == '[uppercase]':
            uppercase = True
            continue
        if symb == '[geminate]':
            geminate = True
            continue
        to_add = symb
        if geminate:
            to_add = to_add[0] * 2 + to_add[1:]
            geminate = False
        if uppercase:
            to_add = to_add[0].upper() + to_add[1:]
            uppercase = False
        res += to_add
    return res
            
def generate_names(num=24):
    res = []
    for i in range(num):
        res.append(compile_sentence(repeat_transform(['NAME'])))
    return res

def help_msg():
    print('Fantasy name generator (c) 2017 kiilas@eluron.com')
    print('USAGE: namegen.py -m <modulename> [-c <count>]')

argv = sys.argv[1:]
module = None
count = 24
try:
    opts, args = getopt.getopt(argv, 'hm:c:', ['help'])
except getopt.GetoptError:
    help_msg()
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        help_msg()
        sys.exit()
    elif opt == '-m':
        module = arg
    elif opt == '-c':
        try:
            count = int(arg)
        except:
            help_msg()
            sys.exit(2)
if not module:
    help_msg()
    sys.exit(2)

if not load_def(module+'.def'):
    print('ERROR: could not load module: ' + module)
    sys.exit(1)

names = generate_names(count)
for name in names:
    print(name)

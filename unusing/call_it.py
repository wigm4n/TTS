#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from dictionary import build_map
from dictionary import find_stress
from dictionary import preprocess_input_text
from dictionary import wrapper_syllables

build_map(False)
all_args = ""
for i in range(len(sys.argv) - 1):
    all_args += sys.argv[i+1] + " "
input_text = all_args.strip()
words = preprocess_input_text(input_text)
res = find_stress(words)
res2 = wrapper_syllables(res)
if res == "":
    print("Not found")
else:
    print(res2)

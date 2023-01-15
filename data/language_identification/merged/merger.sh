#!/bin/bash

cat clean/train.txt noisy/1/train.txt > merged/train.txt
cat clean/test.txt noisy/1/test.txt > merged/test.txt

# add more data in dom_lang for data balance
cat dom_langs/persian.txt | shuf | head -n4800 >> merged/train.txt
cat dom_langs/arabic.txt | shuf | head -n4800 >> merged/train.txt
cat dom_langs/urdu.txt | shuf | head -n4800 >> merged/train.txt
cat dom_langs/urdu.txt | shuf | tail -n1200 >> merged/test.txt
cat dom_langs/persian.txt | shuf | tail -n1200 >> merged/test.txt
cat dom_langs/arabic.txt | shuf | tail -n1200 >> merged/test.txt 
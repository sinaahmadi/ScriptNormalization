# coding: utf-8
"""
Evaluation metrics
"""

import json
import jiwer
from sacrebleu.metrics import BLEU, CHRF
from typing import List
import subprocess

bleu = BLEU()
chrf = CHRF()

def sequence_accuracy(hypotheses: List[str], references: List[str]):
    assert len(hypotheses) == len(references)
    correct_sequences = sum(
        [1 for (hyp, ref) in zip(hypotheses, references) if hyp == ref])
    return (correct_sequences / len(hypotheses)) * 100 if hypotheses else 0.0

def calculate_error_rate_acc(references, candidates, error_type="wer"):
    # calculate word error rate (wer) accuracy and character error rate (cer)
    # the accuracy is 1 - WER
    if error_type == "wer":
        return 1 - jiwer.wer([" ".join(i[0]) for i in references], [" ".join(i) for i in candidates])
    else:
        return 1 - jiwer.cer([" ".join(i[0]) for i in references], [" ".join(i) for i in candidates])

def evaluate_baseline():
    with open("config.json", "r") as f:
        configs = json.load(f)
        
    for config in configs:
        # evaluate the baseline
        source, target = list(), list()
        print("baseline for ", config["source_language"], " ==== ", config["target_language"])
        for n in [20, 40, 60, 80, 100, "1"]:
            with open("../" + config["datasets"] + "/%s/%s.src"%(n, "test"), "r") as f:
                source = f.read().splitlines()
            with open("../" + config["datasets"] + "/%s/%s.trg"%(n, "test"), "r") as f:
                target = f.read().splitlines()

            target_corpus = [[i] for i in target]
            print(n, "\t", bleu.corpus_score(source, target),
                 "\t", chrf.corpus_score(source, target_corpus), 
                 "\t", sequence_accuracy(source, target)) # using target_corpus gave the same results as target

def evaluate_mt():
    with open("config.json", "r") as f:
        configs = json.load(f)
    
    for config in configs:
        if config["source_language"] not in ["Kashmiri", "Sorani", "Sindhi"]:
            continue

        print(config["source_language"], " ==== ", config["target_language"])

        tgt_tested_flag = False
        for n in [20, 40, 60, 80, 100]:
            for t in ["trg", "src", "normalized.src"]:
                if t == "trg" and tgt_tested_flag:
                    continue
                else:
                    tgt_tested_flag = True
                with open("../" + config["FLORES_dataset"] + "/devtest_%s.translated.%s"%(n, t), "r") as f:
                    source = f.read().splitlines()

                with open("../data/machine_translation/FLORES200/eng_Latn.devtest", "r") as f: 
                    target = f.read().splitlines()

                target_corpus = [[i] for i in target]
                print(n, "\t", t, "\t", bleu.corpus_score(source, target_corpus),
                     "\t", chrf.corpus_score(source, target_corpus), 
                     "\t", calculate_error_rate_acc([[i] for i in source], target_corpus, "cer"))

def evaluate_baseline_sh():
    with open("config.json", "r") as f:
        configs = json.load(f)
    
    command_bleu_temp = "sacrebleu ../DDD/NNN/test.trg -i ../DDD/NNN/test.src -m bleu -w 4"
    command_chrf_temp = "sacrebleu ../DDD/NNN/test.trg -i ../DDD/NNN/test.src -m chrf -w 4"
    for config in configs:
        # evaluate the baseline
        source, target = list(), list()
        print("baseline for ", config["source_language"], " ==== ", config["target_language"])
        for n in [20, 40, 60, 80, 100, 1]:
            results = [str(n)]
            command_bleu = command_bleu_temp.replace("DDD", config["datasets"]).replace("NNN", str(n))
            command_chrf = command_chrf_temp.replace("DDD", config["datasets"]).replace("NNN", str(n))
            # print(command)
            output_bleu = subprocess.getoutput(command_bleu)
            output_chrf = subprocess.getoutput(command_chrf)
            # BLEU score
            results.append(output_bleu.splitlines()[6].replace(" \"score\": ", "").replace(",", ""))
            # chrF
            results.append(output_chrf.splitlines()[2].replace(" \"score\": ", "").replace(",", ""))

            print("\t".join(results))
            # print(output)
            # output = json.loads(output).replace("'", "\"")
            # print(type(output))
        #     break
        # break

def evaluate_baseline_mt_sh():
    with open("config.json", "r") as f:
        configs = json.load(f)
    
    for config in configs:
        if config["source_language"] not in ["Kashmiri", "Sorani", "Sindhi"]:
            continue

        print(config["source_language"], " ==== ", config["target_language"])

        command_bleu_temp = "sacrebleu ../data/machine_translation/FLORES200/eng_Latn.devtest -i ../DDD/devtest_NNN.translated.TTT -m bleu -w 4"
        command_chrf_temp = "sacrebleu ../data/machine_translation/FLORES200/eng_Latn.devtest -i ../DDD/devtest_NNN.translated.TTT -m chrf -w 4"
        tgt_tested_flag = False
        for n in [20, 40, 60, 80, 100]:
            for t in ["trg", "src", "normalized.src"]:
                if t == "trg" and tgt_tested_flag:
                    continue
                else:
                    tgt_tested_flag = True

                results = [str(n), t]
                command_bleu = command_bleu_temp.replace("DDD", config["FLORES_dataset"]).replace("NNN", str(n)).replace("TTT", t)
                command_chrf = command_chrf_temp.replace("DDD", config["FLORES_dataset"]).replace("NNN", str(n)).replace("TTT", t)
                # print(command_bleu)
                output_bleu = subprocess.getoutput(command_bleu)
                output_chrf = subprocess.getoutput(command_chrf)
                # BLEU score
                results.append(output_bleu.splitlines()[2].replace(" \"score\": ", "").replace(",", ""))
                # chrF
                results.append(output_chrf.splitlines()[2].replace(" \"score\": ", "").replace(",", ""))

                print("\t".join(results))


if __name__ == '__main__':
    # evaluate_mt()
    # evaluate_baseline()
    # evaluate_baseline_sh()
    evaluate_baseline_mt_sh()





# sacrebleu ../data/datasets/Gorani-Sorani/20/test.trg -i ../data/datasets/Gorani-Sorani/20/test.src -m bleu -w 4  
# sacrebleu ../data/datasets/Gorani-Sorani/40/test.trg -i ../data/datasets/Gorani-Sorani/40/test.src -m bleu -w 4  
# sacrebleu ../data/datasets/Gorani-Sorani/60/test.trg -i ../data/datasets/Gorani-Sorani/60/test.src -m bleu -w 4  
# sacrebleu ../data/datasets/Gorani-Sorani/80/test.trg -i ../data/datasets/Gorani-Sorani/80/test.src -m bleu -w 4  
# sacrebleu ../data/datasets/Gorani-Sorani/100/test.trg -i ../data/datasets/Gorani-Sorani/100/test.src -m bleu -w 4  





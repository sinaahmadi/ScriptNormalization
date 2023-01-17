import json
import random
import re
import synthesize
from klpt.preprocess import Preprocess

'''
    Created in January 2022
    This script generates synthetic data based on the FLORES200 dataset.

    - Sina Ahmadi (last updated January 2022)
'''

def clean_text(text, has_zwnj=False, has_diacritics=False):
    if not has_zwnj:
        text = text.replace("‌", "")
    if not has_diacritics:
        for i in [ "ً", "ِ", "ٌ", "ُ", "ّ", "ٍ", "ْ", "ء"]:
            text = text.replace(i, "")
    return text.replace("‏", " ").replace("‎", " ").replace("ـ", "")

if __name__ == '__main__':
    with open("config.json", "r") as f:
        configs = json.load(f)

    with open("../data/scripts/info.json", "r") as f:
        info = json.load(f)

    for config in configs:
        print(config["source_language"])
        if config["source_language"] not in ["Sorani", "Kashmiri", "Sindhi"]:
            continue

        print(config["source_language"], " ==== ", config["target_language"])

        with open("../" + config["script_map"], "r") as f:
            script_map = f.read().splitlines()[1:]
        
        # convert the tsv format of the script mapping to a dictionary
        script_map = synthesize.tsv_to_dict(script_map)
        # print(generate("ئەمە بۆ تست کردنە.", script_map))

        # extract sentences from the corpus
        with open("../" + config["FLORES"], "r") as f:
            corpus = f.read()

        # clean the FLORES data (for numerals only)
        preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
        corpus_sent = preprocessor_ckb.unify_numerals(corpus).splitlines()
        
        print("Size of the corpus initially: ", len(corpus.splitlines()))
        print("Size of the corpus after cleaning: ", len(corpus_sent))

        print("# Generating data...")

        # generate synthetic data, clean the target text and save the dataset
        preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
        for n in [20, 40, 60, 80, 100]:
            print('Generate synthetic data with noise % of ', str(n))
            synth_dataset = list()
            for i in corpus_sent:
                # tuples likes (noisy sent--source, clean sent--target)
                synth_i = synthesize.generate(i, script_map, noise_percentage=n)

                if synth_i != None:
                    # clean the target
                    clean_i = clean_text(i, has_zwnj=info[config["source_language"]]["zwnj"], has_diacritics=info[config["source_language"]]["diacritics"])
                    if config["source_language"] == "Sorani":
                        clean_i = preprocessor_ckb.preprocess(clean_i)
                    elif config["source_language"] == "Kurmanji":
                        clean_i = preprocessor_kmr.preprocess(clean_i)

                    synth_dataset.append((synth_i, clean_i))

            with open("../" + config["FLORES_dataset"] + "/%s_%s.src"%("devtest", n), "w") as f:
                f.write("\n".join([m[0] for m in synth_dataset]))
            with open("../" + config["FLORES_dataset"] + "/%s_%s.trg"%("devtest", n), "w") as f:
                f.write("\n".join([m[1] for m in synth_dataset]))

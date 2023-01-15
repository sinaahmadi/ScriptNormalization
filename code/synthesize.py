import json
import random
import re
import regex
from klpt.preprocess import Preprocess

'''
    Created in October 2022
    This script generates synthetic data based on a character alignment matrix and using a corpus.
    Make sure the config.json file points to the correct files before running.

    - Sina Ahmadi (last updated December 2022)
'''

def tsv_to_dict(text):
    # convert the script map to a dctionary
    text_dict = dict()
    for i in text:
        i_s = i.split("\t")[0] # source letter
        if i_s not in text_dict:
            text_dict[i_s] = list()
        for j in range(1, len(i.split("\t"))):
            if i.split("\t")[j] != "":
                i_t = i.split("\t")[j] # target letter
                if i_t == "NULL":
                    i_t = ""

                if i_t not in text_dict[i_s]:
                    text_dict[i_s].append(i_t) # a big value to make it more impactful

    return text_dict

def preprocess_corpus(text):
    # clean a corpus and return a dataset
    # unify numerals to latin
    preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
    text = preprocessor_ckb.unify_numerals(text)
    # clean corpus by removing acronyms (x.x or x.x.x)
    clean_text = re.sub(r".\..\..\..", "", text)
    clean_text = re.sub(r".\..\..", "", clean_text)
    clean_text = clean_text.replace("  ", " ").replace("؟ ", "\n").replace("! ", "\n").replace(": ", "\n").replace("* ", " ").replace("۔", "\n").replace(". ", "\n")
    # remove dates
    clean_text = clean_text.replace(" / ", "/").replace(" . ", ".").replace("...", ".")
    clean_text = re.sub(r"([1-9]|0[1-9]|[12][0-9]|3[01])[- /.]([1-9]|0[1-9]|1[012])[- /.]\d\d\d\d", "", clean_text)
    # remove links
    clean_text = re.sub(r'https?:\/\/.*[\r\n]*', '', clean_text, flags=re.MULTILINE)

    return clean_text

def generate(text, character_map, noise_percentage=100):
    keys = list(character_map.keys())
    random.Random(10).shuffle(keys)
    character_map = {key: character_map[key] for key in keys}

    # Determine the number of characters that should be turned noisy, i.e. mapped with noisy equivalents, to meet the synthesis level
    text_set = set(text)
    num_replacements = round(len(text_set) * noise_percentage / 100)
    added_noise = 0
    for i in text_set:
        if not added_noise <= num_replacements:
            break
            
        if i in character_map:
            # note: this can be modified in such a way that the length of the letters be taken into account: first longer replacements, then shorter ones.
            text = text.replace(i, random.choice(character_map[i]))
            added_noise += 1
        
    if added_noise == 0:
        return None
            
    return text.replace("▁", "")

def save_datasets(dataset, noisiness, save_path):
    # save as train, dev and test
    split_name_ratio = {"train": (0, int(len(dataset) * 80 / 100)),
                        "dev": (int(len(dataset) * 80 / 100), int(len(dataset) * 90 / 100)),
                        "test": (int(len(dataset) * 90 / 100), len(dataset))}

    for d in split_name_ratio:
        with open(save_path + "/%s/%s.src"%(noisiness, d), "w") as f:
            f.write("\n".join([m[0] for m in dataset[split_name_ratio[d][0]: split_name_ratio[d][1]]]))
        with open(save_path + "/%s/%s.trg"%(noisiness, d), "w") as f:
            f.write("\n".join([m[1] for m in dataset[split_name_ratio[d][0]: split_name_ratio[d][1]]]))
    print("Saved!")

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
        print(config["source_language"], " ==== ", config["target_language"])

        with open("../" + config["script_map"], "r") as f:
            script_map = f.read().splitlines()[1:]
        
        # convert the tsv format of the script mapping to a dictionary
        script_map = tsv_to_dict(script_map)
        # print(generate("ئەمە بۆ تست کردنە.", script_map))

        # extract sentences from the corpus
        with open("../" + config["corpus"], "r") as f:
            corpus = f.read()

        # extract senteces from the corpus and clean it
        corpus = preprocess_corpus(corpus).splitlines()
        # split sentences > to 20 to smaller ones
        for i in corpus:
            if len(i.split()) > 20:
                i.split()

        # create data instances having a length of less than 20 tokens (space-delimited)
        corpus_sent = list()
        for i in corpus:
            # clean i to remove non-Perso-Arabic text
            latin = regex.sub(r'[^\p{Latin}]', ' ', i).split() # find words in the Latin script
            hindi = re.findall(r'[\u0900-\u097f\ua8e0-\ua8ff]+', i) # find words in Devanagari
            for l in latin + hindi:
                i = i.replace(l, " ")
            # add space before and after punctuation marks
            for c in ".؟،!؛:ː۔":
                i = i.replace(c, " " + c + " ")
            i = " ".join(i.split())
            for c in "-ـ<>«»(){}[]/+٪'\"$&ː… ͡":
                i = i.replace(c, " ")
            i = " ".join(i.split())
            
            if len(i.split()) >= 3 and len(i.split()) < 20 and len(i) >= 10:
                if "http" not in i and "www" not in i and "@" not in i:
                    corpus_sent.append(i.strip())
            elif len(i.split()) > 20 and len(i) >= 10:
                for j in range(0, len(i.split()), 10):
                    if j+10 < len(i):
                        i_j = i[j:j+10]
                    else:
                        i_j = i[j:]

                    if len(i_j.split()) > 5 and len(i_j) >=10:
                        if "http" not in i_j and "www" not in i_j and "@" not in i_j:
                            corpus_sent.append(i_j.strip())

        print("Size of the corpus initially: ", len(corpus))
        print("Size of the corpus after cleaning: ", len(corpus_sent))

        print("# Generating data...")
        # generate synthetic data, clean the target text and save the dataset
        preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
        preprocessor_kmr = Preprocess("Sorani", "Arabic", numeral="Latin")
        for n in [20, 40, 60, 80, 100]:
            print('Generate synthetic data with noise % of ', str(n))
            synth_dataset = list()
            for i in corpus_sent:
                # tuples likes (noisy sent--source, clean sent--target)
                synth_i = generate(i, script_map, noise_percentage=n)

                if synth_i != None:
                    # clean the target
                    clean_i = clean_text(i, has_zwnj=info[config["source_language"]]["zwnj"], has_diacritics=info[config["source_language"]]["diacritics"])
                    if config["source_language"] == "Sorani":
                        clean_i = preprocessor_ckb.preprocess(clean_i)
                    elif config["source_language"] == "Kurmanji":
                        clean_i = preprocessor_kmr.preprocess(clean_i)

                    synth_dataset.append((synth_i, clean_i))

            save_datasets(list(set(synth_dataset)), str(n), "../" + config["datasets"])

        print("# Generating merged data...")
        # merge all the datasets with various noise % and save in the "all" folder
        merged_data_src, merged_data_tgt = list(), list()
        for m in ["train", "dev", "test"]:
            for n in [20, 40, 60, 80, 100]:
                with open("../" + config["datasets"] + "/%s/%s.src"%(n, m), "r") as f:
                    merged_data_src.append(f.read())
                with open("../" + config["datasets"] + "/%s/%s.trg"%(n, m), "r") as f:
                    merged_data_tgt.append(f.read())

        merged_data_src = "\n".join(merged_data_src).splitlines()
        merged_data_tgt = "\n".join(merged_data_tgt).splitlines()
        merged_data = list(set([(merged_data_src[i], merged_data_tgt[i]) for i in range(len(merged_data_src))]))
        print("Total number of merged data instances: ", len(merged_data), len(merged_data))
        save_datasets(merged_data, "1", "../" + config["datasets"])
        
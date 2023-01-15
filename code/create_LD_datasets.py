import json
import random
import copy

with open("config.json", "r") as f:
    configs = json.load(f)

# iso639-3 to iso639-2
fasttext_code_mapper = {
	"arb": "ar",
	"urd": "ud",
	"fas": "fa",
	"snd": "sd",
	"ckb": "ckb",
	"mzn": "mzn",
	"kmr": "kmr",
	"glk": "glk",
	"kas": "kas",
	"hac": "hac",
	"azb": "azb"
}

def create_clean():
	# Create clean datasets
	# for the clean data, the level of noise is not of importance (cause there is none!)
	checked_langs, data = list(), list()
	train, test = list(), list()

	for config in configs:
		if config["source_language"] in checked_langs:
			continue
		else:
			checked_langs.append(config["source_language"])

		print(config["source_language"])
		for m in ["train", "dev", "test"]:
			with open("../" + config["datasets"] + "/%s/%s.trg"%("1", m), "r") as f:
				data += list(set(f.read().splitlines())) # shuffle the list

		random.Random(10).shuffle(data)
		for i in range(6000): # downsample to 6000
			row = "__label__" + fasttext_code_mapper[config["source_language_code"]] + "\t" + data[i]
			if i < 4800:
				train.append(row)
			else:
				test.append(row)

	# add data in Persian, Arabic and Urdu
	for i in ["../data/language_identification/dom_langs/urdu.txt", "../data/language_identification/dom_langs/persian.txt", "../data/language_identification/dom_langs/arabic.txt"]:
		with open(i, "r") as f:
			dom_file = list(set(f.read().splitlines()))
		for i in range(6000): # downsample to 6000
			if i < 4800:
				train.append(dom_file[i])
			else:
				test.append(dom_file[i])

	random.Random(10).shuffle(train)
	random.Random(10).shuffle(test)

	saving_files = {"train": train, "test": test}
	for s in saving_files:
		with open("../data/language_identification/clean/%s.txt"%s, "w") as f:
			f.write("\n".join(saving_files[s]))

def create_noisy():
	noisy_data = {
		"20": {"kas": list(), "snd": list(), "ckb": list(), "kmr": list(), "hac": list(), "azb": list(), "glk": list(), "mzn": list()},
		"40": {"kas": list(), "snd": list(), "ckb": list(), "kmr": list(), "hac": list(), "azb": list(), "glk": list(), "mzn": list()},
		"60": {"kas": list(), "snd": list(), "ckb": list(), "kmr": list(), "hac": list(), "azb": list(), "glk": list(), "mzn": list()},
		"80": {"kas": list(), "snd": list(), "ckb": list(), "kmr": list(), "hac": list(), "azb": list(), "glk": list(), "mzn": list()},
		"100": {"kas": list(), "snd": list(), "ckb": list(), "kmr": list(), "hac": list(), "azb": list(), "glk": list(), "mzn": list()},
		"1": {"kas": list(), "snd": list(), "ckb": list(), "kmr": list(), "hac": list(), "azb": list(), "glk": list(), "mzn": list()}
		}

	for n in noisy_data:
		print(n)
		for config in configs:
			src_file = list()
			for m in ["train", "dev", "test"]:
				if m == "train" and config["source_language_code"] == "ckb" :
					continue
				with open("../" + config["datasets"] + "/%s/%s.src"%(n, m), "r") as f:
					noisy_data[n][config["source_language_code"]] += list(set(f.read().splitlines())) # merge train, dev, validation - then shuffle the list

	for n in noisy_data:
		train, test = list(), list()
		for l in noisy_data[n]:
			print(n, l)
			n_l = list(set(noisy_data[n][l]))
			random.Random(10).shuffle(n_l)
			print(len(n_l))
			if l == "kas":
				counter_train, counter_test = 4700, 3760
			else:
				counter_train, counter_test = 6000, 4800

			for i in range(counter_train):
				row = "__label__" + fasttext_code_mapper[l] + "\t" + n_l[i]
				if i < counter_test:
					train.append(row)
				else:
					test.append(row)

		random.Random(10).shuffle(train)
		random.Random(10).shuffle(test)

		saving_files = {"train": train, "test": test}
		for s in saving_files:
			with open("../data/language_identification/noisy/%s/%s.txt"%(n, s), "w") as f:
				f.write("\n".join(saving_files[s]))


# create_clean()
# create_noisy()



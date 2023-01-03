from Levenshtein import distance
import pyarabic.araby as araby

'''
This script retrieves words that are written identically or somehow similar in two languages. 
The language pairs are as follows:

	Kashmiri / Urdu
	Azeri / Persian
	Gorani / Persian
	Sorani / Arabic
	Sorani / Persian
	Gilaki / Persian
	Mazanderani / Persian
	Kurmanji / Arabic
	Kurmanji / Persian
	Gorani / Persian
	Gorani / Arabic

Two word lists are required: one in the source language, the other one in the target language. 
'''
word_list_dirs = {
	"Sorani": "ckb_corpus_wordlist.txt"
}

target_wordlist_dirs = {
	"Arabic": "data/Arabic_wordlist.txt"
}

source_lang = "Sorani"
target_lang = "Arabic"

with open(word_list_dirs[source_lang], "r") as f:
	source_wordlist = f.read().splitlines()

with open(target_wordlist_dirs[target_lang], "r") as f:
	target_wordlist = f.read().splitlines()

wordlist_common = list()
counter = 0

for j in source_wordlist:
	# print(j)
	if j in target_wordlist:
		wordlist_common.append(j + "\t" + j)
		counter += 1
	else:
		for k in target_wordlist:
			# for Kurmanji, Sorani and Gorani only / the target should be Persian or Arabic
			if source_lang == "Sorani" or source_lang == "Kurmanji" or source_lang == "Gorani":
				j_rep = j.replace("ە", "").replace("ێ", "").replace("وو", "و").replace("ڤ", "و").replace("ڵ", "ل").replace("ڕ", "ر").replace("ۆ", "و").replace("ئ", "").replace("ۊ", "و")
				k_rep = k.replace("ك", "ک").replace("ي", "ی").replace("ث", "س").replace("ص", "س").replace("ذ", "ز").replace("ظ", "ز").replace("ط", "ت").replace("ض", "ز").replace("آ", "ا")
			elif source_lang == "Gorani":
				j_rep = j.replace("ە", "").replace("ێ", "").replace("وو", "و").replace("ڤ", "و").replace("ڵ", "ل").replace("ڕ", "ر").replace("ۆ", "و").replace("ئ", "").replace("ۊ", "و")
			else:
				j_rep, k_rep = j, k

			if j_rep == araby.strip_diacritics(k_rep) or j_rep == k_rep or j_rep == araby.strip_diacritics(k_rep):# or distance(j, k) < 1 or distance(araby.strip_diacritics(j), araby.strip_diacritics(k)) < 1:
				wordlist_common.append(j + "\t" + k)
				counter += 1
				break

	print(counter)

print(len(wordlist_common))
print(counter)
with open("data/%s_%s_dict_common.txt"%(source_lang, target_lang), "w") as f:
	f.write("\n".join(wordlist_common))




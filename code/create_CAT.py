import Needleman_Wunsch as nw
import json 

with open("config.json", "r") as f:
    configs = json.load(f)

NeedlemanWunsch = nw.Needleman_Wunsch()

for config in configs:
	print(config["source_language"], " ==== ", config["target_language"])

	# create the character alignment matrix (CAT) using the common words
	with open("../" + config["common_words"], "r") as f:
	    common = f.read().split("\n")
	with open("../" + config["script_map"], "r") as f:
		script_map = f.read().splitlines()[1:]

	source = [i.split("\t")[0] for i in common]
	target = [i.split("\t")[1] for i in common]

	matrix = NeedlemanWunsch.create_character_matrix(source, target)

	# normalize the matrix
	for i in matrix:
	    factor = 1 / sum(matrix[i].values())
	    
	    for j in matrix[i]:
	        matrix[i][j] = round(matrix[i][j] * factor, 4)

	# update CAT using the script mappings
	for i in script_map:
		i_s = i.split("\t")[0] # source letter
		if i_s not in matrix:
			matrix[i_s] = dict()
		for j in range(1, len(i.split("\t"))):
			if i.split("\t")[j] != "":
				i_t = i.split("\t")[j] # target letter
				if i.split("\t")[j] == "NULL":
					i_t = ""
				if i_t in matrix[i_s]:
					matrix[i_s][i_t] += 1 # a big value to make it more impactful
				else:
					matrix[i_s][i_t] = 1

	# only consider alignments with probability > 0.1
	new_matrix = {i: {} for i in matrix}
	for i in matrix:
		for j in matrix[i]:
			if matrix[i][j] >= 0.1:
				new_matrix[i].update({j: matrix[i][j]})

	with open('../data/CAT/%s_%s_character_alginment_matrix.json'%(config["source_language"], config["target_language"]), 'w', encoding='utf-8') as f:    
	    json.dump(new_matrix, f, indent=4, ensure_ascii=False)

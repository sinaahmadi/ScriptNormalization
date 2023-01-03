import json
import synthesize

def calculate_ratio(script_map):
	target_characters = list(set("\n".join(["\n".join(i) for i in script_map.values()]).splitlines()))

	# calculate common characters between the two
	intersection = set(list(script_map.keys())).intersection(target_characters)
	# calculate all the characters of the two
	union = set(list(script_map.keys()) + target_characters)
	# calculate characters that are identical in both scripts (no other alternative found for them)
	intersection_equivalent = 0
	for i in script_map:
		if i in script_map[i] and len(script_map[i]) == 1:
			intersection_equivalent += 1

	ratio = (len(intersection) /  len(union)) * (intersection_equivalent /  len(intersection))
	return ratio

def report_dataset(dir_path):
	row_counter = list()

	for i in ["20", "40", "60", "80", "100", "1"]:
		l_counter, w_counter = 0, 0
		for j in ["train", "test", "dev"]:
			with open("/".join([dir_path, i, j + ".trg"])) as f:
				text = f.read()
			
			l_counter += len(text.splitlines())
			w_counter += len(text.split())
		
		row_counter.append(str(l_counter))
		row_counter.append(str(w_counter))

	return "\t".join(row_counter)


if __name__ == '__main__':
	with open("config.json", "r") as f:
		configs = json.load(f)

	for config in configs:
		# # convert the tsv format of the script mapping to a dictionary
		# with open("../" + config["script_map"], "r") as f:
			# script_map = f.read().splitlines()[1:]
			# script_map = synthesize.tsv_to_dict(script_map)
			# print(config["source_language_code"], "\t", config["target_language_code"], "\t", round(calculate_ratio(script_map), 3))

		print(config["source_language_code"] + "-" + config["target_language_code"], "\t", report_dataset("../" + config["datasets"]))





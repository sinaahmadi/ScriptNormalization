def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

def splitter():
	for f_name in ["Sorani-Arabic", "Sorani-Persian", "Kashmiri-Urdu", "Sindhi-Urdu"]:
		for n in [20, 40, 60, 80, 100]:
			new_split, split_indices = list(), list()
			with open(f_name + "/devtest_%s.src"%n, "r") as f:
				source = f.read().splitlines()

			counter = 0
			for i in range(len(source)):
				i_split = wrap(source[i], 100)
				new_split.append("\n".join(i_split))

				split_indices.append(str(counter) + "-" + str(counter + len(i_split)))
				counter += len(i_split)

			with open(f_name + "/split/devtest_%s.split.src"%n, "w") as f:
				f.write("\n".join(new_split))
			with open(f_name + "/split/indices_%s.split.src"%n, "w") as f:
				f.write("\n".join(split_indices))

def merger():
	for f_name in ["Sorani-Arabic", "Sorani-Persian", "Kashmiri-Urdu", "Sindhi-Urdu"]:
		for n in [20, 40, 60, 80, 100]:
			merged_data = list()
			with open(f_name + "/split/devtest_%s.split.hyp"%n, "r") as f:
				source = f.read().replace("<unk>", "").splitlines()
			with open(f_name + "/split/indices_%s.split.src"%n, "r") as f:
				indices = f.read().splitlines()

			# remove <unk>
			for i in indices:
				merged_data.append(" ".join(source[int(i.split("-")[0]): int(i.split("-")[1])]))

			with open(f_name + "/devtest_%s.normalized.src"%n, "w") as f:
				f.write("\n".join(merged_data))



if __name__ == '__main__':
	merger()
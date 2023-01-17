import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})

with open("prediction_reference_heatmap.tsv", "r") as f:
	file = f.read().splitlines()[1:]

code_to_lang = {'glk': "Gilaki", 'hac': "Gorani", 'fa': "Persian", 'ar': "Arabic", 'ur': "Urdu", 'ckb': "Sorani", 'kmr': "Kurmanji", 'kas': "Kashmiri", 'mzn': "Mazanderani", 'azb': "Azeri", 'sd': "Sindhi"}

pairs_dict = dict()
for i in file:
	i_1, i_2 = code_to_lang[i.split("\t")[0].replace("__label__", "").strip()], code_to_lang[i.split("\t")[1].replace("__label__", "").strip()]
	if i_1 not in pairs_dict:
		pairs_dict.update({i_1: {i_2: 1}})
	else:
		if i_2 not in pairs_dict[i_1]:
			pairs_dict[i_1].update({i_2: 1})
		else:
			pairs_dict[i_1][i_2] += 1

for i in pairs_dict:
	print(i, pairs_dict[i])
x_axis, y_axis = sorted(pairs_dict.keys()), sorted(pairs_dict.keys())

values = list()
print(x_axis)
for i in x_axis:
	row = list()
	for j in y_axis:
		if j not in pairs_dict[i]:
			row.append(0)
		else:
			row.append(pairs_dict[i][j])
	values.append(row)

print(values)
harvest = np.array(values)

fig, ax = plt.subplots()
im = ax.imshow(harvest, cmap=cm.rainbow)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(y_axis)), labels=y_axis)
ax.set_yticks(np.arange(len(x_axis)), labels=x_axis)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
# Loop over data dimensions and create text annotations.
for i in range(len(x_axis)):
    for j in range(len(y_axis)):
        text = ax.text(j, i, harvest[i, j], ha="center", va="center", color="w")

# ax.set_title("Harvest of local y_axis (in tons/year)")
fig.tight_layout()
fig.savefig("heatmap_merged.pdf")
plt.show()


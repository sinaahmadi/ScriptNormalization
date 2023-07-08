import numpy as np
import sys
from sklearn.metrics import precision_recall_fscore_support

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# python3 macro-f.py noisy/20 0 (0 for first prediction, 1 for second and so on)

print("LID.176")
with open("%s/predict_lid.176.txt"%sys.argv[1], "r") as f:
	y_pred = [i.split()[int(sys.argv[2])] for i in f.read().splitlines()]

with open("%s/test.txt"%sys.argv[1], "r") as f:
	y_true = [i.split("\t")[0] for i in f.read().splitlines()]

y_pred = np.array(y_pred)
y_true = np.array(y_true)

print(precision_recall_fscore_support(y_true, y_pred, average='macro'))


print("OUR MODEL")
with open("%s/model_predict.txt"%sys.argv[1], "r") as f:
	y_pred = [i.split()[int(sys.argv[2])] for i in f.read().splitlines()]

y_pred = np.array(y_pred)

print(precision_recall_fscore_support(y_true, y_pred, average='macro'))


# "predict_lid.176_scr.txt",
# "predict_lid.176_sdh_unconventional.txt",
# "predict_lid.176.txt",

# "predict_scr_sdh_unconventional.txt",
# "predict_scr.txt",
# "predict_sdh_unconventional.txt",
# "predict.txt",
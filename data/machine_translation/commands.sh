python3 -m joeynmt translate training/configs/Kashmiri-Urdu_1.yaml < machine_translation/Sorani-Arabic/split/devtest_20.split.src > machine_translation/Sorani-Arabic/split/devtest_20.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Arabic_1.yaml < machine_translation/Sorani-Arabic/split/devtest_40.split.src > machine_translation/Sorani-Arabic/split/devtest_40.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Arabic_1.yaml < machine_translation/Sorani-Arabic/split/devtest_60.split.src > machine_translation/Sorani-Arabic/split/devtest_60.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Arabic_1.yaml < machine_translation/Sorani-Arabic/split/devtest_80.split.src > machine_translation/Sorani-Arabic/split/devtest_80.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Arabic_1.yaml < machine_translation/Sorani-Arabic/split/devtest_100.split.src > machine_translation/Sorani-Arabic/split/devtest_100.split.hyp


python3 -m joeynmt translate training/configs/Sorani-Persian_1.yaml < machine_translation/Sorani-Persian/split/devtest_20.split.src > machine_translation/Sorani-Persian/split/devtest_20.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Persian_1.yaml < machine_translation/Sorani-Persian/split/devtest_40.split.src > machine_translation/Sorani-Persian/split/devtest_40.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Persian_1.yaml < machine_translation/Sorani-Persian/split/devtest_60.split.src > machine_translation/Sorani-Persian/split/devtest_60.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Persian_1.yaml < machine_translation/Sorani-Persian/split/devtest_80.split.src > machine_translation/Sorani-Persian/split/devtest_80.split.hyp
python3 -m joeynmt translate training/configs/Sorani-Persian_1.yaml < machine_translation/Sorani-Persian/split/devtest_100.split.src > machine_translation/Sorani-Persian/split/devtest_100.split.hyp

python3 -m joeynmt translate training_2/configs_2/Sindhi-Urdu_1.yaml < machine_translation/Sindhi-Urdu/split/devtest_20.split.src > machine_translation/Sindhi-Urdu/split/devtest_20.split.hyp
python3 -m joeynmt translate training_2/configs_2/Sindhi-Urdu_1.yaml < machine_translation/Sindhi-Urdu/split/devtest_40.split.src > machine_translation/Sindhi-Urdu/split/devtest_40.split.hyp
python3 -m joeynmt translate training_2/configs_2/Sindhi-Urdu_1.yaml < machine_translation/Sindhi-Urdu/split/devtest_60.split.src > machine_translation/Sindhi-Urdu/split/devtest_60.split.hyp
python3 -m joeynmt translate training_2/configs_2/Sindhi-Urdu_1.yaml < machine_translation/Sindhi-Urdu/split/devtest_80.split.src > machine_translation/Sindhi-Urdu/split/devtest_80.split.hyp
python3 -m joeynmt translate training_2/configs_2/Sindhi-Urdu_1.yaml < machine_translation/Sindhi-Urdu/split/devtest_100.split.src > machine_translation/Sindhi-Urdu/split/devtest_100.split.hyp


python3 -m joeynmt translate training_2/configs_2/Kashmiri-Urdu_1.yaml < machine_translation/Kashmiri-Urdu/split/devtest_20.split.src > machine_translation/Kashmiri-Urdu/split/devtest_20.split.hyp
python3 -m joeynmt translate training_2/configs_2/Kashmiri-Urdu_1.yaml < machine_translation/Kashmiri-Urdu/split/devtest_40.split.src > machine_translation/Kashmiri-Urdu/split/devtest_40.split.hyp
python3 -m joeynmt translate training_2/configs_2/Kashmiri-Urdu_1.yaml < machine_translation/Kashmiri-Urdu/split/devtest_60.split.src > machine_translation/Kashmiri-Urdu/split/devtest_60.split.hyp
python3 -m joeynmt translate training_2/configs_2/Kashmiri-Urdu_1.yaml < machine_translation/Kashmiri-Urdu/split/devtest_80.split.src > machine_translation/Kashmiri-Urdu/split/devtest_80.split.hyp
python3 -m joeynmt translate training_2/configs_2/Kashmiri-Urdu_1.yaml < machine_translation/Kashmiri-Urdu/split/devtest_100.split.src > machine_translation/Kashmiri-Urdu/split/devtest_100.split.hyp




# procedure explained:
# given the big length of sentences in the FLORES dataset (up to 350), I make sentences shorter to a lenght of 100 and then use the trained models to normalize them.
# when sentences are split into smaller ones, I keep track of the number of lines as indices. Using these, I then merge the normalized data to be paralle to the ortiginal test set. Smart! :-) 
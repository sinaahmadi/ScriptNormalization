import json

with open("config_template.yaml", "r") as f:
    template = f.read()

with open("slurm_template.sh", "r") as f:
    slurm_temp = f.read()

with open("config.json", "r") as f:
    configs = json.load(f)

for config in configs:
    l = config["source_language"] + "-" + config["target_language"]
    for n in ["20", "40", "60", "80", "100", "1"]:
        with open("../training/configs/%s_%s.yaml"%(l, n), "w") as f:
            f.write(template.replace("LANG", l).replace("NOISE", n))
    with open("../training/SLURMs/%s.slurm"%l, "w") as f:
        f.write(slurm_temp.replace("LANG", l))

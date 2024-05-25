import subprocess
import os

# # Create directories
# os.makedirs("project/resources/cartography_plots", exist_ok=True)
# os.makedirs("project/resources/embeddings", exist_ok=True)
# os.makedirs("project/resources/indices", exist_ok=True)
# os.makedirs("project/resources/mapping", exist_ok=True)
# os.makedirs("project/resources/logs/agnews", exist_ok=True)
# os.makedirs("project/resources/logs/trec", exist_ok=True)
# os.makedirs("project/results/agnews", exist_ok=True)
# os.makedirs("project/results/trec", exist_ok=True)
# os.makedirs("project/plots/agnews", exist_ok=True)
# os.makedirs("project/plots/trec", exist_ok=True)

# Specify the directory to save the logs
exp_path = "project/resources/logs/agnews"

seeds = [398048, 127003, 259479, 869323, 570852]
# seeds = [333333]
# functions = ["random" ,"entropy" ,"leastconfidence" ,"bald" ,"discriminative" ,"cartography"]
functions = ["aleatoric","epi-add-alea"]
# modes = ['bi-cls',"regression",'ratio']
# modes = ['epi-alea','epi-add-alea','x-largest-alea']
# modes = ['x-largest-alea']

# Iterate over seeds and functions
for seed in seeds:
    for function in functions:
        if function == 'iq':
            for mode in modes:
                print(f"Experiment: '{function}' and random seed {seed}.")
                print(f"Training MLP classifier using '{function}' acquisition function and random seed {seed}.")

                exp_dir = f"{exp_path}/function-{function}-rs{seed}-mode:{mode}"
                command = [
                    "python3", "main.py", "--task", "agnews",
                    "--initial_size", "1000",
                    "--batch_size", "64",
                    "--learning_rate_main", "0.0001",
                    "--learning_rate_binary", "0.00005",
                    "--epochs", "30",
                    "--al_iterations", "30",
                    "--seed", str(seed),
                    "--pretrained",
                    "--freeze",
                    "--acquisition", function,
                    '--iq_mode', mode,
                    "--exp_path", exp_dir,
                    "--analysis"
                ]
                
                subprocess.run(command)
        else:
            print(f"Experiment: '{function}' and random seed {seed}.")
            print(f"Training MLP classifier using '{function}' acquisition function and random seed {seed}.")

            exp_dir = f"{exp_path}/function-{function}-rs{seed}"
            command = [
                "python3", "main.py", "--task", "agnews",
                "--initial_size", "1000",
                "--batch_size", "64",
                "--learning_rate_main", "0.0001",
                "--learning_rate_binary", "0.00005",
                "--epochs", "30",
                "--al_iterations", "30",
                "--seed", str(seed),
                "--pretrained",
                "--freeze",
                "--acquisition", function,
                "--exp_path", exp_dir,
                "--analysis"
            ]
            
            subprocess.run(command)

# Additional command (if needed)
# subprocess.run(["python3", "main.py", "--task", "trec", "--initial_size", "500", "--plot_results"])

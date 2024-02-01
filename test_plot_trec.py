import subprocess
command = [
    "python3", "main.py", "--task", "trec",
    "--initial_size", "500",
    "--plot_statistics"
]

subprocess.run(command)
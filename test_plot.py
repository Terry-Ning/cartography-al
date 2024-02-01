import subprocess
command = [
    "python3", "main.py", "--task", "agnews",
    "--initial_size", "1000",
    "--plot_statistics"
]

subprocess.run(command)
import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def plot_from_csv(args: argparse.Namespace):
    df_dict = {"accuracy": [], "interval": [], "strategy": []}
    strategies = ["bald", "cartography", "discriminative", "entropy", "leastconfidence", "random", "iq"]

    if args.task == "agnews":
        total_size = float(os.getenv("MAX_INSTANCE_AGNEWS"))
    else:
        total_size = float(os.getenv("MAX_INSTANCE_TREC"))

    for strat in strategies:
        for entry in os.scandir(f"{os.getenv('RESULTS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            if entry.path.endswith(".csv") and strategy == strat:

                with open(entry.path) as f:
                    df = pd.read_csv(f, sep="\t")
                    df_dict["accuracy"] += df["score"].tolist()
                    df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    df_dict["strategy"] += [strategy for _ in range(len(df))]

    sns.set(style="whitegrid")
    paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
    sns.set_context("paper", rc=paper_rc, font_scale=1.1)
    pal = sns.diverging_palette(260, 15, n=7, sep=10, center="dark")
    markers = {"random"     : "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
               "cartography": "o", 'iq': '*'}
    ax = sns.lineplot(data=df_dict,
                      x="interval",
                      y="accuracy",
                      hue="strategy",
                      style="strategy",
                      style_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "iq"],
                      hue_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "iq"],
                      markers=markers,
                      palette=pal,
                      ci=None)
    ax.set(xlabel="Percentage of Data Used", ylabel="Accuracy",
           title=f"Dataset: {args.task.upper()}, Seed set size: {args.initial_size}")
    ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="lower right", bbox_to_anchor=(1.0, 0.0),
              ncol=1)
    plt.tight_layout()
    plt.savefig(f"{os.getenv('PLOT_PATH')}{args.task}/{args.task}_results_{args.initial_size}.pdf", dpi=300)

def plot_from_csv_2(args: argparse.Namespace):
    df_dict = {"accuracy": [], "interval": [], "strategy": []}
    strategies = ["bald", "cartography", "discriminative", "entropy", "leastconfidence", "random", "iq-bi-cls", "iq-regression", "iq-ratio","iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea"]

    if args.task == "agnews":
        total_size = float(os.getenv("MAX_INSTANCE_AGNEWS"))
    else:
        total_size = float(os.getenv("MAX_INSTANCE_TREC"))

    for strat in strategies:
        for entry in os.scandir(f"{os.getenv('RESULTS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            if entry.path.endswith(".csv") and strategy == strat:

                with open(entry.path) as f:
                    df = pd.read_csv(f, sep="\t")
                    df_dict["accuracy"] += df["score"].tolist()
                    df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    df_dict["strategy"] += [strategy for _ in range(len(df))]

    sns.set(style="whitegrid")
    paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
    sns.set_context("paper", rc=paper_rc, font_scale=1.1)

    num_color = len(strategies)
    pal = sns.diverging_palette(260, 15, n=num_color, sep=10, center="dark")
    markers = {"random"     : "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
               "cartography": "o", "iq-bi-cls": '*', "iq-regression": '>', "iq-ratio": 'v',"iq-epi-alea": '<', "iq-epi-add-alea": 'p',"iq-x-largest-alea":"h"}
    ax = sns.lineplot(data=df_dict,
                      x="interval",
                      y="accuracy",
                      hue="strategy",
                      style="strategy",
                      style_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "iq-bi-cls", "iq-regression", "iq-ratio","iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea"],
                      hue_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "iq-bi-cls", "iq-regression", "iq-ratio","iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea"],
                      markers=markers,
                      palette=pal,
                      ci=None)
    ax.set(xlabel="Percentage of Data Used", ylabel="Accuracy",
           title=f"Dataset: {args.task.upper()}, Seed set size: {args.initial_size}")
    ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="lower right", bbox_to_anchor=(1.0, 0.0),
              ncol=1)
    plt.tight_layout()
    plt.savefig(f"{os.getenv('PLOT_PATH')}{args.task}/{args.task}_results_{args.initial_size}.pdf", dpi=300)

def plot_from_csv_3(args: argparse.Namespace):
    df_dict = {"accuracy": [], "interval": [], "strategy": []}
    strategies = ["bald", "cartography", "entropy", "leastconfidence", "random", "iq-bi-cls", "iq-regression", "iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea","epistemic"]

    if args.task == "agnews":
        total_size = float(os.getenv("MAX_INSTANCE_AGNEWS"))
    else:
        total_size = float(os.getenv("MAX_INSTANCE_TREC"))

    for strat in strategies:
        for entry in os.scandir(f"{os.getenv('RESULTS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            if entry.path.endswith(".csv") and strategy == strat:

                with open(entry.path) as f:
                    df = pd.read_csv(f, sep="\t")
                    df_dict["accuracy"] += df["score"].tolist()
                    df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    df_dict["strategy"] += [strategy for _ in range(len(df))]

    sns.set(style="whitegrid")
    paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
    sns.set_context("paper", rc=paper_rc, font_scale=1.1)

    num_color = len(strategies)
    pal = sns.diverging_palette(260, 15, n=num_color, sep=10, center="dark")
    markers = {"random"     : "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
               "cartography": "o", "iq-bi-cls": '*', "iq-regression": '>', "iq-epi-alea": '<', "iq-epi-add-alea": 'p',"iq-x-largest-alea":"h","epistemic":"v"}
    ax = sns.lineplot(data=df_dict,
                      x="interval",
                      y="accuracy",
                      hue="strategy",
                      style="strategy",
                      style_order=["random", "entropy", "leastconfidence", "bald", "cartography", "iq-bi-cls", "iq-regression", "iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea","epistemic"],
                      hue_order=["random", "entropy", "leastconfidence", "bald",  "cartography", "iq-bi-cls", "iq-regression", "iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea","epistemic"],
                      markers=markers,
                      palette=pal,
                      ci=None)
    ax.set(xlabel="Percentage of Data Used", ylabel="Accuracy",
           title=f"Dataset: {args.task.upper()}, Seed set size: {args.initial_size}")
    ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="lower right", bbox_to_anchor=(1.0, 0.0),
              ncol=1)
    plt.tight_layout()
    plt.savefig(f"{os.getenv('PLOT_PATH')}{args.task}/{args.task}_results_{args.initial_size}_part.pdf", dpi=300)


def plot_from_csv_4(args: argparse.Namespace):
    df_dict = {"accuracy": [], "interval": [], "strategy": []}
    # strategies = ["bald", "cartography", "entropy", "leastconfidence", "random","discriminative","epistemic","aleatoric","epi-add-alea"]
    strategies = [ "cartography", "epistemic","aleatoric","epi-add-alea"]

    if args.task == "agnews":
        total_size = float(os.getenv("MAX_INSTANCE_AGNEWS"))
    else:
        total_size = float(os.getenv("MAX_INSTANCE_TREC"))

    for strat in strategies:
        for entry in os.scandir(f"{os.getenv('RESULTS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            if entry.path.endswith(".csv") and strategy == strat:

                with open(entry.path) as f:
                    df = pd.read_csv(f, sep="\t")
                    df_dict["accuracy"] += df["score"].tolist()
                    df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    df_dict["strategy"] += [strategy for _ in range(len(df))]

    sns.set(style="whitegrid")
    paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
    sns.set_context("paper", rc=paper_rc, font_scale=1.1)

    num_color = len(strategies)
    pal = sns.diverging_palette(260, 15, n=num_color, sep=10, center="dark")
    markers = {"random"     : "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
               "cartography": "o", "aleatoric": '<', "epi-add-alea": 'p',"epistemic":"v"}
    ax = sns.lineplot(data=df_dict,
                      x="interval",
                      y="accuracy",
                      hue="strategy",
                      style="strategy",
                      style_order=["random", "entropy", "leastconfidence", "bald", "cartography", "discriminative","epistemic","aleatoric","epi-add-alea"],
                      hue_order=["random", "entropy", "leastconfidence", "bald",  "cartography", "discriminative","epistemic","aleatoric","epi-add-alea"],
                      markers=markers,
                      palette=pal,
                      ci=None)
    ax.set(xlabel="Percentage of Data Used", ylabel="Accuracy",
           title=f"Dataset: {args.task.upper()}, Seed set size: {args.initial_size}")
    ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="lower right", bbox_to_anchor=(1.0, 0.0),
              ncol=1)
    plt.tight_layout()
    plt.savefig(f"{os.getenv('PLOT_PATH')}{args.task}/{args.task}_results_{args.initial_size}_part2.pdf", dpi=300)

def plot_from_csv_part(args: argparse.Namespace):
    df_dict = {"accuracy": [], "interval": [], "strategy": []}
    strategies = ["random","cartography", "epistemic", "aleatoric", "epi-add-alea"]

    if args.task == "agnews":
        total_size = float(os.getenv("MAX_INSTANCE_AGNEWS"))
    else:
        total_size = float(os.getenv("MAX_INSTANCE_TREC"))

    for strat in strategies:
        for entry in os.scandir(f"{os.getenv('RESULTS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            if entry.path.endswith(".csv") and strategy == strat:
                with open(entry.path) as f:
                    df = pd.read_csv(f, sep="\t")
                    df_dict["accuracy"] += df["score"].tolist()
                    df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    df_dict["strategy"] += [strategy for _ in range(len(df))]

    sns.set(style="whitegrid")
    paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
    sns.set_context("paper", rc=paper_rc, font_scale=1.1)

    num_color = len(strategies)
    pal = sns.color_palette("husl", num_color)  # Generate a palette with the number of colors matching strategies

    markers = {"random": "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
               "cartography": "o", "aleatoric": '<', "epi-add-alea": 'p', "epistemic": "v"}
    style_order = ["random", "entropy", "leastconfidence", "bald", "cartography", "discriminative", "epistemic", "aleatoric", "epi-add-alea"]
    hue_order = ["random", "entropy", "leastconfidence", "bald", "cartography", "discriminative", "epistemic", "aleatoric", "epi-add-alea"]

    # Filter style_order and hue_order to include only the selected strategies
    style_order = [s for s in style_order if s in strategies]
    hue_order = [s for s in hue_order if s in strategies]

    ax = sns.lineplot(data=pd.DataFrame(df_dict),
                      x="interval",
                      y="accuracy",
                      hue="strategy",
                      style="strategy",
                      style_order=style_order,
                      hue_order=hue_order,
                      markers=markers,
                      palette=pal,
                      ci=None)
    
    ax.set(xlabel="Percentage of Data Used", ylabel="Accuracy",
           title=f"Dataset: {args.task.upper()}, Seed set size: {args.initial_size}")
    ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="lower right", bbox_to_anchor=(1.0, 0.0),
              ncol=1)
    plt.tight_layout()
    plt.savefig(f"{os.getenv('PLOT_PATH')}{args.task}/{args.task}_results_{args.initial_size}_part2.pdf", dpi=300)


def generate_pdf_table_from_csv(args: argparse.Namespace):
    df_dict = {"accuracy": [], "interval": [], "strategy": [], "step": []}
    strategies = ["random","bald",  "entropy", "leastconfidence", "discriminative","cartography",  "epistemic", "aleatoric", "epi-add-alea"]

    if args.task == "agnews":
        total_size = float(os.getenv("MAX_INSTANCE_AGNEWS"))
    else:
        total_size = float(os.getenv("MAX_INSTANCE_TREC"))

    for strat in strategies:
        for entry in os.scandir(f"{os.getenv('RESULTS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            if entry.path.endswith(".csv") and strategy == strat:
                with open(entry.path) as f:
                    df = pd.read_csv(f, sep="\t")
                    df_dict["accuracy"] += df["score"].tolist()
                    df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    df_dict["strategy"] += [strategy for _ in range(len(df))]
                    df_dict["step"] += df["step"].tolist()

    # Create a DataFrame from the dictionary
    result_df = pd.DataFrame(df_dict)

    # Calculate mean and variance
    summary_df = result_df.groupby(['interval', 'strategy', 'step']).agg(
        mean_accuracy=('accuracy', 'mean'),
        variance_accuracy=('accuracy', 'var')
    ).reset_index()

    # Generate PDF
    pdf_path = f"{os.getenv('PLOT_PATH')}{args.task}/{args.task}_results_{args.initial_size}_summary.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
    elements = []

    # Prepare data for table
    header = ['Step (Data Portion %)'] + strategies
    data = [header]

    # Get unique steps and intervals
    unique_steps = sorted(summary_df['step'].unique())

    for step in unique_steps:
        step_data = summary_df[summary_df['step'] == step]
        interval = step_data['interval'].iloc[0]
        row = [f"{step} ({interval:.2f}%)"]
        for strat in strategies:
            strat_data = step_data[step_data['strategy'] == strat]
            if not strat_data.empty:
                mean_accuracy = strat_data['mean_accuracy'].values[0]
                variance_accuracy = strat_data['variance_accuracy'].values[0]
                cell_value = f"{mean_accuracy:.4f} ({variance_accuracy:.4f})"
            else:
                cell_value = ""
            row.append(cell_value)
        data.append(row)

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduce font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Adjust column widths to fit the page
    col_widths = [80] + [65] * len(strategies)
    table._argW = col_widths

    elements.append(table)
    doc.build(elements)

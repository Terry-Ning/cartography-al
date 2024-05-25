import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def plot_statistics(args: argparse.Namespace):



    # strategies = ["bald", "cartography", "discriminative", "entropy", "leastconfidence", "random", "iq-bi-cls", "iq-regression", "iq-ratio", "iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea"]
    # strategies = ["iq-bi-cls", "iq-regression", "bald", "cartography", "discriminative", "entropy", "leastconfidence", "random","epistemic"]
    strategies = ["bald", "cartography", "discriminative", "entropy", "leastconfidence", "random","epi-add-alea","aleatoric","epistemic"]

    
    strat_dict = {}

    for strat in strategies:
        measurement_dict = {}
        for entry in os.scandir(f"{os.getenv('STATIS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            measurement = entry.path.split("/")[-1].split("_")[-1].split(".")[0]  # to be determined
            if entry.path.endswith(".csv") and strategy == strat:
                with open(entry.path) as f:
                    df = pd.read_csv(f)
                    # df_list.append(df)
                    if measurement not in measurement_dict:
                        measurement_dict[measurement] = []
                        measurement_dict[measurement].append(df)
                    else:
                        measurement_dict[measurement].append(df)
                    # df_dict["accuracy"] += df["score"].tolist()
                    # df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    # df_dict["strategy"] += [strategy for _ in range(len(df))]

        strat_dict[strat] = measurement_dict
    

    
    measurement_list = ['confidence','variability','correctness','aleatoric']


    for measurement in measurement_list:
        plt.figure()
        plt.clf()
        plt.cla()
        result_dict = {"iteration": [], "strategy": [], "std": [], 'mean': []}
        for strategy, measurement_dict in strat_dict.items():

            concated = pd.concat(measurement_dict[measurement], axis=1)
            concated['mean'] = concated.mean(axis=1)
            concated['std'] = concated.std(axis=1) 
            concated['iteration'] = concated.index # to be determined
            result_dict['mean'].extend(concated['mean'].tolist())
            result_dict['strategy'].extend([strategy for _ in range(len(concated))])
            result_dict['iteration'].extend(concated['iteration'].tolist())
                

                

        sns.set(style="whitegrid")
        paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
        sns.set_context("paper", rc=paper_rc, font_scale=1.1)

        num_color = len(strategies)
        pal = sns.diverging_palette(260, 15, n=num_color, sep=10, center="dark")
        markers = {"random"     : "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
                "cartography": "o", "iq-bi-cls": '*', "iq-regression": '>', "iq-ratio": 'v',"iq-epi-alea": '<', "iq-epi-add-alea": 'p',"iq-x-largest-alea":"h"}

        ax = sns.lineplot(data=result_dict,
                        x="iteration",
                        y="mean",
                        hue="strategy",
                        style="strategy",
                        style_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "iq-bi-cls", "iq-regression", "iq-ratio", "iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea"],
                        # style_order=[ "iq-bi-cls", "iq-regression", "iq-ratio"],
                        # hue_order=["iq-bi-cls", "iq-regression", "iq-ratio"],
                        hue_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "iq-bi-cls", "iq-regression", "iq-ratio", "iq-epi-alea","iq-epi-add-alea","iq-x-largest-alea"],
                        markers=markers,
                        palette=pal,
                        ci=None)
        ax.grid(True) 
        ax.set(xlabel="iteration", ylabel=measurement.upper(),
            title=f"{args.task.upper()}- {measurement.upper()}")
        ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="center left", bbox_to_anchor=(1.0, 0.0),
                ncol=1)
        plt.tight_layout()
        plt.savefig(f"{os.getenv('STATISPLOT_PATH')}{args.task}/{args.task}_results_{measurement}_final.pdf", dpi=300)
        plt.close()



def plot_statistics2(args: argparse.Namespace):

    strategies = ["bald", "cartography", "discriminative", "entropy", "leastconfidence", "random","epi-add-alea","aleatoric","epistemic"]

    
    strat_dict = {}

    for strat in strategies:
        measurement_dict = {}
        for entry in os.scandir(f"{os.getenv('STATIS_PATH')}{args.task}"):
            strategy = entry.path.split("/")[-1].split("_")[0]
            measurement = entry.path.split("/")[-1].split("_")[-1].split(".")[0]  # to be determined
            if entry.path.endswith(".csv") and strategy == strat:
                with open(entry.path) as f:
                    df = pd.read_csv(f)
                    # df_list.append(df)
                    if measurement not in measurement_dict:
                        measurement_dict[measurement] = []
                        measurement_dict[measurement].append(df)
                    else:
                        measurement_dict[measurement].append(df)
                    # df_dict["accuracy"] += df["score"].tolist()
                    # df_dict["interval"] += [(s + float(args.initial_size)) / total_size * 100 for s in df["step"].tolist()]
                    # df_dict["strategy"] += [strategy for _ in range(len(df))]

        strat_dict[strat] = measurement_dict
    

    
    measurement_list = ['confidence','variability','correctness','aleatoric']


    for measurement in measurement_list:
        plt.figure()
        plt.clf()
        plt.cla()
        result_dict = {"iteration": [], "strategy": [], "std": [], 'mean': []}
        for strategy, measurement_dict in strat_dict.items():

            concated = pd.concat(measurement_dict[measurement], axis=1)
            concated['mean'] = concated.mean(axis=1)
            concated['std'] = concated.std(axis=1) 
            concated['iteration'] = concated.index # to be determined
            result_dict['mean'].extend(concated['mean'].tolist())
            result_dict['strategy'].extend([strategy for _ in range(len(concated))])
            result_dict['iteration'].extend(concated['iteration'].tolist())
                

                

        sns.set(style="whitegrid")
        paper_rc = {'lines.linewidth': 1.8, 'lines.markersize': 5}
        sns.set_context("paper", rc=paper_rc, font_scale=1.1)

        num_color = len(strategies)
        pal = sns.diverging_palette(260, 15, n=num_color, sep=10, center="dark")
        markers = {"random"     : "P", "entropy": "s", "leastconfidence": "^", "bald": "d", "discriminative": "X",
               "cartography": "o", "aleatoric": '<', "epi-add-alea": 'p',"epistemic":"v"}

        ax = sns.lineplot(data=result_dict,
                        x="iteration",
                        y="mean",
                        hue="strategy",
                        style="strategy",
                        style_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "epi-add-alea","epistemic","aleatoric"],
                        # style_order=[ "iq-bi-cls", "iq-regression", "iq-ratio"],
                        # hue_order=["iq-bi-cls", "iq-regression", "iq-ratio"],
                        hue_order=["random", "entropy", "leastconfidence", "bald", "discriminative", "cartography", "epi-add-alea","epistemic","aleatoric"],
                        markers=markers,
                        palette=pal,
                        ci=None)
        ax.grid(True) 
        ax.set(xlabel="iteration", ylabel=measurement.upper(),
            title=f"{args.task.upper()}- {measurement.upper()}")
        ax.legend(fancybox=True, shadow=True, title="Sampling strategy", loc="center left", bbox_to_anchor=(1.0, 0.0),
                ncol=1)
        plt.tight_layout()
        plt.savefig(f"{os.getenv('STATISPLOT_PATH')}{args.task}/{args.task}_results_{measurement}_final.pdf", dpi=300)
        plt.close()
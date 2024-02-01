import logging

import numpy as np
import pandas as pd
import os


def get_statistics_datamap(confidence_run: list, variability_run: list, correctness_run: list) -> None:
    confidence = np.mean(confidence_run, axis=0)
    variability = np.mean(variability_run, axis=0)
    correctness = np.mean(correctness_run, axis=0)
    # for latex
    logging.info(f"confidence: {' & '.join([str(round(conf, 3)) for conf in confidence])} & {np.mean(confidence)}")
    logging.info(f"variability: {' & '.join([str(round(var, 3)) for var in variability])} & {np.mean(variability)}")
    logging.info(f"correctness: {' & '.join([str(round(cor, 3)) for cor in correctness])} & {np.mean(correctness)}")

def get_statistics_datamap_save(args, confidence_run: list, variability_run: list, correctness_run: list, aleatoric_run: list) -> None:
    confidence = np.mean(confidence_run, axis=0)
    variability = np.mean(variability_run, axis=0)
    correctness = np.mean(correctness_run, axis=0)
    aleatoric = np.mean(aleatoric_run, axis=0)
        # Convert to Pandas DataFrames
    df_confidence = pd.DataFrame({'Confidence': confidence})
    df_variability = pd.DataFrame({'Variability': variability})
    df_correctness = pd.DataFrame({'Correctness': correctness})
    df_aleatoric = pd.DataFrame({'Aleatoric': aleatoric})

    if args.acquisition == 'iq':
        confidence_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}-{args.iq_mode}_{args.initial_size}_{args.seed}_confidence.csv"
        variability_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}-{args.iq_mode}_{args.initial_size}_{args.seed}_variability.csv"
        correctness_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}-{args.iq_mode}_{args.initial_size}_{args.seed}_correctness.csv"
        aleatoric_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}-{args.iq_mode}_{args.initial_size}_{args.seed}_aleatoric.csv"
    
    else:
        confidence_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}_{args.initial_size}_{args.seed}_confidence.csv"
        variability_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}_{args.initial_size}_{args.seed}_variability.csv"
        correctness_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}_{args.initial_size}_{args.seed}_correctness.csv"
        aleatoric_path = f"{os.getenv('STATIS_PATH')}/{args.task}/{args.acquisition}_{args.initial_size}_{args.seed}_aleatoric.csv"

    # Save to CSV at specified paths
    df_confidence.to_csv(confidence_path, index=False)
    df_variability.to_csv(variability_path, index=False)
    df_correctness.to_csv(correctness_path, index=False)
    df_aleatoric.to_csv(aleatoric_path, index=False)

    # for latex
    logging.info(f"confidence: {' & '.join([str(round(conf, 3)) for conf in confidence])} & {np.mean(confidence)}")
    logging.info(f"variability: {' & '.join([str(round(var, 3)) for var in variability])} & {np.mean(variability)}")
    logging.info(f"correctness: {' & '.join([str(round(cor, 3)) for cor in correctness])} & {np.mean(correctness)}")
    logging.info(f"aleatoric: {' & '.join([str(round(alea, 3)) for alea in aleatoric])} & {np.mean(aleatoric)}")
from typing import Dict
import numpy as np

def generate_iq(probabilities: Dict) -> Dict:
    easy, hard, ambig = [], [], []
    grp_dict = {}
    thresh = 0.2
    percentile_thresh = 50

    # Calculate confidences and aleatoric uncertainties
    confidences = {idx: sum(proba) / len(proba) for idx, proba in probabilities.items()}
    aleatoric = {idx: sum(p * (1 - p) for p in proba) / len(proba) for idx, proba in probabilities.items()}
    aleatoric_values = list(aleatoric.values())
    percentile_value = np.percentile(aleatoric_values, percentile_thresh)

    # Categorize indices based on thresholds
    for idx, confidence in confidences.items():
        if confidence >= thresh and aleatoric[idx] <= percentile_value:
            easy.append(idx)
        elif confidence <= thresh and aleatoric[idx] <= percentile_value:
            hard.append(idx)
        else:
            ambig.append(idx)

    grp_dict['easy'] = easy
    grp_dict['hard'] = hard
    grp_dict['ambig'] = ambig

    return grp_dict

def prepare_data_for_iqal_regression(X_train_rep,X_pool_rep,probabilities):

    X_train, y_train = [], []

    aleatoric = {idx: sum(p * (1 - p) for p in proba) / len(proba) for idx, proba in probabilities.items()}



    for key, value in aleatoric.items():
        X_train.append(X_train_rep[int(key)])
        y_train.append(value)

    X_pool = np.array(X_pool_rep)
    X_train, y_train = np.array(X_train), np.array(y_train)


    return X_train , y_train, X_pool

def prepare_data_for_iqal_ratio(X_train_rep,X_pool_rep,probabilities):

    X_train, y_train_al, y_train_ep = [], [],[]

    aleatoric = {idx: sum(p * (1 - p) for p in proba) / len(proba) for idx, proba in probabilities.items()}
    variability = {idx: np.std(proba) for idx, proba in list(probabilities.items())}


    for key in aleatoric:
            X_train.append(X_train_rep[int(key)])
            y_train_al.append(aleatoric[key])
            y_train_ep.append(variability[key]) 

    X_pool = np.array(X_pool_rep)
    X_train, y_train_al , y_train_ep= np.array(X_train), np.array(y_train_al),np.array(y_train_ep)


    return X_train , y_train_al, y_train_ep, X_pool


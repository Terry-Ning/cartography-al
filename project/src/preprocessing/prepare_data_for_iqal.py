from typing import Tuple
import os
import numpy as np


def prepare_data_for_iqal(X_train_rep: list, X_pool_rep: list, group: dict) -> Tuple:

    X_train, y_train = [], []
    my_bool_value = os.getenv('GROUP_2')

    if my_bool_value =='true':
        for key, grplist in group.items():
            if key == 'easy' or 'hard':
                label = 0
            else:
                label = 1
            for idx in grplist:
                X_train.append(X_train_rep[int(idx)])
                y_train.append(label)
        
    else:
        for key, grplist in group.items():
            if key == 'easy':
                label = 0
            elif key == 'hard':
                label = 1
            else:
                label = 2

            for idx in grplist:
                X_train.append(X_train_rep[int(idx)])
                y_train.append(label)




    X_pool, y_pool = np.array(X_pool_rep), np.zeros(len(X_pool_rep))
    X_train, y_train = np.array(X_train), np.array(y_train)

    return X_train, y_train, X_pool, y_pool

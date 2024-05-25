import argparse
import logging
import os
import sys
from collections import defaultdict
from typing import Any, List

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from project.src.estimators.mlp_estimator import MLP
from project.src.utils.data_loader import DatasetMapper
from sklearn.metrics import accuracy_score
from torch.utils.data import DataLoader

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class MLPEstimator:
    def __init__(self, args: argparse.Namespace,
                 vocab_size: int,
                 emb_dim: int,
                 num_labels: int,
                 pt_emb: np.ndarray) -> None:
        self.model = MLP(args, vocab_size, emb_dim, num_labels, pt_emb).to(DEVICE)
        self.criterion = nn.NLLLoss()
        self.args = args
        self.optimizer = optim.AdamW(self.model.parameters(), lr=self.args.learning_rate_main)
        logging.info(f"Optimizing Main Classifier using {self.optimizer.__class__.__name__} with learning rate "
                     f"{self.args.learning_rate_main}.")

        # cartography
        self.cartography_plot = {"correctness": [], "variability": [], "confidence": []}
        self.probabilities = defaultdict(list)
        self.correctness = defaultdict(list)
        self.gold_labels = defaultdict(list)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        train = DatasetMapper(torch.from_numpy(X_train).long(), torch.from_numpy(y_train).long())
        loader_train = DataLoader(train, batch_size=self.args.batch_size)
        representations = []

        # training
        self.model.train()

        for epoch in range(self.args.epochs):
            epoch_loss = 0
            y_pred, y_gold = [], []

            for batch_x, batch_y in loader_train:
                self.model.zero_grad()

                batch_x = batch_x.to(DEVICE)
                batch_y = batch_y.to(DEVICE)

                if self.args.acquisition == "discriminative" or self.args.acquisition == "cartography" or self.args.acquisition == 'iq' or self.args.acquisition == 'epistemic'or self.args.acquisition == 'aleatoric' or self.args.acquisition == 'epi-add-alea':
                    if epoch == self.args.epochs - 1:
                        raw_logits = self.model.forward_discriminative(batch_x)  # this is different function from te 'forward' but influenced by the parameter of model, it's just the represents of the layer2
                        for raw_logit in raw_logits:
                            representations.append(raw_logit.detach().cpu().numpy())

                raw_logits = self.model.forward(batch_x)  # this is the log probabilities after log softmax
                predictions = self.model.predict_class(raw_logits)

                y_pred.extend(predictions)
                y_gold.extend(batch_y.tolist())
                # get probabilities and correctness per batch, for now only gold
                for idx, (raw_logit, gold_cls, pred_class) in enumerate(zip(raw_logits, batch_y, predictions),
                                                                        start=len(y_gold) - len(batch_x)):
                    self.probabilities[idx].append(float(torch.exp(raw_logit)[gold_cls]))
                    self.gold_labels[idx].append(int(gold_cls))
                    if gold_cls == pred_class:
                        self.correctness[idx].append(1)
                    else:
                        self.correctness[idx].append(0)

                loss = self.criterion(raw_logits, batch_y)
                loss.backward()

                self.optimizer.step()  #update the model parameter
                epoch_loss += loss

            sys.stdout.write(f"\rMain Classifier: Epoch {epoch}, train loss: {epoch_loss / len(y_gold):.4f}"
                             f", accuracy: {accuracy_score(y_pred, y_gold):.4f}")
            sys.stdout.flush()
            # logging.info(f"Main Classifier: Epoch {epoch}: train loss: {epoch_loss / len(y_gold)} "
            #               f"accuracy: {round(accuracy_score(y_pred, y_gold), 4)}")
        print("\n", end='')

        if self.args.acquisition == "discriminative" or self.args.acquisition == "cartography" or self.args.acquisition == 'iq' or self.args.acquisition == 'epistemic'or self.args.acquisition == 'aleatoric' or self.args.acquisition == 'epi-add-alea':
            return representations

    def predict(self, X_pool: np.ndarray, y_pool: np.ndarray) -> list:
        pool = DatasetMapper(torch.from_numpy(X_pool).long(), torch.from_numpy(y_pool).long())
        loader_pool = DataLoader(pool, batch_size=self.args.batch_size)
        probas = []

        self.model.eval()
        for batch_x, _ in loader_pool:
            batch_x = batch_x.to(DEVICE)

            with torch.no_grad():
                if self.args.acquisition == "bald":
                    raw_logits_list = [self.model.forward(batch_x) for _ in range(10)]
                    raw_logits_stacked = torch.stack(raw_logits_list).mean(dim=0).to(DEVICE)
                    probas.extend(self.model.predict_proba(raw_logits_stacked))

                elif self.args.acquisition == "discriminative" or self.args.acquisition == "cartography" or self.args.acquisition == 'iq' or self.args.acquisition == 'epistemic' or self.args.acquisition == 'aleatoric' or self.args.acquisition == 'epi-add-alea':
                    raw_logits = self.model.forward_discriminative(batch_x)
                    probas.extend(raw_logits.detach().cpu().numpy())

                else:
                    raw_logits = self.model.forward(batch_x)
                    probas.extend(self.model.predict_proba(raw_logits))

        return probas

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        test = DatasetMapper(torch.from_numpy(X_test).long(), torch.from_numpy(y_test).long())
        loader_test = DataLoader(test, batch_size=self.args.batch_size)

        y_pred = []
        y_gold = []

        self.model.eval()
        for batch_x, batch_y in loader_test:
            batch_x = batch_x.to(DEVICE)
            batch_y = batch_y.to(DEVICE)

            with torch.no_grad():
                raw_logits = self.model.forward(batch_x)
                predictions = self.model.predict_class(raw_logits)

                y_pred.extend(predictions)
                y_gold.extend(batch_y.tolist())

        test_accuracy = round(accuracy_score(y_pred, y_test), 4)

        return test_accuracy

    def weight_reset(self) -> None:
        self.model.weight_reset()

    def predict_class(self, predictions: torch.Tensor) -> List:
        return self.model.predict_class(predictions)

import argparse
import logging
import os
from typing import Any, Dict, Tuple
import torch
from transformers import DistilBertTokenizer, DistilBertModel

import numpy as np

logger = logging.getLogger(__name__)
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def data2feats(args: argparse.Namespace, sent: str, label: str, word_to_idx: Dict,
               label_to_idx: Dict) -> Tuple[Any, Any]:
    sent = sent.split()
    if args.task == "trec":
        feat = np.zeros([int(os.getenv("MAX_LEN_TREC"))], dtype=np.int64)
    else:
        feat = np.zeros([int(os.getenv("MAX_LEN_AGNEWS"))], dtype=np.int64)

    for word_idx, word in enumerate(sent):
        feat[word_idx] = word_to_idx[word]

    label = np.array(label_to_idx[label], dtype=np.int64)

    return feat, label


def initialize_train_pool_test(args: argparse.Namespace, train: np.ndarray, pool: np.ndarray, test: np.ndarray,
                               word_to_idx: Dict,
                               label_to_idx: Dict) -> Tuple:
    if args.bert:
        tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased")
        model = DistilBertModel.from_pretrained("distilbert-base-cased")
        model.to(DEVICE)

    logger.info("Generating training, pool, and test instances...")

    X_train, y_train = [], []
    X_pool, y_pool = [], []
    X_test, y_test = [], []

    for sent, cls in train:
        if args.bert:
            if args.task == "trec":
                model_inputs = tokenizer(sent, padding="max_length", max_length=42, return_tensors="pt")
            else:
                model_inputs = tokenizer(sent, padding="max_length", max_length=200, return_tensors="pt")
            with torch.no_grad():
                feat = torch.flatten(model(**model_inputs.to(DEVICE))[0][:, 0, :]).numpy()
            cls = np.array(label_to_idx[cls], dtype=np.int64)
        else:
            feat, cls = data2feats(args, sent, cls, word_to_idx, label_to_idx)
        X_train.append(feat)
        y_train.append(cls)

    if len(pool) != 0:
        for sent, cls in pool:
            if args.bert:
                if args.task == "trec":
                    model_inputs = tokenizer(sent, padding="max_length", max_length=42, return_tensors="pt")
                else:
                    model_inputs = tokenizer(sent, padding="max_length", max_length=200, return_tensors="pt")
                with torch.no_grad():
                    feat = torch.flatten(model(**model_inputs.to(DEVICE))[0][:, 0, :]).numpy()
                cls = np.array(label_to_idx[cls], dtype=np.int64)
            else:
                feat, cls = data2feats(args, sent, cls, word_to_idx, label_to_idx)
            X_pool.append(feat)
            y_pool.append(cls)

    else:
        X_pool = []
        y_pool = []

    for sent, cls in test:
        if args.bert:
            if args.task == "trec":
                model_inputs = tokenizer(sent, padding="max_length", max_length=42, return_tensors="pt")
            else:
                model_inputs = tokenizer(sent, padding="max_length", max_length=200, return_tensors="pt")
            with torch.no_grad():
                feat = torch.flatten(model(**model_inputs.to(DEVICE))[0][:, 0, :]).numpy()
            cls = np.array(label_to_idx[cls], dtype=np.int64)
        else:
            feat, cls = data2feats(args, sent, cls, word_to_idx, label_to_idx)
        X_test.append(feat)
        y_test.append(cls)

    logger.info(f"Statistics: {len(X_train)} train, {len(X_pool)} pool, {len(X_test)} test.")

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_pool, y_pool = np.array(X_pool), np.array(y_pool)
    X_test, y_test = np.array(X_test), np.array(y_test)

    return X_train, y_train, X_pool, y_pool, X_test, y_test
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import json
import os

import torch
import torch.nn as nn
import torch.nn.functional as F

independent_variables = ['amt_0', 'merch_lat_0', 'merch_long_0', 'unix_time_0', 'is_fraud_0',
                         'amt_1', 'merch_lat_1', 'merch_long_1', 'unix_time_1', 'is_fraud_1',
                         'amt_2', 'merch_lat_2', 'merch_long_2', 'unix_time_2', 'is_fraud_2',
                         'amt_3', 'merch_lat_3', 'merch_long_3', 'unix_time_3', 'is_fraud_3',
                         'amt_4', 'merch_lat_4', 'merch_long_4', 'unix_time_4', 'is_fraud_4',
                         'amt_5', 'merch_lat_5', 'merch_long_5', 'unix_time_5', 'is_fraud_5',
                         'amt_6', 'merch_lat_6', 'merch_long_6', 'unix_time_6', 'is_fraud_6',
                         'amt_7', 'merch_lat_7', 'merch_long_7', 'unix_time_7', 'is_fraud_7',
                         'amt_8', 'merch_lat_8', 'merch_long_8', 'unix_time_8', 'is_fraud_8',
                         'amt_9', 'merch_lat_9', 'merch_long_9', 'unix_time_9', 'is_fraud_9',
                         'amt_10', 'merch_lat_10', 'merch_long_10', 'unix_time_10',
                         'is_fraud_10', 'amt_11', 'merch_lat_11', 'merch_long_11',
                         'unix_time_11', 'is_fraud_11', 'amt', 'merch_lat', 'merch_long',
                         'unix_time']


def scaling(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    m = np.array(data, dtype=np.float32).reshape(1, -1)

    m0 = scaler.fit_transform(m.T[0::5]).T
    m1 = scaler.fit_transform(m.T[1::5]).T
    m2 = scaler.fit_transform(m.T[2::5]).T
    m3 = scaler.fit_transform(m.T[3::5]).T
    m4 = scaler.fit_transform(m.T[4::5]).T

    data = np.concatenate((m0, m1, m2, m3, m4), axis=1)

    return data


def evaluate_rule(rule, df):
    for index, row in df.iterrows():
        rule_passed = True
        for condition in rule["conditions"]:
            field = condition["field"]
            operator = condition["operator"]
            value = condition["value"]

            if operator == "<=":
                rule_passed &= row[field] <= value
            elif operator == ">":
                rule_passed &= row[field] > value

            if not rule_passed:
                break

        return 1 if rule_passed else 0


def rules_prediction(data):
    data = scaling(data)
    df = pd.DataFrame(data)
    df.columns = independent_variables

    with open('rules.json', 'r') as file:
        rules = json.load(file)['rules']

    return [evaluate_rule(rule, df) for rule in rules]

class CreditCardMLP(nn.Module):
    def __init__(self):
        super(CreditCardMLP, self).__init__()
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc5 = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc5(x)
        return x

device = torch.device("cpu")
ann = CreditCardMLP()#.to(device)

ann.load_state_dict(torch.load('/home/paulo/Projects/credit-card-fraud-detection/models/ann.pth', map_location=torch.device('cpu')))

def ann_prediction(data):
    data = scaling(data)
    data = torch.from_numpy(data)#.to(device)
    ann.eval()

    with torch.no_grad():
        logits = ann(data)
        return F.sigmoid(logits).item()
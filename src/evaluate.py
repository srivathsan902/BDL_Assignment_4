import numpy as np
from utils import *

def r2_score(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    TSS = np.sum((y_true - np.mean(y_true))**2)
    RSS = np.sum((y_true - y_pred)**2)
    
    r2 = 1 - RSS/TSS
    return r2

if __name__ == '__main__':
    y_true = json.load(open('gt_monthly_averages.json'))["MonthlyMeanTemperature"]
    y_pred = json.load(open('computed_monthly_averages.json'))['HourlyDryBulbTemperature']
    print(y_true)
    print(y_pred)
    print(r2_score(y_true, y_pred))
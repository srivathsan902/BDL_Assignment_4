import numpy as np
from dvclive import Live
from utils import *

def r2_score(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    TSS = np.sum((y_true - np.mean(y_true))**2)
    RSS = np.sum((y_true - y_pred)**2)
    
    r2 = 1 - RSS/TSS
    return r2

def evaluate_score(params_yaml_path):
    try:
        with open(params_yaml_path, 'r') as file:
            params = yaml.safe_load(file)
        
        gt_file_path = params['evaluate']['INPUT_PATHS'][0]
        computed_file_path = params['evaluate']['INPUT_PATHS'][1]
        gt_file_name = params['evaluate']['INPUT_FILE_NAMES'][0]
        computed_file_name = params['evaluate']['INPUT_FILE_NAMES'][1]
        output_path = params['evaluate']['OUTPUT_PATH']
        mapping = params['base']['MAPPING']
        
        print(output_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        gt = json.load(open(os.path.join(gt_file_path,gt_file_name)))
        pred = json.load(open(os.path.join(computed_file_path,computed_file_name)))
        
        for file_name, data in gt.items():
            gt_file_wise = data
            pred_file_wise = pred[file_name]
            
            for pred_field in pred_file_wise.keys():
                gt_field = mapping[pred_field]
                gt_data = gt_file_wise[gt_field]
                pred_data = pred_file_wise[pred_field]

                score = r2_score(gt_data, pred_data)
                with Live() as live:
                    live.log_metric("R2 Score", score)

    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

if __name__ == '__main__':
    # y_true = json.load(open('gt_monthly_averages.json'))["MonthlyMeanTemperature"]
    # y_pred = json.load(open('computed_monthly_averages.json'))['HourlyDryBulbTemperature']
    # print(y_true)
    # print(y_pred)
    # print(r2_score(y_true, y_pred))

    evaluate_score('params.yaml')
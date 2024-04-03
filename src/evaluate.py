import numpy as np
from dvclive import Live
from utils import *

def r2_score(y_true, y_pred):
    """

    Arguments: 
    y_true : list : List of true values.
    y_pred : list : List of predicted values.

    Computes the R2 score for the given true and predicted values.

    Returns:
    float : R2 score.

    """

    # Define a mask to identify missing values in either of the lists.
    mask = [(x != 'Missing') and (y != "Missing") for x, y in zip(y_true, y_pred)]
    y_true = [x for x, m in zip(y_true, mask) if m]
    y_pred = [y for y, m in zip(y_pred, mask) if m]

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    TSS = np.sum((y_true - np.mean(y_true))**2)
    RSS = np.sum((y_true - y_pred)**2)
    
    r2 = 1 - RSS/TSS
    return r2

def evaluate_score(params_yaml_path, live):

    """
    Arguments:
    params_yaml_path : str : Path to the YAML file containing parameters.
    live : dvclive.Live : Object to log metrics.

    Evaluates the R2 score for the given ground truth and predicted values.

    Returns:
    int : 1 if evaluation is successful, 0 otherwise.

    """

    try:
        # Read params from params.yaml file
        with open(params_yaml_path, 'r') as file:
            params = yaml.safe_load(file)
        
        gt_file_path = params['evaluate']['INPUT_PATHS'][1]
        computed_file_path = params['evaluate']['INPUT_PATHS'][0]
        gt_file_name = params['evaluate']['INPUT_FILE_NAMES'][1]
        computed_file_name = params['evaluate']['INPUT_FILE_NAMES'][0]
        output_path = params['evaluate']['OUTPUT_PATH']
        mapping = params['base']['MAPPING']     # To map the fields in ground truth and computed columns
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Read the files created by prepare.py and process.py
        gt = json.load(open(os.path.join(gt_file_path,gt_file_name)))
        pred = json.load(open(os.path.join(computed_file_path,computed_file_name)))
        
        file_wise_scores = {}       # To track R2 scores for each csv file downloaded
        for file_name, data in gt.items():
            gt_file_wise = data
            pred_file_wise = pred[file_name]
            all_scores = {}
            
            for pred_field in pred_file_wise.keys():
                gt_field = mapping[pred_field]
                gt_data = gt_file_wise[gt_field]
                pred_data = pred_file_wise[pred_field]
                score = r2_score(gt_data, pred_data)
                all_scores[gt_field] = score.round(3)
            
            file_wise_scores[file_name] = all_scores
        
            if not live.summary:
                live.summary = {}
        
        score_list = []
        for all_scores in file_wise_scores.values():
            for score in all_scores.values():
                score_list.append(score)
                print(score)

        average_R2_score = np.mean(np.array(score_list))
        live.summary["Average_R2_Score"] = average_R2_score
        json.dump(file_wise_scores, open(os.path.join(output_path,'scores.json'), 'w'))


    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0
    

if __name__ == '__main__':
    
    with open('params.yaml', 'r') as file:
            params = yaml.safe_load(file)

    output_path = params['evaluate']['OUTPUT_PATH']
    
    # Create a Live object to log metrics
    live = Live(os.path.join(output_path,'live'),dvcyaml = False)
    evaluate_score('params.yaml', live)
    live.make_summary()
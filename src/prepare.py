from utils import *
from utils import load_params

def extract_GT_Monthly_Averages(params_yaml_path):
    with open(params_yaml_path, 'r') as file:
        params = yaml.safe_load(file)

    gt_cols = params['base']['GT_COLUMNS']
    input_path = params['prepare']['INPUT_PATH']
    output_path = params['prepare']['OUTPUT_PATH']
    output_file_name = params['prepare']['OUTPUT_FILE_NAME']

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for files in os.listdir(input_path):
        file_wise_ans = {}
        if files.endswith('.csv'):
            file_name = files.split('.')[0]
            df = pd.read_csv(os.path.join(input_path, files))
            df = df[gt_cols
                    ]
            gt_monthly_averages = {}
            for column in gt_cols:
                df[column] = pd.to_numeric(df[column], errors='coerce')
                gt_monthly_averages[column] = df[column][df[column].notna()].tolist()

            file_wise_ans[file_name] = gt_monthly_averages

    json.dump(file_wise_ans, open(os.path.join(output_path,output_file_name), 'w'))
    
    return 1

if __name__ == "__main__":
    
    extract_GT_Monthly_Averages(params_yaml_path = 'params.yaml')
    

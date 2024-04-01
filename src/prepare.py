from utils import *
from utils import load_params

def extract_GT_Monthly_Averages(df, gt_cols):
    gt_monthly_averages = {}
    for column in gt_cols:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        gt_monthly_averages[column] = df[column][df[column].notna()].tolist()
    return gt_monthly_averages


if __name__ == "__main__":
    params = load_params()
    print(params, flush=True)
    url = params['BASE_URL']
    year = params['YEAR']
    n_locs = params['N_LOCATIONS']
    expected_cols = params['EXPECTED_COLUMNS']
    gt_cols = params['GT_COLUMNS']

    # df = pd.read_csv('01381099999.csv')
    df = pd.read_csv('99999903063.csv')
    df = df[gt_cols]
    gt_monthly_averages = extract_GT_Monthly_Averages(df, gt_cols)
    json.dump(gt_monthly_averages, open('gt_monthly_averages.json', 'w'))
    

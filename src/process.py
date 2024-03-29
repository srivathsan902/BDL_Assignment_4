from utils import *
from utils import load_params

def compute_monthly_averages(df, year, expected_cols):
    df.set_index('DATE', inplace=True)
    start_year = str(year)
    full_date_range = pd.date_range(start=f'{start_year}-01-01', end=f'{start_year}-12-31', freq='ME')
    print(full_date_range)
    # Put average of 0 for the month, if the month is not encountered at all in the file
    monthly_avg_df = df.resample('ME').mean().round(3).reindex(full_date_range).fillna(0)
    print('Hello',monthly_avg_df)
    # monthly_avg_df['month'] = monthly_avg_df.index.month
    
    # monthly_avg_df.set_index('month', inplace=True)
    # monthly_avg_df = monthly_avg_df[expected_cols + ['month']]

    computed_monthly_averages = monthly_avg_df.to_dict(orient='index')
    print(computed_monthly_averages)
    # selected_monthly_averages = {key: value for key, value in computed_monthly_averages.items() if key in expected_cols}

    return computed_monthly_averages


if __name__ == "__main__":
    params = load_params()
    print(params, flush=True)
    url = params['BASE_URL']
    year = params['YEAR']
    n_locs = params['N_LOCATIONS']
    expected_cols = params['EXPECTED_COLUMNS']

    df = pd.read_csv('99999903063.csv')
    cols = ['DATE'] + expected_cols
    df = df[cols]
    df['DATE'] = df['DATE'].apply(pd.to_datetime, errors='coerce')
    df = df.dropna(subset=['DATE'] ,how='any')

    df[expected_cols] = df[expected_cols].apply(pd.to_numeric, errors='coerce')
    df = df.dropna(subset=['HourlyDryBulbTemperature'] ,how='any')
    
    computed_monthly_averages = compute_monthly_averages(df, year, expected_cols)
    ans = {}
    averages =[]
    for key, value in computed_monthly_averages.items():
        for k, v in value.items():
            if k in ans.keys():
                ans[k].append(v)
            else:
                ans[k] = [v]
    for key, value in ans.items():
        print(key, value)
    
    json.dump(ans, open('computed_monthly_averages.json', 'w'))


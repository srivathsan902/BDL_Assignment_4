from utils import *
from utils import load_params

def compute_monthly_averages(params_yaml_path):
    """
    Arguments:
    params_yaml_path : str : Path to the YAML file containing parameters.

    Extracts the monthly averages of the ground truth values from the given CSV files.
    Stores the extracted values in a JSON file.

    Returns:
    int : 1 if extraction is successful, 0 otherwise.

    """

    try:
        # Read params from params.yaml file
        with open(params_yaml_path, 'r') as file:
            params = yaml.safe_load(file)
        
        year = params['base']['YEAR']
        expected_cols = params['base']['EXPECTED_COLUMNS']
        input_path = params['process']['INPUT_PATH']
        output_path = params['process']['OUTPUT_PATH']
        output_file_name = params['process']['OUTPUT_FILE_NAME']

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        file_wise_ans = {}      # To store monthly averages for various columns for each csv file downloaded
        for files in os.listdir(input_path):
            if files.endswith('.csv'):
                file_name = files.split('.')[0]
                df = pd.read_csv(os.path.join(input_path, files))

                cols = ['DATE'] + expected_cols
                df = df[cols]
                df['DATE'] = df['DATE'].apply(pd.to_datetime, errors='coerce')
                df = df.dropna(subset=['DATE'] ,how='any')
                df[expected_cols] = df[expected_cols].apply(pd.to_numeric, errors='coerce')
                df = df.dropna(subset=expected_cols ,how='any')
                
                df.set_index('DATE', inplace=True)
                start_year = str(year)
                full_date_range = pd.date_range(start=f'{start_year}-01-01', end=f'{start_year}-12-31', freq='ME')

                # Handle Missing entries
                # Put average of 0 for the month, if the month is not encountered at all in the file
                monthly_avg_df = df.resample('ME').mean().round(2).reindex(full_date_range).fillna('Missing')

                computed_monthly_averages = monthly_avg_df.to_dict(orient='index')
                
                # Rearranging the data to store monthly averages for various columns in a single dictionary
                ans = {}
                for key, value in computed_monthly_averages.items():
                    for k, v in value.items():
                        if k in ans.keys():
                            ans[k].append(v)
                        else:
                            ans[k] = [v]

                file_wise_ans[file_name] = ans

        json.dump(file_wise_ans, open(os.path.join(output_path,output_file_name), 'w'))

        return 1
    
    except Exception as e:
        print(f"An error occurred in : {str(e)}")
        return 0


if __name__ == "__main__":

    compute_monthly_averages(params_yaml_path = 'params.yaml')
    


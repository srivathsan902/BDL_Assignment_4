from utils import *
from utils import load_params
import random

def extract_csv_link(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all links in the webpage
            links = soup.find_all('a', href=True)
            # Filter out CSV links
            csv_links = [url + link['href'] for link in links if link['href'].endswith('.csv')]
            # If there are multiple CSV links, choose one or implement your logic
            if csv_links:
                return csv_links
            else:
                print("No CSV link found on the webpage.")
                return None
        else:
            print(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def verify_csv(filename, expected_cols, gt_cols):
    try:
        df = pd.read_csv(filename)
        # Check if the CSV file has expected columns
        required_cols = expected_cols + gt_cols
        if set(required_cols).issubset(df.columns):
            for col in required_cols:
                if df[col].isnull().values.all():
                    os.remove(filename)
                    print(f"CSV file '{filename}' does not have expected columns.", flush=True)
                    return False
            return True
        else:
            return False
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def download_csv(params_yaml_path):
    
    with open(params_yaml_path, 'r') as file:
        params = yaml.safe_load(file)
    
    url = params['base']['BASE_URL']
    year = params['base']['YEAR']
    n_locs = params['base']['N_LOCATIONS']
    expected_cols = params['base']['EXPECTED_COLUMNS']
    gt_cols = params['base']['GT_COLUMNS']

    folder = params['download']['DOWNLOAD_PATH']
    SAMPLES_TO_CHOOSE = 100

    if not os.path.exists(folder):
        os.makedirs(folder)

    url = url + str(year) + '/'
    csv_urls = extract_csv_link(url)
    # csv_urls = csv_urls[0:1]
    # temp = url + '99999903063.csv'
    # csv_urls.append(temp)

    cnt = 0
    required_links = random.sample(csv_urls, min(SAMPLES_TO_CHOOSE, len(csv_urls)))
    for csv_url in required_links:
        response = requests.get(csv_url)
        if response.status_code == 200:
            filename = os.path.join(folder, csv_url.split('/')[-1])  # Get filename from URL
            print(filename, flush=True)
            with open(filename, 'wb') as f:
                f.write(response.content)

            if verify_csv(filename, expected_cols, gt_cols):
                print(f"CSV file downloaded successfully as '{filename}'", flush=True)
                cnt += 1
            
            if cnt == n_locs:
                return 1
        else:
            print(f"Failed to download CSV file. Status code: {response.status_code}", flush=True)
    

if __name__ == "__main__":

    download_csv(params_yaml_path = 'params.yaml')
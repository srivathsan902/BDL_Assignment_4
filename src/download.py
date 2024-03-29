from utils import *
from utils import load_params

def extract_csv_link(url):
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

def verify_csv(filename, expected_cols):
    df = pd.read_csv(filename)
    # Check if the CSV file has expected columns
    if set(expected_cols).issubset(df.columns):
        for col in expected_cols:
            if df[col].isnull().values.all():
                os.remove(filename)
                print(f"CSV file '{filename}' does not have expected columns.", flush=True)
                return False
        return True
    else:
        return False


def download_csv(csv_url, N_LOCATIONS, expected_cols, folder = 'intermediate'):
    cnt = 0
    if os.path.exists(folder):
        shutil.rmtree(folder)
    for csv_url in csv_urls:
        response = requests.get(csv_url)
        if response.status_code == 200:
            filename = os.path.join(folder, csv_url.split('/')[-1])  # Get filename from URL
            print(filename, flush=True)
            os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"CSV file downloaded successfully as '{filename}'", flush=True)

            if verify_csv(filename, expected_cols):
                cnt += 1
            # cnt += 1
            if cnt == N_LOCATIONS:
                break
        else:
            print(f"Failed to download CSV file. Status code: {response.status_code}", flush=True)
        

if __name__ == "__main__":
    params = load_params()
    print(params, flush=True)
    url = params['BASE_URL']
    year = params['YEAR']
    n_locs = params['N_LOCATIONS']
    expected_cols = params['EXPECTED_COLUMNS']

    url = url + str(year) + '/'
    csv_urls = extract_csv_link(url)
    # print(csv_urls[:10])
    if csv_urls:
        download_csv(csv_urls, n_locs, expected_cols)
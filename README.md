# DVC Pipeline

## Overview
The National Centers for Environmental Information contains several data pertaining to climatological parameters observed over diverse set of locations all around the world. The data is collected over 13400 stations, and it is collected every hour. It is of engineering interest to analyse these data, and gain insights about the climate. 

The fields in the datasets have certain fields that can be derived from other fields. In this task, we aim to see the degree of acceptance between manually computing a monthly average field from hourly fields vs directly using the monthly average field. R2 is a measured used for this comparison.

## Installation
Use Ubuntu terminal for seamless experience.

Create a venv in the Pipeline directory using the command: `python -m venv venv` and the activate it using `source venv/bin/activate`. After this install the packages in the requirements.txt file using the command: `pip install -r requirements.txt`.

The dvc stage add commands are present in `dvc_commands.txt`. Run these one by one to add stages and create the `dvc.yaml` file. This file is already present for use, so run the commands if any changes have been made.

## Steps to run the pipeline
Clone the repository to the local machine using 
`git clone https://github.com/srivathsan902/BDL_Assignment_3`

Create a virtual environment using `python3 -m venv venv`
Give `sudo apt update` and `sudo apt install python3.10-venv` in case errors arise.

Then add main as the branch name:
`git remote add origin https://github.com/srivathsan902/BDL_Assignment_3`

Then do `dvc exp run` to conduct experiments.

Login to `https://studio.iterative.ai`/ to track the experiments.

Once the experiment is run, use `git push -u origin main` to update it in the `https://studio.iterative.ai` page.


## Walkthrough of Code
The `src` folder has the relevant python scripts for the pipeline. 
1. `download.py` : Based on the year and number of files to download, it downloads files from the given website, checks if the files have necessary columns with non-empty entries and removes the undesired files. Saves them into `downloaded` folder

2. `process.py` : It computes the monthly average of the fields and saves it into `processed` folder as `processed_averages.json`

3. `prepare.py` : It retrieves the monthly average fields and saves it into `prepared` folder as `actual_averages.json`

4. `evaluate.py` : It computes R2 score between every relevant field for every data file considered. Saves the results in `eval` folder as `metrics.json`

## Additional Information
In case you add some code on top of this, you may have to add the libraries that you use in the `requirements.txt` file `Pipeline` directory. Repeat the `pip install -r requirements.txt` command.

Note that dvc is used primarily to track changes in models, data which are not trackable using git due to size constraints. So ensure the data files are tracked by dvc and not git while using.

In case your system consumes a lot of memory and disk usage, then open the command promt with administrator access and run `wsl --shutdown` after this.

## Helpful Links
* [Documentation for DVC](https://dvc.org/doc)
* [Youtube Resource for Understanding DVC](https://www.youtube.com/watch?v=KjEkn5qz5zM)





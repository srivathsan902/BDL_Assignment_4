import os
import shutil
import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import json


import yaml
def load_params():
    with open('params.yaml', 'r') as file:
        params = yaml.safe_load(file)
    return params
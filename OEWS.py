import pandas as pd
import requests
import zipfile
import io
import os
from typing import Union
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import numpy as np

def pull_oews_by_ind(year: int, type: str = "ind") -> pd.DataFrame:
    """
    Downloads QCEW "National industry-specific and by ownership" data table.

    Args:
        type (str): Type of data to download (default: "ind")
        year (int): Year of data (default: 2023)

    Returns:
        pd.DataFrame: Processed employment data
    """
    if type != "ind":
        raise ValueError("Currently only 'ind' type is supported")

    # Convert year to two digits for URL
    year_2d = str(year)[-2:]

    # Create a session with retries and timeouts
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # Comprehensive browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    # Try different URL formats
    urls = [
        f"https://www.bls.gov/oes/special.requests/oesm{year_2d}in4.zip",
        f"https://www.bls.gov/oes/special-requests/oesm{year_2d}in4.zip"
    ]

    response = None
    for url in urls:
        try:
            response = session.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                break
        except Exception as e:
            continue

    if not response or response.status_code != 200:
        raise Exception("Failed to download file from all URLs")

    # Create a BytesIO object from the content
    zip_data = io.BytesIO(response.content)

    # Create temp directory
    temp_dir = "temp_extract"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Extract the zip file
    with zipfile.ZipFile(zip_data) as zip_ref:
        for file_info in zip_ref.filelist:
            # Get the filename without the directory structure
            filename = os.path.basename(file_info.filename)
            # Skip if it's a directory
            if not filename:
                continue
            # Extract only the file we need
            if filename == f"nat5d_6d_M{year}_dl.xlsx":
                source = zip_ref.read(file_info.filename)
                target_path = os.path.join(temp_dir, filename)
                with open(target_path, "wb") as f:
                    f.write(source)

                # Read the Excel file
                df = pd.read_excel(target_path)

                # Clean up: remove temporary directory
                import shutil
                shutil.rmtree(temp_dir)

                # Keep only required columns
                return df

    raise FileNotFoundError(f"Could not find required Excel file in the zip archive")
import os
import requests
import zipfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS = {
    'craft_mlt_25k.zip': 'https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip',
    'english_g2.zip': 'https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip'
}

def download_and_extract(url, zip_path, extract_dir):
    import urllib.request
    logger.info(f"Downloading {url} to {zip_path}...")
    try:
        urllib.request.urlretrieve(url, zip_path)
                
        logger.info(f"Extracting {zip_path} to {extract_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        os.remove(zip_path)
    except Exception as e:
        logger.error(f"Failed to download or extract {url}: {e}")

def setup_easyocr_models():
    # EasyOCR looks for models in ~/.EasyOCR/model
    home_dir = os.path.expanduser('~')
    model_dir = os.path.join(home_dir, '.EasyOCR', 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    for filename, url in MODELS.items():
        zip_path = os.path.join(model_dir, filename)
        # Check if extracted file exists (.pth)
        pth_name = filename.replace('.zip', '.pth')
        if not os.path.exists(os.path.join(model_dir, pth_name)):
            download_and_extract(url, zip_path, model_dir)
        else:
            logger.info(f"{pth_name} already exists in {model_dir}")

if __name__ == '__main__':
    setup_easyocr_models()

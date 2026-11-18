import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1]/"backend"/".env")
from ingestion.importer import import_papers
print(import_papers(int(os.getenv("DATASET_SIZE","100"))))

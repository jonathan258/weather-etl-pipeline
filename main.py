from extract import extract
from transform import transform
from load import load

def run_pipeline():
    print("Extracting...")
    raw = extract()

    print("Transforming...")
    df = transform(raw)

    print("Loading...")
    load(df)

    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
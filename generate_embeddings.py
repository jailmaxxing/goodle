import requests
from transformers import AutoTokenizer, AutoModel
import torch
import json

# URL to download the input JSON file
INPUT_URL = "http://51.38.51.221/result.json"
INPUT_FILE = "result.json"
OUTPUT_FILE = "result_with_embeddings.json"

def download_file(url, filename):
    print(f"Downloading {url} ...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Saved to {filename}")

def embed(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Mean pooling of last hidden state
    return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

def main():
    # Download the input file
    download_file(INPUT_URL, INPUT_FILE)

    # Load model and tokenizer
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    print(f"Loading model '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # Load input data
    print(f"Loading input file {INPUT_FILE} ...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        pages = json.load(f)

    result = []
    for i, page in enumerate(pages):
        print(f"[{i+1}/{len(pages)}] Processing: {page.get('title', '')}")
        try:
            text = (page.get("title", "") + " " + page.get("description", ""))[:512]
            embedding = embed(text, tokenizer, model)
            page["embedding"] = embedding
            result.append(page)
        except Exception as e:
            print(f"⚠️ Error processing page '{page.get('title', '')}': {e}")
            continue

    # Save output file
    print(f"Saving output to {OUTPUT_FILE} ...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("✅ Done.")

if __name__ == "__main__":
    main()

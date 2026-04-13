import pickle
import re

# Load model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def handler(request):
    try:
        data = request.get_json()
        resume = data.get("resume", "")

        cleaned = clean_text(resume)
        vector = tfidf.transform([cleaned])
        prediction = model.predict(vector)[0]

        return {
            "statusCode": 200,
            "body": {
                "predicted_role": prediction
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
        }
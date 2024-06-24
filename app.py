from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
os.environ['HF_HOME'] = 'D:\code\\tinhoctre\\blabla\\cache'
tokenizer = AutoTokenizer.from_pretrained("michellejieli/NSFW_text_classifier")
model = AutoModelForSequenceClassification.from_pretrained("michellejieli/NSFW_text_classifier")
#cache_asset = cached_assets_path(assets_dir="/blabla/cache")
app = Flask(__name__)
@app.route("/hello")
def home():
    return "Home"
@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id":user_id,
        "name":"John Doe",
        "email":"john@gmail.com",
    }
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
        return jsonify(user_data),200
@app.route("/",methods = ["POST"])
def create_user():
    login(token="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")
    data = request.get_json()
    url = data["url"]
    video_id = url.split("=")[1]
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    transcript = transcript[:1024]
    classifier = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")
    result = classifier(transcript)
    res = {
        "text":transcript,
        "result":result,
    }
    return jsonify(res),201
if __name__ == "__main__":
    app.run(debug= True)
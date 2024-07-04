from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask_cors import CORS,cross_origin
#cache_asset = cached_assets_path(assets_dir="/blabla/cache")
import os
#os.environ['HF_HOME'] = 'D:\code\\tinhoctre\\blabla\\cache'
#tokenizer = AutoTokenizer.from_pretrained("michellejieli/NSFW_text_classifier")
#model = AutoModelForSequenceClassification.from_pretrained("michellejieli/NSFW_text_classifier")
#Model AI source 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/hello")
@cross_origin()
def home():
    return "Home"
@app.route("/",methods = ["POST"])
def create_user():
    login(token="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")
    data = request.get_json()
    url = data["url"]
    video_id = url.split("=")[1]
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        error ={
            "text":"Không thể kiểm tra video này vui lòng kiểm tra lại phụ đề, ngôn ngữ và Url!",
            "result":"Thất bại",
            "check":"Fail",
        }
        return jsonify(error),201

    classifier =pipeline("text-classification", model="s-nlp/roberta_toxicity_classifier")
    count = 0
    texts = []
    for i in transcript_list:
        transcript = i['text']
        result = classifier(transcript)
        transcript = transcript.replace("\u266a",' ')
        transcript = transcript.replace("\n",' ')
        transcript = transcript.strip()
        transcript = transcript.lower()
        print(transcript)
        print(result[0]["label"])
        if((result[0]["label"]=="toxic" and '[' not in transcript and '(' not in i['text']) or "[ __ ]" in transcript ):
            count+=1
            texts.append(transcript)
        if("[ __ ]" in transcript):
            count+=1
    if round(count/len(transcript_list),3)>0.04:
        final_result = "NSFW"
        print(count)
    else:
        final_result = "SFW"
        print(count)
    
    res = {
        "text":texts,
        "total":len(transcript_list),
        "count_toxic":str(count),
        "result":final_result,
        "check":"received successful",
    }
    return jsonify(res),201
if __name__ == "__main__":
    app.run(debug= True)
from flask import Flask, request, jsonify, Response
from flask_cors import CORS 
import torch
from transformers import pipeline

app = Flask(__name__)

CORS(app)

model_id = "meta-llama/Llama-3.2-1B"

pipe = pipeline(
    "text-generation", 
    model=model_id, 
    torch_dtype=torch.bfloat16, 
    device_map="auto"
)

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        input_text = data['text']

        def generate_stream():
            result = pipe(input_text)
            print(result)
            for r in result:
                for token in r["generated_text"]:
                    yield token 

        return Response(generate_stream(), content_type='text/plain;charset=utf-8')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
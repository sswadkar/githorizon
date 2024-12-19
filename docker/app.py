from flask import Flask, request, jsonify, Response
from flask_cors import CORS 
from litgpt import LLM

app = Flask(__name__)

CORS(app)

llm = LLM.load("microsoft/phi-2")

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        input_text = data['text']

        def generate_stream():
            result = llm.generate(input_text, stream=True, max_new_tokens=1_000)  # Stream tokens
            for token in result:
                yield token 

        return Response(generate_stream(), content_type='text/plain;charset=utf-8')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(threaded=True)
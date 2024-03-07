from flask import Flask, request
from SemanticSearchAccelerator import query_vectordb

app = Flask(__name__)

@app.route('/')
def root():
    return "API is running!"

@app.route('/api/generate_response', methods=['GET','POST'])
def generate_response():
    try :
        
        if request.method == 'GET':
            user_query = request.args.get('query')
        elif request.method == 'POST':
            data = request.get_json()
            user_query = data.get('user_query')

        response = query_vectordb(user_query)
        print("At API endpoint : " +response)
        # return "Success", 201
        return response
    
    except Exception as e:
        print(e)
        return "Error", 500

if __name__ == '__main__':
    app.run(port=3000,host="0.0.0.0",debug=False)

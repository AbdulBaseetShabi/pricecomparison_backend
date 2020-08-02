from flask import request, jsonify, Flask
from bestbuyproducts import bestbuyproducts
from savedItems import savedItems
from Administrator import administrator
from customers import customers

app = Flask(__name__)
app.register_blueprint(bestbuyproducts)
app.register_blueprint(savedItems)
app.register_blueprint(administrator)
app.register_blueprint(customers)

@app.route('/', methods=['GET'])
def main():
    return "Server is running"

@app.errorhandler(404)
def endPointNotFound(error):
    return "Endpoint not found"

if __name__ == "__main__":
    app.run()
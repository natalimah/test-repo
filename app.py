from flask import Flask, request
from flask.templating import render_template
import pymongo
from bson.json_util import dumps
import os

app = Flask(__name__)

myclient = pymongo.MongoClient(f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}",username=os.environ['USERNAME'],password=os.environ['PASSWORD'])
mydb = myclient["flask"]
products_coll=mydb["products"]

@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')

@app.route('/apipage', methods=['GET'])
def api_page():
    return render_template('apipage.html')

@app.route('/listprod', methods=['GET'])
def list_page():
    query = products_coll.find({})
    return render_template('listproductpage.html',products=query)

@app.route('/addprod', methods=['GET'])
def add_page():
    return render_template('addproductpage.html')

@app.route('/deleteprod', methods=['GET','POST'])
def delete_page():
    query = products_coll.find({})
    return render_template('deleteproductpage.html',products=query)

@app.route('/api/products', methods = ['GET'])
def list_products():
    query = products_coll.find({})
    result = dumps(query)
    return result

@app.route('/api/products/<name>', methods = ['GET'])
def get_product(name):
    query = products_coll.find({"name":name})
    result = dumps(query)
    if result == "[]":
        return "not found"
    else:
        return result

@app.route('/api/addproduct', methods = ['POST'])
def add_product():
    name = request.json["name"]
    price = request.json["price"]
    quantity = request.json["quantity"]
    mydict = {"name":name,"price":price,"quantity":quantity}
    products_coll.insert_one(mydict)
    return "200"

@app.route('/api/addproductform', methods = ['POST'])
def add_product_form():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    mydict = {"name":name,"price":price,"quantity":quantity}
    products_coll.insert_one(mydict)
    return render_template('addproductpage.html')  

@app.route('/api/deleteproduct/<name>', methods = ['DELETE'])
def delete_product(name):
    query = {"name":name}
    products_coll.delete_one(query)
    return "200"

@app.route('/deleteprodform', methods = ['POST'])
def delete_product_form():
    product = request.form['name']
    query = {"name":product}
    status = products_coll.delete_one(query)
    return render_template('deleteproductpage.html',status=status)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)
from flask import Flask,render_template,url_for,request,redirect
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.artsea
collection = db.cart
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/shop')
def shop():
    return render_template('shop.html')
@app.route('/cart')
def cart():
    pipeline = [
        {
            '$group': {
                '_id': None,
                'total': {'$sum': {'$toInt': '$cost'}}
            }
        }
    ]
    result = list(collection.aggregate(pipeline))

    if result:  # Check if the result list is not empty
        sum_value = result[0]['total']
    else:
        sum_value = 0  # Set a default value if the result list is empty

    data = collection.find()
    return render_template('cart.html', data=data, sum=sum_value)
  
@app.route('/dele',methods=['POST'])
def dele():
    val = request.form['cost']
    print(val)
    collection.delete_one({'cost': val})
    return redirect('cart')
@app.route('/final')
def final():
    pipeline = [
        {
            '$group': {
                '_id': None,
                'total': {'$sum': {'$toInt': '$cost'}}
            }
        }
    ]
    result = list(collection.aggregate(pipeline))

    if result:  # Check if the result list is not empty
        sum_value = result[0]['total']
    else:
        sum_value = 0  # Set a default value if the result list is empty

    data = collection.find()
    collection.delete_many({})  # Deleting all documents in the collection
    return render_template('final.html', d=data, sum=sum_value)

@app.route('/add', methods=['POST'])
def add():
    head = request.form['head']
    img = request.form['img']
    cost = request.form['cost']
    data = {
        'heading': head,
        'image': img,
        'cost': cost,
    }
    collection.insert_one(data)
    return redirect('shop')
if __name__=='__main__':
    app.run(debug=True)
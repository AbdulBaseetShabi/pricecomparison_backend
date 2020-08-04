"""
This artificat is implemented as an API using flask.
It retrieves the first ten product results from BestBuy's website based on a user input keyword. ItemName, price, url, retailer name, imageUrl are retrieved.
Returns the list of products in json format, sorted by price.
New Update: Returns the first ten product results from Ebay as well. Same information is retrieved using the same keyword. Make sure to pipinstall ebaysdk.
Programmer: Daniel Zhou
Variables:
    search: Keyword to search (string)
    data: Retrieves name, price, and url of items/products (dictionary)
    products: List of retrieved products. Returned in json format.
"""
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from flask import request, jsonify, Blueprint
import urllib.request, json 
from Administrator import sendResponse

bestbuyproducts = Blueprint('bestbuyproducts',__name__)

@bestbuyproducts.route('/bestbuyproducts/products', methods=['GET'])
def api_all():
    error = False

    response = {'result': 'null'}
    try:
        if 'search' in request.args:
            search = request.args['search']
        else:
            response['error_2'] = "Error: No search field provided. Please search for products."
        link = "https://api.bestbuy.com/v1/products(search={})?format=json&show=name,salePrice,addToCartUrl,largeImage&apiKey=N0ReEPP28MPw3Gd2xSIAQ5dM".format(search)
        data = json.loads(urllib.request.urlopen(link).read().decode()) #Retrieve data from bestbuyAPI
        products = data['products']
        for item in products: #Rename url and include retailer name to the items
            item['url']  = item.pop('addToCartUrl')
            item['retailer'] = 'BestBuy'
        
        #eBay Code 
        api = Connection(config_file='ebay.yaml') #Connect to the API using authentication file
        res = api.execute('findItemsAdvanced', {'keywords': search}) #Retrieve data using eBay developer API

        items = res.reply.searchResult.item[:10] #Only use the first 10 results
        ebay_products = []
        
        for item in items:
            ebay_product = {}
            name = item.get('title') #Retrieve name, price, image, link to purchase product

            sellingStatus = item.get('sellingStatus')
            currentPrice = sellingStatus.get('currentPrice')
            salePrice = float(currentPrice.get('value'))
            
            largeImage = item.get('galleryURL')
            url = item.get('viewItemURL')
            #Format dictionary to match the categories that were used for the Best Buy products
            ebay_product['name'] = name 
            ebay_product['retailer'] = 'eBay'
            ebay_product['salePrice'] =salePrice 
            ebay_product['largeImage'] = largeImage 
            ebay_product['url'] = url
            
            ebay_products.append(ebay_product)
            
        products.extend(ebay_products) #Extend the dictionary to include the ebay products
        products = sorted(products, key = lambda i: i['salePrice']) #Sort by price
        response['result'] = products
    except Exception as err:
        response['error'] = str(err)
        error = True
    
    return sendResponse(response, error)
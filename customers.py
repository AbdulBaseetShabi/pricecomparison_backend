from flask import request, jsonify, Blueprint
from Connect import Connect
from Administrator import sendResponse

conn = Connect('database.txt')
customers = Blueprint('customers',__name__)

@customers.route('/customers/history', methods=['GET'])
def history():
    """
    -------------------------------------------------------
    Checks history status of a user
    Use: history = Customer.history(conn, itemCode, userID)
    -------------------------------------------------------
    Parameters:
        userId - a user ID number (int)
    Returns:
        history - the search history of the user (tuple)
    -------------------------------------------------------
    """
    userID=request.args['userID']
    response = {'history' : 'null'}
    error = False

    try:
        if userID !='null':
            sql = "SELECT * FROM history WHERE userID = %s ORDER BY searchedDate DESC"
            conn.cursor.execute(sql, (userID,))
            data = conn.cursor.fetchall()
            response['history'] = []
            for item in data:
                response['history'].append({
                    'itemName' : item[3],
                    'searchedDate' : item[2],
                    'itemID' : item[1]
                })
    except Exception as err:
        request['error'] = err
        error = True
    
    return sendResponse(response,error)

@customers.route('/customers/addHistory', methods=['GET'])
def addHistory():
    """
    -------------------------------------------------------
    add to user history
    -------------------------------------------------------
    Parameters:
        itemName - item's name (int)
        userId - a user ID number (int)
        searchDate - search date (datetime)
    Returns:
        updatedHistory - user's new history (boolean)
    -------------------------------------------------------
    """
    userID = request.args['userID'] 
    searchDate = request.args['searchDate']
    itemName = request.args['itemName']
    error = False

    response = {'update' : 'null'}
    if userID != 'null':
        try:
            sql = "INSERT INTO history (userID, searchedDate, itemName) VALUES (%s, %s, %s)"
            conn.cursor.execute(sql, (userID, searchDate, itemName, ))
            response['update'] = 'done'
        except Exception as err:
            response['error'] = str(err)
            error = True
    
    return sendResponse(response,error)


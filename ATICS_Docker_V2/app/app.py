""" module: App
    file: App.py
    application: Automated tool box inventory control system 
    language: python
    computer: i5 9600k
    opertaing system: windows subsystem  ubuntu
    course: CPT_S 422
    team: Null Terminators
    author: Navin Sabandith
    date: 4/10/24
"""

"""
This is the API to establish communication between the computer vision componenet and the database.

Security Note: The MySQL configuration, as well as the API key, are currently hardcoded below. 
While this approach may suffice for the immediate scope, it poses a slight security risk.
For enhanced security, it's recommended to consider moving these configurations to more secure storage options, such as environment variables, a configuration file, 
or a secure database. This would help mitigate the risk of unauthorized access to sensitive data and adhere to best practices in secure software development. 
"""

from flask import Flask, request, jsonify
import mysql.connector
import time
app = Flask(__name__)
mysql_config = {
    'host': 'db',
    'user': 'root',
    'port': '3306',
    'password': 'navin',
    'database': 'hiline_tool_database' 
}
try:
    conn = mysql.connector.connect(**mysql_config)
    print("Connected to MySQL database")
except mysql.connector.Error as err:
    print("Error: ", err)

conn = None
"""
    name: establish_connection
    purpose: connect to the sql database and retry every 5 seconds.
    operation: trivial
    note: If making an api call and the database is down, the api will be in an infinite loop until the database is back up. This is for redundancy purposes.
"""
def establish_connection():
    global conn
    while True:
        try:
            conn = mysql.connector.connect(**mysql_config)
            print("Connected to MySQL database")
            break
        except mysql.connector.Error as err:
            print("Error: ", err)
            print("Retrying database connection in 5 seconds...")
            time.sleep(5)

establish_connection()

"""
    name: before_request
    purpose: Check if the database is connected & if the api_key matches before every request
    operation: trivial
"""
@app.before_request
def before_request():
    global conn
    if conn is None or not conn.is_connected():
        print("Database connection lost. Reconnecting...")
        establish_connection()
    
    if 'API-Key' not in request.headers or request.headers['API-Key'] != 'Navinskey':
        return jsonify({'error': 'Unauthorized access'}), 401

"""
    name: add_drawer
    purpose: endpoint for adding a drawer to the drawer table
    operation: Obtain the data dictionary from the json and issue a query to the db.
"""
@app.route('/add_drawer', methods=['POST'])
def add_drawer():
    data = request.json
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Drawer (DrawerNum, DrawerBoxNum, DrawerStartX, DrawerStartY, DrawerPixelWidth, DrawerPixelHeight, DrawerYAML, DrawerPicAllTools, DrawerPicNoTools, DrawerSymbols) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['DrawerNum'], data['DrawerBoxNum'], data['DrawerStartX'], data['DrawerStartY'], data['DrawerPixelWidth'], data['DrawerPixelHeight'], data['DrawerYAML'], data['DrawerPicAllTools'], data['DrawerPicNoTools'], data['DrawerSymbols'])
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Drawer added successfully'}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()

"""
    name: add_tool
    purpose: endpoint for adding a tool to the tools table
    operation: Obtain the data dictionary from the json and issue a query to the db.
"""
@app.route('/add_tool', methods=['POST'])
def add_tool():
    data = request.json
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Tools (ToolName, ToolType, ToolClassifierType, toolDrawerID, ToolSymbolAvailable, ToolSymbolPath, ToolCheckedOut, ToolStartX, ToolStartY, ToolPixelWidth, ToolPixelHeight, ToolPictureWithPath, ToolPictureWithoutPath, ToolInfoTakenManually) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['ToolName'], data['ToolType'], data['ToolClassifierType'], data['toolDrawerID'], data['ToolSymbolAvailable'], data['ToolSymbolPath'], data['ToolCheckedOut'], data['ToolStartX'], data['ToolStartY'], data['ToolPixelWidth'], data['ToolPixelHeight'], data['ToolPictureWithPath'], data['ToolPictureWithoutPath'], data['ToolInfoTakenManually'])
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Tool added successfully'}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()

"""
    name: add_event
    purpose: endpoint for adding an event to the event table
    operation: Obtain the data dictionary from the json and issue a query to the db.
"""
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Events (EventType, EventToolID, EventTimestamp, EventDrawerLocation, EventUserID, EventNotes) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data['EventType'], data['EventToolID'], data['EventTimestamp'], data['EventDrawerLocation'], data['EventUserID'], data['EventNotes'])
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Event added successfully'}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()

"""
    name: get_tools_info
    purpose: endpoint for obtaining tool information given a drawerid
    operation: Obtain the drawerid from the args and issue a query to the db.
"""
@app.route('/get_tools_info', methods=['GET'])
def get_tools_info():
    try:
        cursor = conn.cursor(dictionary=True) 
        drawer_id = request.args.get('drawer_id')
        query = "SELECT * FROM Tools WHERE ToolDrawerID = %s"
        cursor.execute(query, (drawer_id,))
        tools = cursor.fetchall()
        if tools:
            return jsonify(tools), 200
        else:
            return jsonify({'message': 'No tools found for the specified drawer ID'}), 404

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

    finally:
        cursor.close()

"""
    name: get_drawers_info
    purpose: endpoint for obtaining drawer information given a drawerid
    operation: Obtain the drawerid from the args and issue a query to the db.
"""
@app.route('/get_drawers_info', methods=['GET'])
def get_drawers_info():
    try:
        cursor = conn.cursor(dictionary=True) 
        box_num = request.args.get('boxNum')
        query = "SELECT * FROM Drawer WHERE DrawerBoxNum = %s"
        cursor.execute(query, (box_num,))
        drawers = cursor.fetchall()
        if drawers:
            return jsonify(drawers), 200
        else:
            return jsonify({'message': 'No drawers found for the specified box number'}), 404

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

    finally:
        cursor.close()

"""
    name: update_tool
    purpose: endpoint for updating tool checked out status given tool and tooldrawer id
    operation: Obtain the parameters from the json and issue a query to the db.
"""
@app.route('/update_tool', methods=['POST'])
def update_tool():
    try:
        checked_out = request.json.get('checkedOut')
        tool_id = request.json.get('toolID')
        drawer_id = request.json.get('drawerID')

        cursor = conn.cursor()
        query = "UPDATE Tools SET ToolCheckedOut = %s WHERE ToolID = %s AND ToolDrawerID = %s"
        cursor.execute(query, (checked_out, tool_id, drawer_id))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({'message': 'Tool updated successfully'}), 200
        else:
            return jsonify({'message': 'No tool found with the specified IDs'}), 404

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

    finally:
        cursor.close()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

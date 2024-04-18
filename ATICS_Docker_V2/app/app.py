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
@app.before_request
def before_request():
    global conn
    if conn is None or not conn.is_connected():
        print("Database connection lost. Reconnecting...")
        establish_connection()

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

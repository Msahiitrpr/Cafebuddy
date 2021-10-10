import mysql.connector

def DataUpdate(session_id,order_details):

     mydb = mysql.connector.connect( host="localhost", user="root",
     passwd="1234", database="test_rasa")

     mycursor = mydb.cursor()

     #sql="CREATE TABLE ORDERS (id VARCHAR(255) , order_name VARCHAR(255));"
     sql='INSERT INTO ORDERS (id,order_name) VALUES ("{0}","{1}");'.format(session_id,order_details)

     mycursor.execute(sql)

     mydb.commit()

     print(mycursor.rowcount,"record inserted")


def Datafetch(session_id):

     mydb = mysql.connector.connect(host="localhost", user="root",
     passwd="1234", database="test_rasa")

     mycursor=mydb.cursor()

     sql="""SELECT distinct order_name FROM ORDERS WHERE id = %s"""

     mycursor.execute(sql, (session_id,))

     records=mycursor.fetchall()

     return records

def Datamenu(cusene):

     mydb = mysql.connector.connect(host="localhost", user="root",
     passwd="1234", database="test_rasa")

     print(cusene)
     mycursor=mydb.cursor()
     if cusene==None:
          sql="""SELECT food FROM menu;"""
          mycursor.execute(sql)
     else :
          sql = """SELECT food FROM menu where cuisine = %s;"""
          mycursor.execute(sql, (cusene,))


     records=mycursor.fetchall()
     print(records)
     return records



def Datafetch_cuisine():

    mydb = mysql.connector.connect(host="localhost", user="root",
                                    passwd="1234", database="test_rasa")
    mycursor = mydb.cursor()
    sql = """SELECT Distinct cuisine FROM menu"""
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return records

# if __name__=="__main__":
#   Datafetch("123")
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="1234"
# )

#print(mydb)
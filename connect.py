# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 13:58:50 2023

@author: Shivani_SB
"""
def showall():
    sql= "SELECT * from REGISTER"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The username is : ",  dictionary["USERNAME"])
        print("The Password is : ",  dictionary["PASSWORD"])
        print("The Role is : ",  dictionary["ROLE"])
      #  print("The Branch is : ",  dictionary["BRANCH"])
       # print("The Password is : ",  dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def getdetails(email,password):
    sql= "select * from REGISTER where email='{}' and password='{}'".format(email,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The username is : ", dictionary["USERNAME"])
        print("The Password is : ", dictionary["PASSWORD"])
        print("The Role is : ", dictionary["ROLE"])
       # print("The Branch is : ", dictionary["BRANCH"])
        
        dictionary = ibm_db.fetch_both(stmt)
        
def insertdb(conn, name, email, username, password, role):
    sql = "INSERT into REGISTER VALUES('{}', '{}', '{}', '{}', '{}')".format(name, email, username, password, role)
    stmt = ibm_db.exec_immediate(conn, sql)
    print("Number of affected rows: ", ibm_db.num_rows(stmt))

try:
    import ibm_db
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA(1).crt;UID=wrj97286;PWD=yr9TGZdqnKAYr7Tx",'','')
    print(conn)
    print("Connection successful...")
    
    insertdb(conn, "Hari", "Hari@gmail.com",'manu', 'manu', 1)
    getdetails("Hari@gmail.com", 'manu')
    showall()

except Exception as e:
    print("Error:", e)
    print(ibm_db.conn_errormsg())




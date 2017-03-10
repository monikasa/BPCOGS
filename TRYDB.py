#!/usr/bin/python
'''BPGEPR
    :groep_10'''

#import os
import psycopg2

'''Deze functie runt een bash file. De file verzameld
	informatie vanuit online databases en maakt er bruikbare 
	tekst bestanden van
	:return: empty string'''
#def make_files():
	#os.system ('bash Tables_files.sh')
	#return ""

'''Deze functie maakt een connectie aan met de server
   	van postgresql.

	:return: connetion
	:return: connection variable'''


def connect():
    conn_string = "host='localhost' dbname='postgres' user='monika'" \
                  " password='elzelek'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    return conn, cursor



def make_tables(cursor, conn):

    cursor.execute(
        "CREATE TABLE EIWIT (Eiwit_id VARCHAR (100) "
        "NOT NULL, Database VARCHAR (100) NOT NULL, COG_id "
        "VARCHAR (100), CONSTRAINT pk_eiwit PRIMARY KEY (Eiwit_id))") # Wat is COG_id? Komt het ergens uit of is het gewoon index nr? Het staat als FK in erd waarvoor?
    cursor.execute(
        "CREATE TABLE ORGANISME (Organisme_id VARCHAR (100), "
	"Beschrijving VARCHAR (100000), CONSTRAINT pk_organisme " 		"PRIMARY KEY (Organisme_id))")

    cursor.execute(
        "CREATE TABLE BLAST (Eiwit_id_1 VARCHAR (100) , "
        "Database_1 VARCHAR (100), Eiwit_id_2 VARCHAR (100), "
        "Database_2 VARCHAR (100), Organisme_id_1 VARCHAR (100), "
	"Organisme_id_2 VARCHAR (100), CONSTRAINT pk_blast "
	"PRIMARY KEY (Eiwit_id_1, Database_1, "
	"Eiwit_id_2, Database_2), CONSTRAINT fk_1_blast "
	"FOREIGN KEY (Eiwit_id_1) REFERENCES EIWIT "
	"(Eiwit_id), CONSTRAINT fk_2_blast " 	
	"FOREIGN KEY (Eiwit_id_2) REFERENCES EIWIT " 		
	"(Eiwit_id), CONSTRAINT fk_org1_blast "
	"FOREIGN KEY (Organisme_id_1) REFERENCES "
	"ORGANISME  (Organisme_id), CONSTRAINT "
	"fk_org2_blast FOREIGN KEY (Organisme_id_2) "
	"REFERENCES ORGANISME (Organisme_id))") #CONSTRAINTS CHECKEN!!
    cursor.execute(
        "CREATE TABLE PATHWAY (Pathway_id VARCHAR (100), Eiwit_id " 
	"VARCHAR (100), Beschrijving VARCHAR "
        "(100000), CONSTRAINT pk_patwhay PRIMARY KEY (Pathway_id))")
   
    cursor.execute(
        "CREATE TABLE KOPPEL_PATHWAY (Eiwit_id VARCHAR (100), "
        "Pathway_id VARCHAR (100), CONSTRAINT pk_koppel PRIMARY KEY (Eiwit_id, Pathway_id), CONSTRAINT fk_eiw_koppel FOREIGN KEY (Eiwit_id) REFERENCES EIWIT (Eiwit_id), CONSTRAINT fk_path_koppel FOREIGN KEY(Pathway_id) REFERENCES PATHWAY (Pathway_id)) ")

   
    conn.commit()
    return ""

def fill_tables(cursor, conn):
    cursor.execute(
            "INSERT INTO EIWIT VALUES(%s,%s,%s)",
            ("1", "1d", "1c"))
    cursor.execute(
            "INSERT INTO EIWIT VALUES(%s,%s,%s)",
            ("2", "2d", "2c"))
    cursor.execute(
            "INSERT INTO ORGANISME VALUES (%s,%s)",
            ("1o", "dsjfgsdzgkh"))
    cursor.execute(
            "INSERT INTO ORGANISME VALUES (%s,%s)",
            ("2o", "dsjfgsdzgkh"))
    cursor.execute(
            "INSERT INTO PATHWAY VALUES (%s,%s,%s)",
            ("11", "1", "fsdjklhnvrbuyfucahvbioayugiu"))
    cursor.execute(
            "INSERT INTO PATHWAY VALUES (%s,%s,%s)",
            ("22", "2", "fsdjklhnvrbuyfucahvbioayugiu"))
    cursor.execute(
            "INSERT INTO KOPPEL_PATHWAY VALUES(%s,%s)",
            ("1", "11"))
    cursor.execute(
            "INSERT INTO KOPPEL_PATHWAY VALUES(%s,%s)",
            ("2", "22"))
    cursor.execute(
            "INSERT INTO BLAST VALUES (%s,%s,%s,%s,%s,%s)",
            ("1","1d", "2", "2d", "1o", "2o"))


    conn.commit()
    return ""
   
def main():

    conn, cursor = connect()
    make_tables(cursor, conn)
    fill_tables(cursor, conn)
    print "Database is met succes opgezet."


if __name__ == "__main__":
    main()


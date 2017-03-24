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
    conn_string = "host='localhost' dbname='bpcogs' user='sven'" \
                  " password='bpcogs1617'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    return conn, cursor

def drop_db(cursor, conn):
    cursor.execute("DROP TABLE IF EXISTS KOPPEL_PATHWAY")
    cursor.execute("DROP TABLE IF EXISTS BLAST")
    cursor.execute("DROP TABLE IF EXISTS EIWIT")
    cursor.execute("DROP TABLE IF EXISTS PATHWAY")

    conn.commit()

def make_tables(cursor, conn):

    cursor.execute(
        "CREATE TABLE EIWIT (Eiwit_id VARCHAR (100) NOT NULL,"
        "ORG VARCHAR(100) NOT NULL, Database VARCHAR (100) NOT NULL, COG_id VARCHAR (100), Sequetie VARCHAR (10000) NOT NULL,"
        "CONSTRAINT pk_eiwit PRIMARY KEY (Eiwit_id, ORG))") # Wat is COG_id? Komt het ergens uit of is het gewoon index nr? Het staat als FK in erd waarvoor?
    #cursor.execute(
        #"CREATE TABLE ORGANISME (Organisme_id VARCHAR (100), "
	#"Beschrijving VARCHAR (100000), CONSTRAINT pk_organisme " 		"PRIMARY KEY (Organisme_id))")

    cursor.execute(
        "CREATE TABLE BLAST (Eiwit_id_1 VARCHAR (100),"
        " ORG_1 VARCHAR (100), Eiwit_id_2 VARCHAR (100),"
        "ORG_2 VARCHAR (100),"
	    "CONSTRAINT pk_blast PRIMARY KEY (Eiwit_id_1, ORG_1, Eiwit_id_2, ORG_2),"
	    "CONSTRAINT fk_1_blast FOREIGN KEY (Eiwit_id_1, ORG_1) REFERENCES EIWIT(Eiwit_id, ORG),"
	    "CONSTRAINT fk_2_blast FOREIGN KEY (Eiwit_id_2, ORG_2) REFERENCES EIWIT(Eiwit_id, ORG))")
    cursor.execute(
        "CREATE TABLE PATHWAY (Pathway_id VARCHAR (100),"
	    "Beschrijving VARCHAR (10000),"
        "CONSTRAINT pk_patwhay PRIMARY KEY (Pathway_id))")
   
    cursor.execute(
        "CREATE TABLE KOPPEL_PATHWAY (Eiwit_id VARCHAR (100), "
        "ORG VARCHAR (100), Pathway_id VARCHAR (100),"
        "CONSTRAINT pk_koppel PRIMARY KEY (Eiwit_id, ORG, Pathway_id),"
        "CONSTRAINT fk_eiw_koppel FOREIGN KEY (Eiwit_id, ORG) REFERENCES EIWIT (Eiwit_id, ORG),"
        "CONSTRAINT fk_path_koppel FOREIGN KEY(Pathway_id) REFERENCES PATHWAY (Pathway_id)) ")

   
    conn.commit()
    return ""

def fill_tables(cursor, conn):

    db_eiwit = [x[:-1].split(";") for x in open("db_eiwit", "r").readlines()]
    db_blast = [x[:-1].split(";") for x in open("db_blast", "r").readlines()]
    db_pathway = [x[:-1].split(";") for x in open("db_pathway", "r").readlines()]
    db_pathway_koppel = [x[:-1].split(";") for x in open("db_pathway_koppel", "r").readlines()]

    for line in db_eiwit:
        cursor.execute(
            "INSERT INTO EIWIT VALUES(%s,%s,%s,%s,%s)",
            (line[0], line[1], line[2], (line[3]) if line[3] != "NULL" else None, line[4]))

    for line in db_blast:
        cursor.execute(
            "INSERT INTO BLAST VALUES(%s,%s,%s,%s)",
            (line[0], line[1], line[2], line[3]))

    for line in db_pathway:
        cursor.execute(
            "INSERT INTO PATHWAY VALUES(%s,%s)",
            (line[0], line[1]))

    for line in db_pathway_koppel:
        cursor.execute(
            "INSERT INTO KOPPEL_PATHWAY VALUES(%s,%s,%s)",
            (line[0], line[1], line[2]))

    """
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
    """


    conn.commit()
    return ""
   
def main():

    conn, cursor = connect()
    drop_db(cursor, conn)
    make_tables(cursor, conn)
    fill_tables(cursor, conn)
    print("Database is met succes opgezet.");


if __name__ == "__main__":
    main()


# must be a v0.10.1 version - next version (v1.0.0+) is not supported for older password mysql
from pymysql import Connect
from pymysql import err
from warnings import catch_warnings
from warnings import simplefilter
from sys import exc_info

# Custom
from log import Log

class DataBase():

    def __init__(self):
        self.log = Log()

    def open_connection(self, connect):
        try:
            server = connect["server"]
            port = connect["port"]
            db = connect["db"]
            user = connect["user"]
            password = connect["pass"]
            self.query = connect["sql_querry"]
            self.query_count = connect["sql_count_query"]
            self.index_application_column = int(connect["index_application_column"])
            self.index_file_name_coumn = int(connect["index_file_name_column"])
        
            self.log.info(f'Conecting to {server} ...')
            with catch_warnings(record=True) as warn:
                simplefilter("always")
                self.db = Connect(host = server, port = int(port), database = db, user = user, password = password)
                print(warn[0].message, "\n")
                self.log.warning(warn[0].message)
            
            self.log.info("Conected to DB")
            print("Nawiązano połączenie z bazą ! ")
    
        except err.OperationalError as err:
            self.log.error(err)

        except:
            print(exc_info()[1])
            self.log.error(exc_info()[1])

        finally:
            pass
                
    def exec_export_rows_querry(self):

        cur = self.db.cursor()
        query = self.query

        self.log.info(f"Read row from DB")
        cur.execute(f"""{query}""")
        record = cur.fetchall()
        
        return record
        
    def exec_count_files(self, record):
        index_application_column = int(self.index_application_column)
        query_count = self.query_count
        tab_record_count = []
        previous_row_id = None
        files = 0
        application = 0

        for row in record:
            # if(row[0] != row_id and row_id != None):
            current_row_id = row[index_application_column]

            if(current_row_id != previous_row_id):
                cur = self.db.cursor()
                sql_count_row_per_id = query_count
                sql_count_row_per_id = eval('f"{}"'.format(sql_count_row_per_id)) 
                cur.execute(sql_count_row_per_id)
                record_count = cur.fetchall()
                tab_record_count += record_count
                
                application += 1

            files += 1
            previous_row_id = row[index_application_column]
            
        return application, files, tab_record_count

    def close_connection(self):
        self.log.info(f'Disconecting from lanmytest.qa.bpsa.pl ...')
        self.db.close()
        self.log.info("Disconected from DB")
        print("Rozłączono połączenie z bazą !")

    def __del__(self):
        pass
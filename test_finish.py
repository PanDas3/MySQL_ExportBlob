from configparser import ConfigParser
from pymysql import Connect
from pathlib import Path
from os import listdir, path

file_config = "config.ini"
config = ConfigParser()
config.read(file_config)

server = config["MySQL"]["Server"]
port = config["MySQL"]["Port"]
db = config["MySQL"]["DB"]
usr = config["MySQL"]["User"]
passwd = config["MySQL"]["Pass"]
export_path = config["Export"]["Export_path_from_db"]

sql_count_query = "SELECT count(id) FROM base.table where id = "

conn = Connect(host=server, port=int(port), database=db, user=usr, password=passwd)
cur = conn.cursor()

if(path.isdir(export_path) == True):
    dir_listing = listdir(export_path)
    count_files = 0
    tab = []
    for dir in dir_listing:
        cur.execute(f"{sql_count_query} '{dir}'")
        result = cur.fetchone()
        result = int(result[0])
        dir_listing2 = listdir(f"{export_path}\\{dir}\\{dir}")
        count = 0
        for file in dir_listing2:
            valid_xml = Path(file).suffixes
            if(valid_xml[0] == ".html"):
                pass
            
            else:
                count_files += 1
                count += 1

        if(result != count):
            tab.append(dir)
            print(f"Not ok {dir}")
            with open("result.txt", mode="a") as f:
                f.write(f"not ok {dir}")
                f.close()

        elif(result == count):
            print(f"OK {dir}")

print(tab)
print(count_files)
with open("result.txt", mode="a") as f:
    f.write(f"Number all files: {count_files}")
    f.close()
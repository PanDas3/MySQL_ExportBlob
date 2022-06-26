from configparser import ConfigParser
from configparser import MissingSectionHeaderError
from sys import exc_info
from shutil import rmtree
from os import path

# Custom
from log import Log

class Configuration():
    def __init__(self):
        self.log = Log()

    def read_config(self, file_config):
        try:
            config = ConfigParser()
            config.read(file_config)

            # Read MySQL Section
            self.server = config["MySQL"]["Server"]
            self.port = config["MySQL"]["Port"]
            self.database = config["MySQL"]["DB"]
            self.user = config["MySQL"]["User"]
            self.password = config["MySQL"]["Pass"]
            self.sql_query = str(config["MySQL"]["SQL_query"])
            self.sql_count_query = str(config["MySQL"]["SQL_count_query"])

            # Read Export Section
            self.index_application_column = config["Export"]["SQL_index_application_column"]
            self.index_content_name_column = config["Export"]["SQL_index_content_name_column"]
            self.index_file_name_column = config["Export"]["SQL_index_file_name_column"]
            self.index_binary_column = config["Export"]["SQL_index_binary_column"]
            self.export_path = config["Export"]["Export_path_from_db"]
            self.error_del_files = config["Export"]["Error_delete_files"].lower()

            # Read XML Section
            self.change_xml = config["XML"]["Change_xml_file"].lower()
            self.change_xml_utf8 = config["XML"]["Change_xml_utf8"].lower()
            self.change_xml_inside = config["XML"]["Chagne_xml_inside"].lower()
            self.change_inside_xml_src = config["XML"]["Change_xml_inside_src"]
            self.change_inside_xml_desc = config["XML"]["Change_xml_inside_desc"]
            self.convert_xml_to_html = config["XML"]["Convert_xml_to_html"].lower()
            self.xslt_path = config["XML"]["XSLT_path"]
            
        except AttributeError as err:
            self.log.error(f"Config Error: {err}")
        
        except UnicodeDecodeError as err:
            self.log.error(f"Config Error: {err}")

        except MissingSectionHeaderError as err:
            self.log.error(f"Config Error: {err}")
        
        except KeyError as err:
            self.log.error(f"Config Error: {err}")

        except UnboundLocalError as err:
            self.log.error(f"Config Error: {err}")
        
        except:
            print(exc_info()[1])
            self.log.error(exc_info()[1])

        finally:
            pass

    def get_server_params(self):
        try:
            server = self.server
            port = self.port
            db = self.database
            user = self.user
            password = self.password
            sql_query = self.sql_query
            sql_count_query = self.sql_count_query
            index_application_column = self.index_application_column
            index_file_name_column = self.index_file_name_column

        except AttributeError as err:
            self.log.error(f"Config Error: {err}")

        except:
            print(exc_info()[0])
            self.log.error(exc_info()[0])

        finally:     
            return {
                    "server":server,
                    "port":port,
                    "db":db,
                    "user":user,
                    "pass":password,
                    "sql_query":sql_query,
                    "sql_count_query":sql_count_query,
                    "index_application_column":index_application_column,
                    "index_file_name_column":index_file_name_column
                    }

    def get_export_params(self):
        try:
            index_application_column = self.index_application_column
            index_content_name_column = self.index_content_name_column
            index_file_name_column = self.index_file_name_column
            index_binary_column = self.index_binary_column
            export_path = self.export_path
            error_del_files = self.error_del_files
            change_xml = self.change_xml
            change_xml_utf8 = self.change_xml_utf8
            change_xml_inside = self.change_xml
            change_inside_xml_src = self.change_inside_xml_src
            change_inside_xml_desc = self.change_inside_xml_desc
            convert_xml_to_html = self.convert_xml_to_html
            xslt_path = self.xslt_path

            return {          
                    "index_application_column":index_application_column,
                    "index_content_name_column":index_content_name_column,
                    "index_file_name_column":index_file_name_column,
                    "index_binary_column":index_binary_column,
                    "export_path":export_path,
                    "error_del_files":error_del_files,
                    "change_xml":change_xml,
                    "change_xml_utf8":change_xml_utf8,
                    "change_xml_inside":change_xml_inside,
                    "change_inside_xml_src":change_inside_xml_src,
                    "change_inside_xml_desc":change_inside_xml_desc,
                    "convert_xml_to_html":convert_xml_to_html,
                    "xslt_path":xslt_path,
                    }
            
        except AttributeError as err:
            self.log.error(f"Config Error: {err}")

        except:
            print(exc_info()[1])
            self.log.error(exc_info()[1])

        finally:
            pass

    def check_config(self, file_config):

        default_cfg = """[MySQL]
# Serwer
Server = localhost
# Port
Port = 3306
# Baza
DB = something
# User
User = user
# Pass
Pass = pass
# SQL dla wyciągania plików - posortowane po id
SQL_query = SELECT id, content, filename, binarydata FROM base.table where id in ('xxxx123', 'xyz123', 'xxx124', 'xyz124')
# Liczenie plikow dla wnioskow - w tym wpisie nie moze byc znakow: ""
SQL_count_query = SELECT id, count(id) from base.table where id = "{current_row_id}"

[Export]
# Kolumna ID (Nr wniosku) z zapytania (od 0)
SQL_index_application_column = 0
# Kolumna content z zapytania
SQL_index_content_name_column = 1
# Kolumna File_Name z zapytania
SQL_index_file_name_column = 2
# Kolumna Binary z zapytania
SQL_index_binary_column = 3
# Ścieżka do exportu plików
Export_path_from_db = d:\skrypty\MySQL-Export
# Usuń i pobierz jeszcze raz pliki w przypadku jakiegoś błędu per wniosek
Error_delete_files = True

[XML]
# Zmiany w pliku xml
Change_xml_file = True
# Konwertuj do HTML
Covnert_xml_to_html = True
# Lokalizacja pliku XSLT
XSLT_path = D:\\Skrypty\\MySQL-Export\\test.xsl
# Zamiana utf16 na utf8
Change_xml_utf8 = True
# Zmiana w pliku xml
Change_xml_inside = True
# Źródło zmiany w pliku xml
Change_xml_inside_src = href="xxx/test2.xsl"
# Docelowa zmiana w pliku xml
Change_xml_inside_desc = href="xxx/test.xsl" """

        try:
            open(file_config)

        except IOError:
            err = "Config Error: Not found config.ini or is demaged !"
            print(err)
            self.log.error(f"{err}")

            if(path.isfile(file_config)):
                rmtree(file_config)
                self.log.warning("Removed config.ini")
 
            with open(file_config, mode="w", encoding="ansii") as default_config:
                default_config.write(default_cfg)
                default_config.close()
                
            self.log.warning("Created default config.ini")
            self.log.warning("Complete the config.ini")

        except KeyError as err:
            print(err)
            self.log.error(f"Config Error: {err}")

        except:
            print(exc_info()[1])
            self.log.error(exc_info()[1]) 

        finally:
            pass

    def __del__(self):
        pass
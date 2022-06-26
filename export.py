from os import path
from os import listdir
from pathlib import Path
from shutil import rmtree
from sys import exc_info

from log import Log
from file_repack import Repack

class Export():
    def __init__(self) -> None:
        self.log = Log()
        self.repack = Repack()

    def execute_export(self, save_path, filedata, filename, current_row_id, content_name, file_extension, change_xml, change_xml_params):
        convert_to_html = change_xml_params["convert_to_html"]
        xml = "xml"

        if(filedata == bytes("Null - The database file was empty", "utf-8")):
            name_of_file = f"{save_path}\\{current_row_id}\\{current_row_id}_{content_name}.{file_extension}.txt"
        else:
            name_of_file = f"{save_path}\\{current_row_id}\\{current_row_id}_{content_name}.{file_extension}.gz"

        self.repack.write_file(filedata, name_of_file)

        if((xml in filename) and (change_xml == "true")):
            content = self.repack.change_xml(f"{save_path}\\{current_row_id}\\{current_row_id}_{content_name}", change_xml_params)
            if(convert_to_html == "true"):
                self.repack.convert_to_html(f"{save_path}\\{current_row_id}\\{current_row_id}_{content_name}", content, change_xml_params)

    def pack_export(self, export_config, record, record_count):
        index_application_column = int(export_config["index_application_column"])
        index_content_name_column = int(export_config["index_content_name_column"])
        index_file_name_column = int(export_config["index_file_name_column"])
        index_binary_column = int(export_config["index_binary_column"])
        error_del_files = export_config["error_del_files"]
        change_xml = export_config["change_xml"]
        exp_path = export_config["export_path"]

        change_xml_params = export_config

        previous_row_id = None
        previous_content_name = None
        file_skipped = 0
        file_archived = 0
        application_archived = 0
        application_skipped = 0
        reset_count_duplicates = 1

        try:
            for row in record:
                # get values from SQL results
                current_row_id = row[index_application_column]
                content_name = row[index_content_name_column]
                current_filename = row[index_file_name_column]
                filedata = row[index_binary_column]
                last_row_id = record[-1][index_binary_column]

                export_path = f"{exp_path}\\{current_row_id}"
                current_file_extensions = current_filename.split(".",1)[1]

                if(filedata == None):
                    filedata = "Null - The database file was empty"
                    filedata = bytes(filedata, "utf-8")

                if((previous_row_id != None) and (previous_row_id != current_row_id)):
                    if(skipped != True):
                        self.log.info(f"Archive {previous_row_id} completed")
                        application_archived += 1
                        reset_count_duplicates = 1
                    
                    elif(skipped == True):
                        application_skipped += 1
                        reset_count_duplicates = 1

                if((previous_row_id == None) or (previous_row_id != current_row_id)):
                    for count_row in record_count:
                        current_count_row_id = count_row[0]         # check if app number count = app number

                        if(current_count_row_id == current_row_id):
                            current_count_row = count_row[1]     # app number count - tab[[app_number, count_app_number], [... , ...]]
                            print("------------------------------")
                            print(f"Found files:", current_count_row, "for", current_row_id)

                            self.log.info(f"Found files: {current_count_row} for {current_row_id}")
                            self.log.info(f"Check directory: {export_path}\\{current_row_id}")
                    
                if(previous_content_name == content_name):          # In database filename are duplicated
                    content_name_2 = f"{content_name}_{reset_count_duplicates}"
                    print(content_name_2)
                    reset_count_duplicates += 1

                else:
                    content_name_2 = content_name

                print("ID =", current_row_id)
                print(f"Filename = {current_row_id}_{content_name_2}.{current_file_extensions}")

                if(path.isdir(f"{export_path}\\{current_row_id}") == True):     # check exist
                    id_path = f"{export_path}\\{current_row_id}"
                    dir_listing = listdir(id_path)
                    count_files = 0
                    for file in dir_listing:                    # validation of previous exports
                        valid_xml = Path(file).suffixes
                        if(valid_xml[0] == ".html"):
                            pass

                        else:
                            count_files += 1

                    if(count_files == current_count_row):
                        if(previous_row_id != current_row_id):
                            self.log.info(f"Directory exist: {id_path} - Inside: {count_files} files")
                            self.log.info(f"Skipping save: {current_row_id}_{content_name_2}.{current_file_extensions}.gz")

                            file_skipped += 1
                            skipped = True

                        elif(previous_row_id == current_row_id):
                            self.log.info(f"Skipping save: {current_row_id}_{content_name_2}.{current_file_extensions}.gz")
                            file_skipped += 1
                            skipped = True

                    elif(count_files != current_count_row):
                        self.log.warning("Different number of files in the directory")
                        if(error_del_files == "true"):
                            if(previous_row_id != current_row_id):
                                rmtree(id_path)

                                self.log.warning(f"Remove directory: {export_path}\\{current_row_id}\\{current_row_id}")
                                self.log.warning("Save files again")
                                self.execute_export(export_path, filedata, current_filename, current_row_id, content_name_2, current_file_extensions, change_xml, change_xml_params)

                                file_archived += 1
                                skipped = False

                            elif(previous_row_id == current_row_id):
                                self.execute_export(export_path, filedata, current_filename, current_row_id, content_name_2, current_file_extensions, change_xml, change_xml_params)

                                file_archived += 1
                                skipped = False

                        elif(error_del_files != "true"):
                            if(previous_row_id != current_row_id):
                                self.log.warning(f"Directory exist: {export_path}\\{current_row_id} - Inside: {count_files} files")
                                self.log.info(f"Skipping save: {current_row_id}_{content_name_2}.gz")

                                file_skipped += 1
                                skipped = True
                            
                            elif(previous_row_id == current_row_id):
                                self.log.info(f"Skipping save: {current_row_id}_{content_name_2}.gz")

                                file_skipped += 1
                                skipped = True

                    else:
                        self.execute_export(export_path, filedata, current_filename, current_row_id, content_name_2, current_file_extensions, change_xml, change_xml_params)
                        file_archived += 1
                        skipped = False

                elif(path.isdir(f"{export_path}\\{current_row_id}") == False):
                    Path(f"{export_path}\\{current_row_id}").mkdir(parents=True, exist_ok=True)

                    self.log.info(f"Created directory: {export_path}\\{current_row_id}")
                    self.execute_export(export_path, filedata, current_filename, current_row_id, content_name_2, current_file_extensions, change_xml, change_xml_params)

                    file_archived += 1
                    skipped = False

                previous_row_id == current_row_id
                previous_content_name == content_name

                if(last_row_id == filedata):
                    if(previous_row_id != None):
                        if(skipped != True):
                            self.log.info(f"Archive {current_row_id} completed")
                            application_archived += 1
                            reset_count_duplicates = 1

                        elif(skipped == True):
                            application_skipped += 1
                            reset_count_duplicates = 1

        except FileNotFoundError as err:
            self.log.error(err)
            self.log.warning("Check directory which is before directory with application number - If doesn't exist just create it.")
            print(err)
        
        except:
            print(exc_info()[1])
            self.log.error(exc_info()[1])

            del_path = Path(export_path)
            rmtree(export_path)

            self.log.error(f"Delete directory {export_path}")
            print("Error with download package")

        finally:
            self.log.info("End export")

            return [application_skipped, file_skipped, application_archived, file_archived]

    def __del__(self) -> None:
        del self.log
        del self.repack
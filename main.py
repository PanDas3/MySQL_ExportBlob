from sys import exc_info

# Custom
from file_repack import Repack
from config import Configuration
from base import DataBase
from log import Log

if __name__ == "__main__":
    
    # New instance class
    log = Log()
    base = DataBase()
    cfg = Configuration()
    files = Repack()

    log.info("##### Start Application #####")

    file_config = "config.ini"
    print("##########################")
    print("### Powered by Majster ###")
    print("##########################\n")

    # Execute script
    try:
        cfg.check_config(file_config)                                               # Checking if not exist - create it
        cfg.read_config(file_config)                                                # Read config
        connect_config = cfg.get_server_params()                                    # Get sql connection params    
        export_config = cfg.get_export_params()                                     # Get export params

        base.open_connection(connect_config)                                        # Connect to database
        querry = base.exec_export_rows_querry()                                     # Execute select -> return tab with row
        archive_count_rows = base.exec_count_files(querry)                          # Exectue select count from tab with row -> return result how many application and files

        log.found_export(archive_count_rows[0], archive_count_rows[1])              # Write found result to log
        result = files.pack_export(export_config, querry, archive_count_rows[2])    # Save filedata from database to file -> return result successed export
        log.result_export(result)                                                   # Write result export to log

        base.close_connection()                                                     # Close connect database

    except:
        if(type(exc_info()[1]) != SystemExit):
            print(exc_info()[1])
            log.error(exc_info()[1]) 

    finally:
        log.info("##### End Application #####\n")
        input("Press Enter to continue...")

        # Del instance class
        del log
        del base
        del cfg
        del files
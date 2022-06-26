from logging import getLogger
from logging import basicConfig
from logging import error
from logging import info
from logging import warning
from logging import ERROR
from logging import INFO
from logging import WARNING

class Log():

    def __init__(self):
        pass

    def error(self, msg):
        logger = getLogger("Logger")
        logger.setLevel(ERROR)
        basicConfig(filename="MySQL_Export.log", level=ERROR, format="%(asctime)s \t %(levelname)s: %(message)s")
        error(msg)

    def info(self, msg):
        logger = getLogger("Logger")
        logger.setLevel(INFO)
        basicConfig(filename="MySQL_Export.log", level=INFO, format="%(asctime)s \t %(levelname)s: \t\t %(message)s")
        info(msg)

    def warning(self, msg):
        logger = getLogger("Logger")
        logger.setLevel(WARNING)
        basicConfig(filename="MySQL_Export.log", level=WARNING, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        warning(msg)

    def found_export(self, application, files):
        
        self.info("-----------------------")
        self.info("Application found: " + str(application))
        self.info("Files found: " + str(files))
        self.info("-----------------------")

    def result_export(self, result):
        application_skipped = result[0]
        file_skipped = result[1]
        application_archived = result[2]
        file_archived = result[3]
        
        self.info("-----------------------")
        self.info("Skipped application: " + str(application_skipped))
        self.info("Skipped files: " + str(file_skipped))
        self.info("Archived application: " + str(application_archived))
        self.info("Archived files: " + str(file_archived))
        self.info("-----------------------")
    
    def __del__(self):
        pass
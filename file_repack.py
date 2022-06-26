import lxml.etree as ET
from gzip import open as gz_open
from os import remove

# Custom
from log import Log

class Repack():
    def __init__(self):
        self.log = Log()

    def write_file(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

        self.log.info(f"Save file: {filename}")

    def convert_to_html(self, filename, content, change_xml_params):
        xslt_path = change_xml_params["xslt_path"]

        with open(f"{filename}.xml", "wt", encoding="utf8") as file_out:
            file_out.write(content)
            self.log.info(f"\tSave tmp file: {filename}.xml")
            file_out.close()

        dom = ET.parse(f"{filename}.xml")
        xslt = ET.parse(xslt_path)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        self.log.info(f"\t Transofrm xml and xslt to HTML")

        with gz_open(f"{filename}.html.gz", "wb") as zipp_html:
            zipp_html.write(ET.tostring(newdom, pretty_print=True))
            self.log.info(f"\tZipping HTML: {filename}.html.gz")
            zipp_html.close()

        remove(f"{filename}.xml")
        self.log.info(f"\tDelete tmp file: {filename}")

    def change_xml(self, filename, change_xml_params):
        change_utf8 = change_xml_params["change_xml_utf8"]
        change_xml_inside = change_xml_params["change_xml_inside"]
        change_inside_xml_src = change_xml_params["change_inside_xml_src"]
        change_inside_xml_desc = change_xml_params["change_inside_xml_desc"]

        self.log.info(f"\tRead file: {filename}.xml.gz")

        with gz_open(f"{filename}.xml.gz", "r+") as file_in:
            filedata = file_in.read().decode("utf-8")
            file_in.close()

        if((change_inside_xml_src in filedata) and (change_xml_inside == "true")):
            filedata = filedata.replace(change_inside_xml_src, change_inside_xml_desc)
            self.log.info(f"\tReplace {change_inside_xml_src} to {change_inside_xml_desc}")

        if(("utf-16" in filedata) and (change_utf8 == "true")):
            filedata = filedata.replace("utf-16", "utf-8")
            self.log.info(f"\tReplace UTF-16 to UTF-8")

        content = filedata
        with gz_open(f"{filename}.xml.gz", "wt", encoding="utf8") as zipp:
            zipp.write(content)
            self.log.info(f"\tZipping file: {filename}.xml.gz")
            zipp.close()

        return content

    def __del__(self) -> None:
        del self.log
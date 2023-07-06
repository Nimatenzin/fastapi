import xmltodict
import json

def process_xml_data(xml_data):
    try:
        parsed_data = xmltodict.parse(xml_data)


        return {
            "status": "Ok",
            "code": "200",
            "message": "XML processing successful",
            "result": parsed_data
        }
    except Exception as e:
        return {
            "status": "Error",
            "code": "500",
            "message": "XML processing failed: " + str(e)
        }
    

def process_json_data(json_data):
    try:
        # Convert JSON to ordered dictionary
        ordered_dict = json.loads(json_data)

        # Convert ordered dictionary to XML
        xml_data = xmltodict.unparse(ordered_dict, pretty=True)

        return {
            "status": "Ok",
            "code": "200",
            "message": "JSON to XML conversion successful",
            "result": xml_data
        }
    except Exception as e:
        return {
            "status": "Error",
            "code": "500",
            "message": "JSON to XML conversion failed: " + str(e)
        }
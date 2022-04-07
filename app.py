from flask import Flask, jsonify, request
from flask_accept import accept
import xml.etree.ElementTree as ET
import yaml

app = Flask(__name__)

@app.route('/api')
@accept('application/json')
def currentIp_endpoint():
    return jsonify({'Current Ip':request.remote_addr})

@currentIp_endpoint.support('text/plain')
def currentIp_endpoint_text():
    ip = request.remote_addr
    return ip

@currentIp_endpoint.support('text/html')
def currentIp_endpoint_html():

    output = "<p>" + request.remote_addr + "<p>"

    return output

@currentIp_endpoint.support('text/yaml')
def currentIp_endpoint_yaml():

    current_Ip = [request.remote_addr]
    output = yaml.dump(current_Ip, explicit_start=True, default_flow_style=False)

    return app.response_class(output, mimetype='text/yaml')

@currentIp_endpoint.support('application/xml')
def currentIp_endpoint_xml():
    root = ET.Element('current_Ip')

    usr = ET.SubElement(root, "usr")
    usr.text = request.remote_addr

    tree = ET.ElementTree(root)

    return app.response_class(ET.tostring(root), mimetype='application/xml')

if __name__ == '__main__':
    app.run()
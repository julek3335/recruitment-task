from flask import Flask, jsonify, request, render_template
from flask_accept import accept
import xml.etree.ElementTree as ET
import yaml

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    ENV = 'develop'
)

@app.route('/')
def home():
    return render_template("index.html")

# a list that stores the IP addresses of clients who have used the application in the past 
ip_log = []

# routing handling current IP
@app.route('/currentIP')
@accept('application/json')
def currentIp_endpoint():
    ip_log.append(request.remote_addr)
    return jsonify({'Current Ip':request.remote_addr})

@currentIp_endpoint.support('text/plain')
def currentIp_endpoint_text():
    ip = request.remote_addr
    ip_log.append(ip)
    return app.response_class(ip, mimetype='text/plain')

@currentIp_endpoint.support('text/html')
def currentIp_endpoint_html():
    ip_log.append(request.remote_addr)
    output = "<p>" + request.remote_addr + "<p>"

    return app.response_class(output, mimetype='text/html')

@currentIp_endpoint.support('text/yaml')
def currentIp_endpoint_yaml():
    ip_log.append(request.remote_addr)
    current_Ip = [request.remote_addr]
    output = yaml.dump(current_Ip, explicit_start=True, default_flow_style=False)

    return app.response_class(output, mimetype='text/yaml')

@currentIp_endpoint.support('application/xml')
def currentIp_endpoint_xml():
    ip_log.append(request.remote_addr)
    root = ET.Element('current_Ip')

    usr = ET.SubElement(root, "usr")
    usr.text = request.remote_addr

    tree = ET.ElementTree(root)

    return app.response_class(ET.tostring(root), mimetype='application/xml')

# routing handling clients IP adresses that used app in the past
@app.route('/history')
@accept('application/json')
def history_endpoint():
    
    return jsonify({'visitors':ip_log})


@history_endpoint.support('text/plain')
def history_endpoint_text():
    return app.response_class(' '.join([str(elem) for elem in ip_log]), mimetype='text/plain')


@history_endpoint.support('text/html')
def history_endpoint_html():
    output = ''
    for adress in ip_log:
        output += "<p>" + adress + "<p>"

    return output


@history_endpoint.support('text/yaml')
def history_endpoint_yaml():
    output = yaml.dump(ip_log, explicit_start=True, default_flow_style=False)

    return app.response_class(output, mimetype='text/yaml')


@history_endpoint.support('application/xml')
def history_endpoint_yaml():
    root = ET.Element('visitors')

    for ip in ip_log:
        user = ET.SubElement(root, "user")
        user.text = ip


    tree = ET.ElementTree(root)

    return app.response_class(ET.tostring(root), mimetype='application/xml')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
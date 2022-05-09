from flask import Flask, jsonify, request, render_template
from flask_accept import accept
import xml.etree.ElementTree as ET
import yaml
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db
from models.IpAdresses import IpAdresses
from models import ma

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    ENV = 'develop',
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db",
    SQLALCHEMY_ECHO = True,
    SQLALCHEMY_TRACK_MODIFICATION = True
)

db.app = app
db.init_app(app)
ma.init_app(app)



# limiter limits the number of queries for each client
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[ "100 per minute", "2 per second"]
)


def write_to_db(ip):
    ip = IpAdresses(ip)
    ip.db_save()



@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")


# routing handling current IP
@app.route('/currentIP')
@accept('text/json')
def currentIp_endpoint():
    client_ip = request.access_route[0]
    write_to_db(client_ip)

    return jsonify({'Current Ip':client_ip})

@currentIp_endpoint.support('text/plain')
def currentIp_endpoint_text():
    client_ip = request.access_route[0]
    write_to_db(client_ip)

    return app.response_class(client_ip, mimetype='text/plain')

@currentIp_endpoint.support('text/html')
def currentIp_endpoint_html():
    client_ip = request.access_route[0]
    write_to_db(client_ip)

    return app.response_class("<p>" + client_ip + "<p>", mimetype='text/html')

@currentIp_endpoint.support('text/yaml')
def currentIp_endpoint_yaml():
    client_ip = request.access_route[0]
    write_to_db(client_ip)

    output = yaml.dump([client_ip], explicit_start=True, default_flow_style=False)

    return app.response_class(output, mimetype='text/yaml')

@currentIp_endpoint.support('text/xml')
def currentIp_endpoint_xml():
    client_ip = request.access_route[0]
    write_to_db(client_ip)

    root = ET.Element('current_Ip')
    usr = ET.SubElement(root, "usr")
    usr.text = client_ip

    return app.response_class(ET.tostring(root), mimetype='text/xml')


def query_all_ip_adresses():
    returnList = []
    query = IpAdresses.query.all()

    for row in query:
        returnList.append(row.ip)
    
    return returnList


# routing handling clients IP adresses that used app in the past
@app.route('/history')
@accept('text/json')
def history_endpoint():
    return jsonify({'visitors':query_all_ip_adresses()})


@history_endpoint.support('text/plain')
def history_endpoint_text():
    return app.response_class(' '.join([str(elem) for elem in query_all_ip_adresses()]), mimetype='text/plain')


@history_endpoint.support('text/html')
def history_endpoint_html():
    output = ''
    for adress in query_all_ip_adresses():
        output += "<p>" + adress + "<p>"

    return output


@history_endpoint.support('text/yaml')
def history_endpoint_yaml():
    output = yaml.dump(query_all_ip_adresses(), explicit_start=True, default_flow_style=False)

    return app.response_class(output, mimetype='text/yaml')


@history_endpoint.support('text/xml')
def history_endpoint_yaml():
    root = ET.Element('visitors')

    for ip in query_all_ip_adresses():
        user = ET.SubElement(root, "user")
        user.text = ip

    return app.response_class(ET.tostring(root), mimetype='text/xml')



if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
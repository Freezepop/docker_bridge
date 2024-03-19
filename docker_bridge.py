#!/usr/bin/python3

import json
import requests_unixsocket
from flask import Flask, jsonify
from gevent.pywsgi import WSGIServer


app = Flask(__name__)

static_data = {"path": {"/docker_containers_all": "containers/json?all=true",
                        "/docker_containers_not_all": "containers/json?all=false",
                        "/docker_data_usage":"system/df",
                        "/docker_images": "images/json",
                        "/docker_info": "info",
                        "/docker_ping": "_ping"}}

session = requests_unixsocket.Session()

for static_route in static_data["path"]:
    @app.route(static_route, endpoint=static_route, methods=["GET"])
    def static_routes(static_route=static_route):
        try:
            response=session.get(f"http+unix://%2Fvar%2Frun%2Fdocker.sock/{static_data['path'][static_route]}")
            if response.status_code == 200:
                if static_data['path'][static_route] == "_ping":
                    socket_data = response.text
                else:
                    socket_data = json.loads(response.text)
            else:
                socket_data="No data"
                print(f"Error: HTTP request failed with status code {response.status_code}")
        except Exception as error:
            socket_data = "No data"
            print(f"Error: Failed to fetch data - {error}")

        return jsonify({static_route: socket_data})


@app.route("/docker_container_info/<string:container_id>", methods=["GET"])
def docker_container_info(container_id):
    try:
        response=session.get(f"http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/{container_id}/json")
        if response.status_code == 200:
            socket_data=json.loads(response.text)
        else:
            socket_data="No data"
            print(f"Error: HTTP request failed with status code {response.status_code}")
    except Exception as error:
        socket_data="No data"
        print(f"Error: Failed to fetch data - {error}")

    return jsonify({f"docker_container_info_{container_id}": socket_data})


@app.route("/docker_container_stats/<string:container_id>", methods=["GET"])
def docker_container_stats(container_id):
    try:
        response=session.get(f"http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/{container_id}/stats?stream=false")
        if response.status_code == 200:
            socket_data=json.loads(response.text)
        else:
            socket_data="No data"
            print(f"Error: HTTP request failed with status code {response.status_code}")
    except Exception as error:
        socket_data="No data"
        print(f"Error: Failed to fetch data - {error}")

    return jsonify({f"docker_container_stats_{container_id}": socket_data})


if __name__ == "__main__":
    http_server=WSGIServer(("0.0.0.0", 10070), app)
    http_server.serve_forever()

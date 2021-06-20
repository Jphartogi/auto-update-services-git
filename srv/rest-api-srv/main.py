from flask import Flask,jsonify,request
import os
app = Flask(__name__)

import grpc

from version_check_pb2 import VersionCheckRequest
from version_check_pb2_grpc import VersionCheckSrvStub

version_check_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
version_check_port = os.getenv("RECOMMENDATIONS_PORT", 50051)
version_check_channel = grpc.insecure_channel(
    f"{version_check_host}:{version_check_port}"
)
client = VersionCheckSrvStub(version_check_channel)

@app.route('/check_version',methods = ['POST', 'GET'])
def check_for_update():
    if not request.is_json:
        return jsonify(message="Missing JSON in requests",type="DataFormatError"),400
    else:
        folder_location = request.json.get('folder_location')
        request_id = request.json.get('request_id')
        token = request.json.get('token')

        if folder_location == None or folder_location == "":
            return jsonify(message="Folder location is required!",type="MissingRequiredDataError"),400

        version_check_request = VersionCheckRequest(
            folder_location=str(folder_location),
            request_id=1,
            request_token="abc"
        )
        try:
            response = client.VersionCheck(
                version_check_request
            )
        except Exception as e:
            print(e)
            return jsonify(message="Internal Server Error"),500
            
        return jsonify(
            current_version=response.current_version,
            latest_version=response.latest_version,
            need_upgarde=response.need_upgrade
        )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3123)

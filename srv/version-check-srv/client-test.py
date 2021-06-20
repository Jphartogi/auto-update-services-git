import grpc
from version_check_pb2_grpc import VersionCheckSrvStub
from version_check_pb2 import VersionCheckRequest

channel = grpc.insecure_channel("localhost:50051")
client = VersionCheckSrvStub(channel)
request = VersionCheckRequest(
    folder_location="/Users/jphartogi/Documents/qlue/auto_update/test-repo",
    request_id=1,
    request_token="abc"
)
result = client.VersionCheck(request)
if result.need_upgrade:
    print(f"you need to upgrade the software to latest version {result.latest_version}, because you are still in {result.current_version}")
else:
    print(f"all good, no need to upgrade the version. Current version {result.current_version}")

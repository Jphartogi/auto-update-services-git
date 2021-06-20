from git import Repo
from dotenv import load_dotenv
import os
from concurrent import futures

load_dotenv()

import grpc
from version_check_pb2 import (
    VersionCheckResponse
)
import version_check_pb2_grpc 
SERVICES_PORT=os.getenv("SERVICES_PORT")

class VersionCheckServices(
    version_check_pb2_grpc.VersionCheckSrvServicer
):
    def __init__(self) -> None:
        super().__init__()
        self.repo_path = os.getenv("REPO_PATH")
        self.folder_path = None

    def VersionCheck(self, request, context):
        if request.folder_location == None or request.folder_location == "":
            context.abort(grpc.StatusCode.NOT_FOUND, "Folder Location must be filled")

        self.folder_path = request.folder_location

        if self.app_is_current(self.folder_path):
            # if the app is latest version
            print(f"Your app is in latest version {self.get_current_tags(self.folder_path)}")
            return VersionCheckResponse(
                latest_version=str(self.get_current_tags(self.folder_path)),
                current_version=str(self.get_tag_info(self.folder_path)['latest_tag']['name']),
                need_upgrade=False)
        else:
            # if there is newer software from remote origin
            print(f"There is an software update available at version {self.get_tag_info(self.folder_path)['latest_tag']['name']}, \nwhile your current software version is {self.get_current_tags(self.folder_path)}")
            return VersionCheckResponse(
                latest_version=str(self.get_current_tags(self.folder_path)),
                current_version=str(self.get_tag_info(self.folder_path)['latest_tag']['name']),
                need_upgrade=True)

    def app_is_current(self,folder_path):
        local_repo = Repo(path=folder_path)
        remote_repo = local_repo.remote()
        local_commit = local_repo.commit()

        # We don't want to upgrade if the local commit is newer than the remote commit (IE - we're doing development
        # on the local copy)
        remote_fetch = remote_repo.fetch()
        remote_commit = remote_fetch[0].commit
        return remote_commit.committed_datetime <= local_commit.committed_datetime 

    def get_current_tags(self,folder_path):
        repo = Repo(path=folder_path)
        return next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)

    def get_tag_info(self,folder_path):
        local_repo = Repo(path=folder_path)

        # Fetch remote branches to ensure we are up to date
        for remote in local_repo.remotes:
            remote.fetch()

        tags = []
        latest_tag = None
        for this_tag in local_repo.tags:
            tag_data = {'name': this_tag.name, 'committed_datetime': this_tag.commit.committed_datetime,
                        'hexsha': this_tag.commit.hexsha}
            if latest_tag is None:
                latest_tag = tag_data
            elif latest_tag['committed_datetime'] < tag_data['committed_datetime']:
                latest_tag = tag_data
            tags.append(tag_data)

        return {'latest_tag': latest_tag, 'all_tags': tags}


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    version_check_pb2_grpc.add_VersionCheckSrvServicer_to_server(
        VersionCheckServices(), server
    )
    server.add_insecure_port(f"[::]:{SERVICES_PORT}")
    server.start()
    print(f"Starting microservices server at port {SERVICES_PORT}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    

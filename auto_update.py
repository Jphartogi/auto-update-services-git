from git import Repo
from dotenv import load_dotenv
import os

load_dotenv()
REPO_PATH = os.getenv("REPO_PATH")


def app_is_current(tagged_commits_only=False, branch_to_check=None):
    local_repo = Repo(path=REPO_PATH)
    remote_repo = local_repo.remote()
    local_commit = local_repo.commit()
    if tagged_commits_only:
        # Functionality no longer exists, but leaving the code in case we reenable it later. This should generally never
        # be reached.
        tags = get_tag_info()
        return tags['latest_tag']['committed_datetime'] <= local_commit.committed_datetime
    else:
        # We don't want to upgrade if the local commit is newer than the remote commit (IE - we're doing development
        # on the local copy)
        remote_fetch = remote_repo.fetch()
        remote_commit = remote_fetch[0].commit
        return remote_commit.committed_datetime <= local_commit.committed_datetime 

def get_current_tags():
    repo = Repo(path=REPO_PATH)
    return next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)

def get_tag_info():
    local_repo = Repo(path=REPO_PATH)

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

if __name__ == "__main__":
    # check whether the app is in latest version with remote
    if app_is_current():
        # if the app is latest version
        print(f"Your app is in latest version {get_current_tags()}")
    else:
        # if there is newer software from remote origin
        print(f"There is an software update available at version {get_tag_info()['latest_tag']['name']}, \nwhile your current software version is {get_current_tags()}")

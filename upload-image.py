import base64
import json
import random

import requests
import os.path
import sys
import time

import config


class GiteaUploader:
    def __init__(self):
        self.protocol = config.protocol
        self.domain = config.domain
        self.port = config.port
        self.owner = config.owner
        self.repo = config.repo
        self.branch = config.branch
        self.filepath = config.filepath
        self.token = config.token
        self.headers = {'content-type': 'application/json'}

    def get_url(self, filepath):
        return "{protocol}://{domain}:{port}/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={token}" \
            .format(protocol=self.protocol, domain=self.domain, port=self.port, owner=self.owner, repo=self.repo,
                    filepath=filepath, token=self.token)

    def get_random_filename(self, image):
        rand = random.randint(1, 1000)

        # 自定义文件名称
        filename = os.path.basename(image)
        suffix = "." + filename.split(".")[1]
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + "%04d" % rand + suffix

        # 设置上传文件在gitea上的路径
        return self.filepath + filename

    def upload(self, image):
        filepath = self.get_random_filename(image)

        # 获取文件的base64
        with open(image, 'rb') as f:
            file_date = f.read()
        base64_str = base64.b64encode(file_date)
        base64_str = base64_str.decode('utf-8')

        response = requests.request(
            method='POST',
            url=self.get_url(filepath),
            headers=self.headers,
            json={
                "branch": self.branch,
                "content": base64_str,
                "message": "Upload by Typora",
            },
        )

        if response.ok:
            result = json.loads(response.text)
            return result["content"]["download_url"]
        return None

    def run(self, args):
        print("Upload Success:")
        for image in args[1:]:
            remote_url = self.upload(image)
            if remote_url:
                print(remote_url)


if __name__ == '__main__':
    gitea = GiteaUploader()
    gitea.run(sys.argv)

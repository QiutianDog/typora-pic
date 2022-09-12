# typora-pic
Typora auto update image to online, Custome a Gitea Server as Pic

## 背景

在使用 Typora 编写 markdown 的时候，如果需要用到图片，默认是使用本地路径，如此一来，就无法在网络上查看md文档的图片，因此Typora提供了快捷的上传图片接口，可以在粘入图片的时候，自动上传图片到指定服务器，并且将路径更换成url。

![image-20220912163600066](http://tencent.qiutiandog.fun:3000/Qiutian_Dog/uPic/raw/branch/main/uPic/202209121642380264.png)

并且上传服务提供了多种第三方工具。

![image-20220912164539048](http://tencent.qiutiandog.fun:3000/Qiutian_Dog/uPic/raw/branch/main/uPic/202209121645390301.png)

在试用了各种第三方工具之后，发现大都数的图云都是使用云存储（七牛云，阿里云OSS）和GIt（GitHub，Gitee）。从经济上来说，使用Gitee和Github无疑是最好的选择，但是存在被封仓库的风险。所以我选择自建Gitea作为图云，问题就是找了一圈都没有发现支持Gitea图云的软件，所以我决定使用Typora提供的接口自己用python来对接Gitea。

## 环境准备

* Docker（云服务器用于部署Gitea）
* Gitea（部署在云服务器中）
* Python3（本地环境调用脚本）

### Gitea

在云服务器中部署Gitea，寻找一个空文件夹，比如 ~/Document/Project/

```bash
mkdir -p ~/Document/Project/
cd ~/Document/Project/
```

1. 下载docker-compose.yml

```bash
git clone https://github.com/QiutianDog/typora-pic.git
```

2. 利用 docker-compose 部署 Gitea

```bash
# 一定要进入文件夹
cd typora-pic/Docker
# 启动 Gitea
docker-compose up -d
```

3. 进入启动页自行配置 http://x.x.x.x:3000/

创建一个用户，并且创建一个仓库，进行一次初次提交，为的是生成main分支。

## 使用

首先要在本地环境安装好python3，并且下载脚本。

```bash
git clone https://github.com/QiutianDog/typora-pic.git
```

修改config,py文件的配置。

* domain：服务器的域名或者公网IP
* port：Gitea服务器端口号，如果没有改之前的docker-compose，默认就是3000
* owner：就是你注册的Gitea用户名，不是邮箱
* repo：之前创建的远程仓库名称
* branch：分支名称
* filepath：就是你的图片文件会上传到仓库的哪个位置
* token：利用Gitea生成的 用户令牌

```ini
# Gitea config

# http or https
protocol = "http"

# ip address or domain
domain = ""

# port default 3000
port = 3000

# your gitea username
owner = ""

# your gitea repo name
repo = ""

# your gitea repo branch, default "master"
branch = "master"

# where your file upload to repo filepath
filepath = "uPic/"

# your gitea Access Token
token = ""
```

其中 token 为 Gitea 的用户令牌，访问 http://x.x.x.x:3000/，登陆用户后，在用户设置，应用，生成 Access Token。

![image-20220912174556338](http://tencent.qiutiandog.fun:3000/Qiutian_Dog/uPic/raw/branch/main/uPic/202209121745560769.png)

复制生成的 token 到 config.py 中。

![image-20220912174627284](http://tencent.qiutiandog.fun:3000/Qiutian_Dog/uPic/raw/branch/main/uPic/202209121746270421.png)

### Typroa配置

在 首选项 -> 图片 中，选择插入图片时上传图片，并且勾选适用于本地图片。

在下方，选择上传图片方式为命令行。

并且输入

```bash
python 本地存放的路径/typora-pic/upload-image.py
```

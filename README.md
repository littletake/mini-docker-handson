# コンテナ型仮想環境の実装
コンテナ型仮想化を実装することで仮想化に関する理解を深める。
プロセスを隔離しその中で簡単なコマンドを実行するところまでを作成した。

## セットアップ
### vagrantのインストール
https://www.vagrantup.com/downloads

### VMの作成と起動
```bash
vagrant up
vagrant ssh
```

### VMの動作確認
以下の動作確認はVM内で実施した。  
`vagrant ssh`でVirtualBox上の仮想環境に移動できる。

#### OSの確認

```bash
cat /etc/os-release

# --->
# NAME="Ubuntu"
# VERSION="20.10 (Groovy Gorilla)"
# ID=ubuntu
# ID_LIKE=debian
# PRETTY_NAME="Ubuntu 20.10"
# VERSION_ID="20.10"
```

#### コマンドの確認
コマンドは`mini-docker`に実装した。  
システムコールを用いるため、特権ユーザーで実行する。

```bash
sudo su -
cd /vagrant
```

- イメージの取得

```bash
./mini-docker pull <取得したいDockerイメージ名>

# ---> 
# pulling <registry名>/<image名>:<tag名> ...
# Fetching manifest for <image名>:<tag名>
# Fetching layer: sha256:hogehoge
# Fetching layer: sha256:hugahuga
# 👌 Docker image <image名>:<tag名> has been stored in /var/opt/app/images/library_<image名>_<tag名>
```

- 取得したイメージの一覧取得
```bash
./mini-docker images
# ---> 
# fetching images
# +-------------------+---------+---------+---------------+
# | name              | version | size    | path          |
# +-------------------+---------+---------+---------------+
# | library/<image>   | <tag>   | <size>  | <path>        |
# +-------------------+---------+---------+---------------+
```

- イメージの実行
```bash
./mini-docker run <image名> <command>
# ---> 
# parent_pid: <親プロセスのPID>
# child_pid:  <小プロセスのPID>
# <何かしらの処理>
```

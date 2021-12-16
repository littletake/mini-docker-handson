import linux
import os
from typing import Dict, Tuple

from commands.cgroup import CGroup
from commands.local import find_images
from commands.data import Container


def exec_cmd_in_child(option: Dict):
    _pid = os.getpid()
    print(f'child_pid: {_pid}')

    if option["cpu"]:
        cgroup = CGroup("child_group")
        cgroup.set_cpu_limit(option["cpu"])
        cgroup.add(_pid)

    change_hostname("child")

    # ルートディレクトリを変更
    container: Container = option["container"]
    os.chroot(container.root_dir)
    os.chdir("/")

    # 小プロセス内での処理
    commands = option["commands"]
    os.execvp(
        commands[0],
        commands,
    )
    # 上記の処理がプロセスを置き換えるためそれ以降の処理がなされない


def change_hostname(name: str):
    print("set hostname: {}".format(name))
    linux.sethostname(name)


def exec_run(
        commands: Tuple,
        cpu: float,
        image_name: str):

    _pid = os.getpid()
    print(f'parent_pid: {_pid}')

    # イメージの選択
    # TODO: プル済みかどうかを調べる条件分岐を作成
    _image = find_images()

    # コンテナの作成（マウント先のディレクトリ作成）
    _container = Container.init_from_image(_image[0])

    # マウント
    linux.mount(
        "overlay",
        _container.root_dir,
        "overlay",
        linux.MS_NODEV,
        f"lowerdir={_image[0].content_dir},upperdir={_container.rw_dir},workdir={_container.work_dir}"
    )

    # 小プロセスでの処理
    _flags = linux.CLONE_NEWUTS
    option = {
        "commands": commands,
        "container": _container,
        "cpu": cpu,
        "image": _image
    }

    # linux.clone: 子プロセスの作成
    child_pid = linux.clone(
        exec_cmd_in_child,
        _flags,
        (option,)
    )

    os.waitpid(
        child_pid,
        0,
    )

    # PIDの確認
    # print("parent: {}".format(os.getpid()))


def mount():
    _image = find_images()
    _container = Container.init_from_image(_image[0])
    linux.mount(
        "overlay",
        _container.root_dir,
        "overlay",
        linux.MS_NODEV,
        f"lowerdir={_image[0].content_dir},upperdir={_container.rw_dir},workdir={_container.work_dir}"
    )

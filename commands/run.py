import linux
import os
from typing import Tuple

from commands.cgroup import CGroup


def exec_cmd_in_child(*command):
    # command[0]  : シェルコマンド（str）
    # command[1:] : 関数で実行する文字列（str）

    # PIDの確認
    # print("child: {}".format(os.getpid()))
    change_hostname(command[1])

    if len(command) != 0:
        os.execvp(
            command[0],
            command,
        )
        # 上記の処理がプロセスを置き換えるためそれ以降の処理がなされない


def change_hostname(name: str):
    print("set hostname: {}".format(name))
    linux.sethostname(name)


def exec_run(command: Tuple, cpu: float):
    cgroup = CGroup("test")

    # linux.clone: 子プロセスの作成
    child_pid = linux.clone(
        exec_cmd_in_child,
        linux.CLONE_NEWUTS,
        command,
    )

    # cpuの制限
    cgroup.set_cpu_limit(cpu)
    cgroup.add(child_pid)

    os.waitpid(
        child_pid,
        0,
    )

    # PIDの確認
    # print("parent: {}".format(os.getpid()))

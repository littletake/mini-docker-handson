import linux
import os

from typing import Tuple


def print_hello(*command):
    # 第一引数：シェルスクリプトの関数
    # 第二引数：関数で実行する文字列

    # PIDの確認
    # print("child: {}".format(os.getpid()))

    if len(command) != 0:
        os.execvp(
            command[0],
            command,
        )
        # 上記の処理がプロセスを置き換えるためそれ以降の処理がなされない


def exec_run(command: Tuple):

    # linux.clone: 子プロセスの作成
    child_pid = linux.clone(
        print_hello,
        0,
        command,
    )
    os.waitpid(
        child_pid,
        0,
    )

    # PIDの確認
    # print("parent: {}".format(os.getpid()))

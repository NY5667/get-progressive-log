@echo off

REM 激活虚拟环境
call venv\Scripts\activate

REM 运行 Python 脚本
python ./user/delete_online_user.py

REM 关闭虚拟环境
REM deactivate

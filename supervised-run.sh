#!/usr/bin/env bash
python supervised.py ls \
	--mail-user=sender@example.com \
	--mail-passwd=Passwd-or-Token \
	-r reciever1@example.com \
	-r reciever2@example.com \
	--wechat-user=wechat-agent-id \
	--wechat-passwd=wechat-agent-secret \
	--log-dir=logs \
    -e "ls命令退出" \
    -e "-e 参数测试"
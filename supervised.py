import os
import sys
import socket
import logging

from collections import defaultdict
from mail.mailWrapper import EmailAgent
from wechat.wechatWrapper import quick_send_msg

is_long_flag = lambda arg: len(arg) > 3 and arg[0:2] == '--' and "=" in arg
is_short_flag = lambda arg: len(arg) == 2 and arg[0] == '-' and arg[0] != arg[1]
is_opt_flag = lambda arg: is_long_flag(arg) or is_short_flag(arg)

def getopt(argv):
    argc = len(argv)
    opt = defaultdict(list)
    if (argc < 1): return opt
    for i in range(argc):
        if(is_short_flag(argv[i])):
            if (i < argc - 1 and not is_opt_flag(argv[i+1])):
                opt[argv[i][1:]].append(argv[i+1])
                i += 1
            else:
                opt[argv[i][1:]].append("")
        elif(is_long_flag(argv[i])):
            if (i < argc):
                kv = argv[i].split("=")
                opt[kv[0][2:]].append(kv[1])
            else:
                opt[argv[i][2:]].append("")
    return opt

def help():
    print("""
    if len(sys.argv) < 2 or is_opt_flag(sys.argv[1]):
        print("note: please specify the target to supervise")
        print("    Example:%s target.exe ..."%sys.argv[0])
        return

    opt = getopt(sys.argv[2:])
    if ("h" in opt or "help" in opt):
        help()

    if "mail-user" not in opt and "wechat-user" not in opt and "log-dir" not in opt:
        print("note: please specify one mail-user, wechat-user or log-dir")
        print("    Example1:%s target.exe --log-dir='path/to/log/'..."%sys.argv[0])
        print("    Example2:%s target.exe --mail-user=user --mail-passwd=password..."%sys.argv[0])
        print("    Example3:%s target.exe --wechat-user=user --wechat-passwd=password ..."%sys.argv[0])
        print("    Example4:%s target.exe --log-dir='path/to/log/' --mail-user=user1 --mail-passwd=password1 --wechat-user=user2 --wechat-passwd=password2 ..."%sys.argv[0])
        return

    if "log-dir" in opt and not os.path.isfile(opt['log-dir'][0]):
        print("note: a regular file path is required will a dir or some thing others got:%s"%opt["log-dir"][0])
        return
    else: # create log director
        # log_dir = os.path.abspath(opt["log-path"][0],os.pardir)
        if not os.path.exists(opt["log-dir"][0]):
            os.makedirs(opt["log-dir"][0])
    
    if "mail-user" in opt and "mail-passwd" not in opt:
        print("note: please specify password(with `--mail-passwd` flag) for %s"%opt["mail-user"][0])
        return

    if "wechat-user" in opt and "wechat-passwd" not in opt:
        print("note: please specify password(with `--wechat-passwd` flag) for %s"%opt["wechat-user"][0])
        return
    
    if "mail-user" in opt and "r" not in opt or len(opt["r"]) < 1:
        print("note: when using mail, at least one reciver(with flag `-r`) required")
        print("    Example1:%s target.exe --mail-user=user --mail-passwd=password -r reciever1@example.com [-r reciever2@example.com ...]...")
        return
    -e for extra-info, e.g: -e name-of-process dump, which will send with mail/wechat
   """) 

def main():
    if len(sys.argv) < 2 or is_opt_flag(sys.argv[1]):
        print("note: please specify the target to supervise")
        print("    Example:%s target.exe ..."%sys.argv[0])
        return

    opt = getopt(sys.argv[2:])
    if ("h" in opt or "help" in opt):
        help()

    if "mail-user" not in opt and "wechat-user" not in opt and "log-dir" not in opt:
        print("note: please specify one mail-user, wechat-user or log-dir")
        print("    Example1:%s target.exe --log-dir='path/to/log/'..."%sys.argv[0])
        print("    Example2:%s target.exe --mail-user=user --mail-passwd=password..."%sys.argv[0])
        print("    Example3:%s target.exe --wechat-user=user --wechat-passwd=password ..."%sys.argv[0])
        print("    Example4:%s target.exe --log-dir='path/to/log' --mail-user=user1 --mail-passwd=password1 --wechat-user=user2 --wechat-passwd=password2 ..."%sys.argv[0])
        return

    if "log-dir" in opt and os.path.isfile(opt['log-dir'][0]):
        print("note: a directory path is required while a regular got:%s"%opt["log-dir"][0])
        return
    else: # create log director
        # log_dir = os.path.abspath(opt["log-path"][0],os.pardir)
        if not os.path.exists(opt["log-dir"][0]):
            os.makedirs(opt["log-dir"][0])
    
    if "mail-user" in opt and "mail-passwd" not in opt:
        print("note: please specify password(with `--mail-passwd` flag) for %s"%opt["mail-user"][0])
        return

    if "wechat-user" in opt and "wechat-passwd" not in opt:
        print("note: please specify password(with `--wechat-passwd` flag) for %s"%opt["wechat-user"][0])
        return
    
    if "mail-user" in opt and ("r" not in opt or len(opt["r"]) < 1):
        print("note: when using mail, at least one reciver(with flag `-r`) required")
        print("    Example1:%s target.exe --mail-user=user --mail-passwd=password -r reciever1@example.com [-r reciever2@example.com ...]...")
        return
    try:
        info = os.popen(sys.argv[1]).read()
    except Exception as e:
        info = str(e)
    extra_info = opt['e'] + [info]
    content = "【进程死亡】{}:{}\n进程/命令：{}\n细节：\n{}".format(
        socket.gethostbyname(socket.gethostname()),os.getcwd(),sys.argv[1],"\n".join(extra_info))
    # 微信发送
    if "wechat-user" in opt:
        quick_send_msg("盛塘·子衿风控",content,opt["wechat-user"][0],opt["wechat-passwd"][0])
    # 邮件发送
    if "mail-user" in opt:
        agent = EmailAgent("盛塘·子衿",opt["mail-user"][0],opt["mail-passwd"][0])
        agent.to_list = opt["r"]
        attach = agent.build_email_to_send("【程序异常报警】",content)
        agent.send(attach)
    # 日志报错
    if "log-dir" in opt:
        logger = logging.getLogger("supervised")
        fhd = logging.FileHandler(os.path.join(opt["log-dir"][0],"supervised.log"),mode="a",encoding=None,delay=False)
        fmt = logging.Formatter(fmt="%(asctime)-15s[%(levelname)s] %(filename)s %(funcName)s %(lineno)d||%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        fhd.setFormatter(fmt)
        logger.addHandler(fhd)
        logger.error(content.replace("\n","||").replace("\r","||").replace(":","=").strip("||"))

if __name__ == "__main__":
    main()
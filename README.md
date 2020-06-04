## Supervised For Windows
This is a simple but useful processor for service deploying, which is similar with supervied under linux/mac. what different is that this one do not provide restart strategy. Instead, it provide warning with wechat/mail/log which more useful in our production environment.
### Basic Info
- Create on 2020-05
- by Paul Li @ ST.Tec
### Build/Distribute
- this can be package with `nuitka3` so `nuitka3` is required
- install `nuitka3`: `pip install nuitka`
- build package command: `python buildexe.py`
- install `supervised.exe`: `add path of supervised.exe which is in supervised.dist to PATH environment varaible`
### About `Nuitka`
- `--standalone` is used for install convenience
- `--windows-disable-console` is used for `Backgrounder Runnging` just like `&` in linux/mac
### User Guide
``` Python
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
```
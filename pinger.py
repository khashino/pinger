import argparse, subprocess, platform, time, logging

def arghandler():
    parser = argparse.ArgumentParser(description="Variables")
    parser.add_argument('-u', type=str,required=True , help='url or ip address')
    parser.add_argument('-c', type=int, help='Count of ping. Default never stop till (Ctrl+c)')
    parser.add_argument('-s', type=int, help='Sleep time between every ping. Default 1 second')
    args = parser.parse_args()
    print(type(args.s))
    #print(getattr(args, 's'))
    global count
    global sleeptime
    global url
    url = str(args.u)
    if not args.s:
        sleeptime = 1
    else:
        sleeptime = args.s

    if not args.c:
        count = 1
    else:
        count = args.c


def pinger():
    # Ping parameters as function of OS
    #ping_str = "-n "+str(count) if platform.system().lower() == "windows" else "-c "+str(count)
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + url
    need_sh = False if platform.system().lower() == "windows" else True
    process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=need_sh)
    return process
    #return subprocess.Popen(args, shell=need_sh, stdout=subprocess.PIPE) == 0



def winout():
    cnt = count
    res = False
    while cnt > 0:
        for line in pinger().stdout:
            #print(str(line).find("Reply"))
            #print("Reply" in str(line))
            if res == True:
                print(str(line)[2:-5])
                logging.info(str(line)[2:-5])
                res = False
            if "Pinging" in str(line):
                res = True
        cnt -= 1
        time.sleep(sleeptime)



def linout():
    return 0


def logger():
    return 0

def main():
    arghandler()
    logging.basicConfig(format='%(asctime)s|%(message)s', filename='log/ping-'+url+'.log', filemode='w', level=logging.INFO)
    if platform.system().lower() == "windows":
        winout()
    else:
        linout()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
from urllib.request import Request, urlopen
import urllib.parse, urllib.error
import re
import json
import threading
import sys


Lock = threading.Lock()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class controller:
    """ A website checker objects """
    def __init__(self, target):
        data = json.load(open("sites.json"))
        self.sites = [site(value) for value in data.values()]
        self.target = target
        self.scan()

    def scan(self):
        threadPool = []
        for _ in range(len(self.sites)):
            threadPool.append(scannerThread(self.sites[_], self.target).start())


class scannerThread(threading.Thread):
    def __init__(self, siteObj, target):
        threading.Thread.__init__(self)
        self.site = siteObj
        self.target = target

    def run(self):
        self.site.scan(self.target)


class site:
    """ A site object that has functions such as encoding, regex """
    def __init__(self, obj):
        """ Accepts JSON object """
        self.name    = obj["name"]
        self.url     = obj["url"]
        self.encoder = obj["encoder"]
        self.regex   = re.compile(obj["regex"])

    def scan(self, url):
        payload = self.url + eval(str(self.encoder).format(url))
        page = self.fetchpage(payload)

        if not page or len(page) == 0:
            with Lock:
                print("{}[!] Got no response for query : {}{}".format(
                  bcolors.WARNING, payload, bcolors.ENDC))
            return

        result = self.regex.findall(page)[0]

        if result in ("up", "online"):
            with Lock:
                print(("{}[+] {}{} reports {}ONLINE!{}".format(
                   bcolors.WARNING, bcolors.ENDC, self.name,
                   bcolors.OKBLUE, bcolors.ENDC)))
        elif result in ("down", "offline"):
            with Lock:
                print(("{}[+] {}{} reports {}OFFLINE!{}".format(
                  bcolors.WARNING, bcolors.ENDC, self.name,
                  bcolors.FAIL, bcolors.ENDC)))
        else:
            with Lock:
                print("[!] RegEx returns abnormal result")
                print((self.payload))
                print(result)

    def fetchpage(self, url):
        try:
            request = urllib.request.Request(url)
            request.add_header("UserAgent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
            return urlopen(request).read().decode('utf-8')
        except Exception as e:
            with Lock:
                print(("{}[!] Unable to connect to {}{}".format(
                   bcolors.WARNING, url, bcolors.ENDC)))
                print("Exception : {}".format(e))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : uod.py http://www.google.com")
    elif len(sys.argv) == 2:
        program = controller(sys.argv[1])
        # program.target = URL(sys.argv[1]).url
    else:
        print("Usage : uod.py http://www.google.com")

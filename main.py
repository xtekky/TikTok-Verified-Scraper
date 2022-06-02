import requests , json, random, string, threading, os, time, cursor
cursor.hide()


class Verifinder:
    def __init__(self):

        os.system('mode con: cols=60 lines=1')
        os.system(f'cls' if os.name == 'nt' else '')

        self.accs = []
        self.reqs = 0
        self.hits = 0
        self.rates = 0

        self.sessid = "" #SESSION ID HERE

        self.threads = 3
        self.rate_time = 30
        self.cursor = 0

        self.starter()

    def title(self):
        while True:
            os.system(f'title Verifinder ^| Hits ~ {self.hits} ^| Requests ~ {self.reqs} Rates ~ {self.rates}' if os.name == 'nt' else '')

    def starter(self):
        threading.Thread(target=self.title).start()
        while True:
            if threading.active_count() < self.threads + 1:
                threading.Thread(target=self.worker, args=(self.cursor,)).start()
                #self.cursor += 1

    def worker(self, cursor):
        try:
            key_word = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=1))

            URI = f"https://api31-normal-useast1a.tiktokv.com/aweme/v1/discover/search/?count=30&offset=30&cursor={cursor}&keyword={key_word}&search_source=report_user&type=1&device_id=7100986933613987334&aid=1233"
            PARAMS = {
                'Cookie': f'sessionid={self.sessid}',
                'User-Agent': 'com.zhiliaoapp.musically/2022405010 (Linux; U; Android 7.1.2; en; ASUS_Z01QD; Build/N2G48H;tt-ok/3.12.13.1)',
            }

            accounts = requests.get(URI, headers=PARAMS)
            self.reqs += 1

            for _ in accounts.json()["user_list"]:
                if _["user_info"]["unique_id"] not in self.accs:
                    self.accs.append(_["user_info"]["unique_id"])
                    print(f'{_["user_info"]["unique_id"]}:{_["user_info"]["follower_count"]}:{_["user_info"]["uid"]}:{_["user_info"]["sec_uid"]}:{_["user_info"]["region"]}', file=open("accounts.txt", "a"))
                    self.hits += 1


        except:
            self.rates += 1
            time.sleep(self.rate_time)

Verifinder()

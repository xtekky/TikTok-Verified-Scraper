import time
import string
import requests
import itertools

from urllib.parse import urlencode
from utils.signer import *

class Verifinder:
    def __init__(self, proxy: str or None = None, count: int = 4) -> None:
        self.proxies  = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
        self.accounts = []
        self.keywords = get_keywords(count)

    def __base_params(self, keyword: str, cursor: int = 0) -> str:
        return urlencode({
            "count"             : 30,
            "cursor"            : cursor,
            "keyword"           : keyword,
            "search_source"     : "report_user",
            "type"              : 1,
            "request_tag_from"  : "h5",
            "storage_type"      : 0,
            "iid"               : 7137816409338136325,
            "channel"           : "googleplay",
            "device_type"       : "SM-G973N",
            "device_id"         : 6990239216324986369,
            "os_version"        : 9,
            "version_code"      : 160904,
            "app_name"          : "musically_go",
            "device_brand"      : "samsung",
            "device_platform"   : "android",
            "aid"               : 1340,
        })
        
    def __base_headers(self, params: str) -> dict:
        sig = XGorgon(
            params = params
        ).get_value()
        
        return {
            "accept-encoding"   : "gzip",
            "sdk-version"       : "2",
            "x-ss-req-ticket"   : str(int(time.time() * 1000)),
            "x-khronos"         : sig["X-Khronos"],
            "x-gorgon"          : sig["X-Gorgon"],
            "host"              : "api16-normal-c-useast1a.tiktokv.com",
            "connection"        : "Keep-Alive",
            "user-agent"        : "okhttp/3.10.0.1"
        }
    
    def __scrape_veris(self, keyword: str, cursor: int = 0) -> requests.Response:
        __base_params = self.__base_params(keyword, cursor)

        return requests.get(
            url = (
                "https://api16-normal-c-useast1a.tiktokv.com"
                    + "/aweme/v1/discover/search/?"
                    + __base_params 
            ),
            headers = self.__base_headers(__base_params)
        )
        
    def main(self):
        cursor  = 0
        for keyword in self.keywords:
            while True:
                try:
                    __scrape_req = self.__scrape_veris(keyword, cursor)
                    # print(__scrape_req.text)
                    for _ in __scrape_req.json()["user_list"]:
                        if _["user_info"]["unique_id"] not in self.accounts:
                            
                            self.accounts.append(_["user_info"]["unique_id"])
                            info_string = f'{_["user_info"]["unique_id"]}:{_["user_info"]["follower_count"]}:{_["user_info"]["uid"]}:{_["user_info"]["sec_uid"]}:{_["user_info"]["region"]}'
                            
                            print(info_string)
                            
                            with open("utils/veris.txt") as file:
                                file.write(info_string + "\n")
                    
                    if len(__scrape_req.json()["user_list"]) == 0:
                        cursor = 0
                        break
                    
                    cursor += 30 if cursor < 30 else 31
                
                except Exception:
                    cursor = 0
                    break
                
if __name__ == "__main__":
    Verifinder().main()
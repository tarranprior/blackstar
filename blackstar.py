#! /usr/bin/env python3

import argparse
import asyncio
import json
import os
import random
import datetime

import aiohttp
from colorama import Fore, init

SITEDATA = json.load(open("sites.json"))
USERAGENTS = open("useragents.txt").read().splitlines()

B = Fore.LIGHTBLACK_EX
G = Fore.LIGHTGREEN_EX
R = Fore.LIGHTRED_EX
W = Fore.WHITE
Y = Fore.LIGHTYELLOW_EX
init()


async def search_username(
    username: str, timeout: int, show_all: bool
) -> None:

    timeout = aiohttp.ClientTimeout(total=timeout)
    start_time = datetime.datetime.now()

    print(f"{W}[{Y}*{W}]{Y} "
        + f"Searching for {W}{username}{Y} "
        + f"across a total of {len(SITEDATA['all_sites'])} social networking platforms:\n")

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        success_count = 0
        for site in SITEDATA["all_sites"]:
            task = asyncio.ensure_future(
                make_request(session, site, username, show_all)
            )
            tasks.append(task)
        results = await asyncio.gather(*tasks)

    finish_time = datetime.datetime.now()
    total_duration = round((finish_time - start_time).total_seconds(), 2)

    json_results = {
        "parameters": {
            "username": username,
            "date": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
            "total_sites": len(SITEDATA['all_sites']),
            "search_duration": f"{total_duration}s",
        },
        "results": []
    }

    for i in results:
        json_results['results'].append(i[0])
        if i[1]:
            success_count += 1

    with open(
        os.path.join(os.path.dirname(__file__), "results",
        username + ".json"), mode='w', encoding='utf-8'
    ) as f:
        json.dump(json_results, f, indent=4, ensure_ascii=False)

    print(f"\n{W}[{G}+{W}]{G} "
        + f"{success_count} total user profiles.")
    print(f"{W}[{Y}*{W}]{Y} "
        + f"Search complete in {W}{(total_duration)}s{Y}. "
        + f"Results written to {W}'results/{username}.json'{Y}.\n")


async def make_request(
    session, site: str, username: str, show_all: bool
) -> tuple:

    url = site["url"].format(username=username)
    headers = {"User-Agent": random.choice(USERAGENTS)}

    try:
        async with session.request(
            site["method"], url, headers=headers, ssl=False
        ) as response:
            response_content = await response.text()

            if eval(site["success"]):
                print(f"{W}[{G}+{W}] "
                    + f"{G}{site['name']}: {W}{url} "
                    + f"{B}[{response.status} {response.reason}]"
                )

                return {
                    "site": site["name"],
                    "url": site["url"].format(username=username),
                    "response_status": f"{response.status} {response.reason}",
                    "success": True,
                }, True

            else:
                if show_all:
                    print(f"{W}[{R}-{W}] "
                        + f"{R}{site['name']}: {W}{url} "
                        + f"{B}[{response.status} {response.reason}]"
                    )

                return {
                    "site": site["name"],
                    "url": site["url"].format(username=username),
                    "response_status": f"{response.status} {response.reason}",
                    "success": False,
                }, False

    except TimeoutError:
        if show_all:
            print(f"{W}[{Y}-{W}] "
                + f"{Y}{site['name']}: {W}{url} "
                + f"{B}[Timeout]"
            )

        return {
            "site": site["name"],
            "url": site["url"].format(username=username),
            "response_status": "Timeout",
            "success": False,
        }, False


if __name__ == "__main__":

    print("""
             ,d8          ______  _              _                            
          ,d888" ,d      (____  \| |            | |           _               
      888888888,d88       ____)  ) | _____  ____| |  _  ___ _| |_ _____  ____ 
 =888888888888888K       |  __  (| |(____ |/ ___) |_/ )/___|_   _|____ |/ ___)
      888888888"Y88      | |__)  ) |/ ___ ( (___|  _ (|___ | | |_/ ___ | |
          "Y888, "Y      |______/ \_)_____|\____)_| \_|___/   \__)_____|_|
             "Y8         
          """)

    parser = argparse.ArgumentParser(
        description="""
        An asynchronous and lightweight open-source intelligence tool
        which searches for usernames across common social networking platforms.
        """
    )
    parser.add_argument(
        "-u", '--username',
        action="store",
        dest="username",
        required=True,
        help="specify a target username."
    )
    parser.add_argument(
        "-t", "--timeout",
        action="store",
        dest="timeout",
        required=False,
        default=30,
        type=int,
        help="specify a time to wait (in seconds) before requests time out."
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        dest="show_all",
        required=False,
        default=False,
        help="show all results."
    )
    arguments = parser.parse_args()

    if arguments.username:
        asyncio.run(search_username(
                arguments.username,
                arguments.timeout,
                arguments.show_all
        ))

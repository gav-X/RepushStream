import time
from utils import *


def try_to_push_live_stream():
    youtube_live_url = None
    schedule_start_time = None
    retry_times = 0

    # main loop：
    # 1. reset youtube live url, schedule_start_time to None, wait for next live stream, if retry_times > 20 (about 7 minutes)
    # 1. get YouTube live url if youtube_live_url is None
    # 2. if the live stream is upcoming and not started yet, sleep 30s and continue
    # 3. try to repush YouTube and twitch
    # 4. if repush successfully, sleep 60s and continue
    # 5. if both YouTube and twitch are not living, sleep 30 minutes and continue
    # 6. if repush failed, sleep 20s and continue

    while True:
        now = get_bj_time()

        if retry_times > 20:
            # reset youtube_url to None and wait for next live stream
            print(f"{now}: It's time to sleep, break the loop.")
            return

        if youtube_live_url is None:
            print(f"{now}: Try to get youtube live url...")
            res = get_youtube_live_url()
            youtube_live_url = res[0]
            schedule_start_time = res[1]

        if schedule_start_time and schedule_start_time > now:
            print(f"{now}: the live stream is not started yet.")
            time.sleep(30)
            continue

        push_result = try_to_push_youtube(youtube_live_url) and try_to_push_twitch()
        if push_result == 0:
            print(f"{now}: Repush twitch successfully.")
            retry_times = 0
            time.sleep(60)
            continue

        if youtube_live_url is None:
            print(f"{now}: Both youtube and twitch are not living. Sleep 30 minutes.")
            time.sleep(30 * 60)
        else:
            print(f"{now}: Repush youtube and twitch failed. Maybe caused by network, will retry 30s later.")
            retry_times += 1
            time.sleep(20)


def main():
    load_from_config()
    while True:
        try_to_push_live_stream()


if __name__ == "__main__":
    main()

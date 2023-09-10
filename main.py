import time
from utils import *

if __name__ == '__main__':
    load_from_config()

    youtube_live_url = None
    schedule_start_time = None
    kick_is_living = False

    # main loop：
    # 1. reset youtube live url, schedule_start_time to None, wait for next live stream, if now is between 4:00 and 8:00
    # 1. get youtube live url if youtube_live_url is None
    # 2. if the live stream is upcoming and not started yet, sleep 30s and continue
    # 3. try to repush youtube and twitch
    # 4. if repush successfully, sleep 60s and continue
    # 5. if both youtube and twitch are not living, sleep 30 minutes and continue
    # 6. if repush failed, sleep 30s and continue

    while True:
        now = get_bj_time()

        if now.replace(hour=4, minute=0, second=0, microsecond=0) <= now <= now.replace(hour=8, minute=0, second=0,
                                                                                        microsecond=0):
            # reset youtube_url to None and wait for next live stream
            print(f"{now}: It's time to sleep. Reset youtube_url to None and wait for next live stream.")
            youtube_url = None
            schedule_start_time = None

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
            time.sleep(60)
            continue

        if not youtube_is_living(youtube_live_url):
            print(f"{now}: Both youtube and twitch are not living. Sleep 30 minutes.")
            time.sleep(30 * 60)
            continue

        print(f"{now}: Repush youtube and twitch failed. Maybe caused by network, will retry 30s later.")
        time.sleep(30)

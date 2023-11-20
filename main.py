import time
from utils import *


def try_to_push_live_stream():
    schedule_start_time = None

    # main loop：
    # 1. check if the channel is live streaming, if yes, repush and return
    # 2. get YouTube live url if it is upcoming
    # 3. if the live stream is upcoming and not started yet, sleep 30s and continue
    # 4. try to repush YouTube and twitch
    # 5. if repush successfully, sleep 60s and continue
    # 6. if both YouTube and twitch are not living, sleep 30 minutes and continue
    # 7. if repush failed, sleep 30s and continue

    # check whether the channel is live streaming if youtube_live_url is not initialized
    youtube_live_url = get_live_streaming_url()

    # if the channel is live streaming, repush and return
    if youtube_live_url is not None:
        print(f"{get_bj_time()}: The channel is live streaming: {youtube_live_url}")
        youtube_live_url = youtube_live_url
        push_result = try_to_push_youtube(youtube_live_url) and try_to_push_twitch()

        if push_result == 0:
            print(f"{get_bj_time()}: Repush to kick successfully.")
            time.sleep(60 * 60 * 12)
            return

        print(f"{get_bj_time()}: Repush youtube and twitch failed. Maybe caused by network, will retry 30s later.")
        time.sleep(30)
        return

    while True:
        # if the channel is not live streaming, check whether the youtube_live_url has get upcoming initialized
        # if not try to get upcoming url
        if youtube_live_url is None and schedule_start_time is None:
            print(f"{get_bj_time()}: Try to get upcoming youtube live url...")
            res = get_upcoming_url()
            youtube_live_url = res[0]
            schedule_start_time = res[1]

        # if the live stream is not upcoming, sleep 30 minutes and continue
        if youtube_live_url is None and schedule_start_time is None:
            print(f"{get_bj_time()}: Both youtube and twitch are not living or upcoming. Sleep 30 minutes.")
            time.sleep(30 * 60)
            continue

        # if the live stream is upcoming and not started yet, sleep 30s and continue
        if schedule_start_time and schedule_start_time > get_bj_time():
            print(f"{get_bj_time()}: The live stream is not started yet.")
            time.sleep(30)
            continue

        # if the live stream is upcoming and started, try to repush youtube and twitch
        push_result = try_to_push_youtube(youtube_live_url) and try_to_push_twitch()
        if push_result == 0:
            print(f"{get_bj_time()}: Repush twitch successfully.")
            time.sleep(60 * 60 * 12)
            return
        else:
            print(f"{get_bj_time()}: Repush youtube and twitch failed. Maybe caused by network, will retry 30s later.")
            time.sleep(30)


def main():
    load_from_config()
    while True:
        try_to_push_live_stream()


if __name__ == "__main__":
    main()

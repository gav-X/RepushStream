import time
from utils import *


def try_to_push_live_stream():
    youtube_live_url = None
    schedule_start_time = None

    # main loop：
    # 1. check if the channel is live streaming, if yes, repush and return
    # 2. get YouTube live url if it is upcoming
    # 3. if the live stream is upcoming and not started yet, sleep 30s and continue
    # 4. try to repush YouTube and twitch
    # 5. if repush successfully, sleep 60s and continue
    # 6. if both YouTube and twitch are not living, sleep 30 minutes and continue
    # 7. if repush failed, sleep 30s and continue

    while True:
        now = get_bj_time()

        living_stream_url = get_live_streaming_url()

        if living_stream_url is not None:
            print(f"{now}: The channel is live streaming: {living_stream_url}")
            youtube_live_url = living_stream_url
            push_result = try_to_push_youtube(living_stream_url) and try_to_push_twitch()

            if push_result == 0:
                print(f"{now}: Repush to kick successfully.")
                time.sleep(60 * 60 * 12)
                return

            print(f"{now}: Repush youtube and twitch failed. Maybe caused by network, will retry 30s later.")
            time.sleep(30)
            continue

        if youtube_live_url is None and schedule_start_time is None:
            print(f"{now}: Try to get upcoming youtube live url...")
            res = get_upcoming_url()
            youtube_live_url = res[0]
            schedule_start_time = res[1]

        if youtube_live_url is None and schedule_start_time is None:
            print(f"{now}: Both youtube and twitch are not living or upcoming. Sleep 30 minutes.")
            time.sleep(30 * 60)

        if schedule_start_time and schedule_start_time > now:
            print(f"{now}: The live stream is not started yet.")
            time.sleep(30)
            continue

        push_result = try_to_push_youtube(youtube_live_url) and try_to_push_twitch()
        if push_result == 0:
            print(f"{now}: Repush twitch successfully.")
            time.sleep(60 * 60 * 12)
            return
        else:
            print(f"{now}: Repush youtube and twitch failed. Maybe caused by network, will retry 30s later.")
            time.sleep(30)


def main():
    load_from_config()
    while True:
        try_to_push_live_stream()


if __name__ == "__main__":
    main()

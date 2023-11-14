import googleapiclient.discovery
import googleapiclient.errors

# Create the YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)


twitch_url = None


def get_bj_time():
    import datetime
    from dateutil import tz

    # 获取当前UTC时间
    utc_time = datetime.datetime.now(tz=tz.tzutc())
    print(utc_time.strftime('%Y-%m-%d %H:%M:%S %Z'))
    # 设置时区为北京时间
    bj_tz = tz.gettz('Asia/Shanghai')
    bj_time = utc_time.astimezone(bj_tz)
    return bj_time


def load_from_config():
    # load parameters from config.json
    # Replace with your own API key and channel ID
    # 67373 channel id: "UC7QVieoTCNwwW84G0bddXpA"

    import json
    with open('config.json') as json_file:
        data = json.load(json_file)
        global api_key
        global channel_id
        global destination_url
        global twitch_url
        api_key = data["api_key"]
        channel_id = data["channel_id"]
        destination_url = data["destination_url"]
        twitch_url = data["twitch_url"]


def repush_to_target_stream(original_stream_url):
    import subprocess

    print(f"The channel is live streaming: {original_stream_url}")

    repush_cmd = f"streamlink {original_stream_url} \"1080p,720p,480p\" -O | ffmpeg  -i pipe: -c copy -f flv -bsf:a aac_adtstoasc {destination_url}"
    print(repush_cmd)
    return_code = subprocess.call(repush_cmd, shell=True)
    return return_code


def get_live_streaming_url():
    # Define the API request parameters
    request = youtube.liveBroadcasts().list(
        part='id,snippet,status',
        channelId=channel_id,
        broadcastStatus='active'
    )

    # Execute the API request
    response = request.execute()

    # Check if the channel is currently streaming
    if response['items']:
        print('The channel is currently streaming!')
        stream_url = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']
        print(f'The streaming URL is: {stream_url}')
        return stream_url
    else:
        print('The channel is not currently streaming.')
        return None


def get_upcoming_url():
    # Call the search.list method and pass the parameters
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="upcoming",
        type="video"
    )
    response = request.execute()
    print("Search response: ", response)

    # Loop through each item in the response
    items = response["items"]
    if not items:
        return [None, None]

    # Get the video ID, title and publishedAt from the snippet
    video_id = items[0]["id"]["videoId"]

    # Call the videos.list method and pass the video ID and part
    request = youtube.videos().list(
        part="liveStreamingDetails",
        id=video_id
    )
    response = request.execute()
    print("Live stream details: ", response)

    if not response["items"]:
        return [None, None]

    # Get the live-streaming details from the response
    live_streaming_details = response["items"][0]["liveStreamingDetails"]

    scheduledStartTime = live_streaming_details["scheduledStartTime"]

    # Get the live URL and live start time from the live-streaming details
    live_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"The channel is live streaming: {live_url}")
    print(f"The live stream will start at {scheduledStartTime}")
    return [live_url, transform_to_time_object(scheduledStartTime)]


def try_to_push_youtube(youtube_live_url):
    return_code = -1

    if youtube_live_url is not None:
        return_code = repush_to_target_stream(youtube_live_url)

    return return_code


def try_to_push_twitch():
    return repush_to_target_stream(twitch_url)


def transform_to_time_object(time_str):
    import datetime
    return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')

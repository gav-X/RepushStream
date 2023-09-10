# Repush stream to Kick platform

## Description
This project could pull the live stream from Youtube or Twitch and push to Kick platform. It was based on [Python](https://www.python.org/), Miniconda3 is recommended to deploy it.

## Deploy
### Install Miniconda3
Download Miniconda3 from [here](https://docs.conda.io/en/latest/miniconda.html), and install it.

### Create environment
```bash
conda create -n RepushStream python=3.9
```

### Activate environment
```bash
conda activate RepushStream
```

### Install dependencies
Install google api client
```bash
pip install --upgrade google-api-python-client
```

Install streamlink
```bash
pip install --user -U git+https://github.com/streamlink/streamlink.git
```

Apply for google data api key, fill the api key in `config.json`

Fill the Youtube channel id and Twitch channel url in `config.json`

Fill the Kick platform url in destination_url of `config.json`


### Run
```bash
python main.py
```

Recommend to run it in screen session

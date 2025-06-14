This script will perform sentiment analysis on comment section of any youtube video.
# How to use it
If you have a good GPU, you can use the script locally, but you need to install dependencies using Python's pip: `pip install matplotlib numpy transformers google-api-python-client` (`re` is preinstalled). If you don't have a good GPU, you can use Google Colab.
 To use this script, you also need a Google Cloud API token. To get your own token, visit the [official website](https://console.cloud.google.com/), register, and enable the "YouTube Data API v3". After that, you will have your own API token.
Once you have **a** token and **a** link to **the** video, you can start sentiment analysis of its comment section using the script.

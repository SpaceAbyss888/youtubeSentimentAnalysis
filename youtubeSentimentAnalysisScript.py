#======= Import ================================
import matplotlib.pyplot as plt
import numpy as np
from transformers import pipeline
from googleapiclient.discovery import build
import re

#======= Definition of "diagram" function =========================
def diagram(categories, values):
  plt.figure(figsize=(8, 5))
  bars = plt.bar(categories, values, color='skyblue')

  for bar in bars:
      height = bar.get_height()
      plt.text(bar.get_x() + bar.get_width() / 2, height,
               f'{height}',
               ha='center', va='bottom')

  plt.title('Statistic', fontsize=14)
  plt.xlabel('Category', fontsize=12)
  plt.ylabel('Amount', fontsize=12)
  plt.grid(axis='y', linestyle='--', alpha=0.7)

  plt.show()

#======= Definition of get_youtube_comments function =============
def get_youtube_comments(api_key, video_url, comments_amount):
    # Getting videos id from link ( I have no idea how this works )
    video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", video_url).group(1)

    youtube = build('youtube', 'v3', developerKey=api_key)
    comments_list = []
    next_page_token = None

    try:
        while True:
            # Here we are getting data from youtube
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            # Here we are seperating comment text from other useless for us parameters
            for item in response['items']:
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments_list.append(comment_text)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

            if len(comments_list) >= int(comments_amount):
                break

        return comments_list

    except Exception as e:
        print(f"Error: {e}")
        return comments_list

#========== Definition of the main functon ==========
def main():
  print('youtubeSentimentAnalysis started. Please read the README.md file before you countinue')
  print('Loading model...')

  model = pipeline("sentiment-analysis", "tabularisai/multilingual-sentiment-analysis", truncation=True, max_length=512)
  api_key = input('Insert your google cloud api key for youtube: ')
  link = input('Insert youtube videos link: ')
  amm_coms = input('How many comments you want to analyse? Type a number: ')

  comments = get_youtube_comments(api_key, link, amm_coms)
  print(f'{len(comments)} comments have been collected')
  if len(comments) == 0:
    print('NO COMMENTS HAVE BEEN COLLECTED! Script has been stopped...')
  else:
    print('Starting sentiment analysis... This could take а few minutes...')

    results = model(comments)

    label = None
    very_positive = 0
    positive = 0
    neutral = 0
    negative = 0
    very_negative = 0

    for result in results:
      label = result['label']
      match label:
        case 'Very Positive':
          very_positive += 1
        case 'Positive':
          positive += 1
        case 'Neutral':
          neutral += 1
        case 'Negative':
          negative += 1
        case 'Very Negative':
          very_negative += 1

    print('Results of sentiment analysis:')
    print(f'Amount of very positive comments: {very_positive} ( {very_positive / len(results) * 100}% )')
    print(f'Amount of positive comments: {positive} ( {positive / len(results)  * 100}% )')
    print(f'Amount of neutral comments: {neutral} ( {neutral / len(results) * 100}% )')
    print(f'Amount of negative comments: {negative} ( {negative / len(results) * 100}% )')
    print(f'Amount of very negative comments: {very_negative} ( {very_negative / len(results) * 100}% )')

    print('Making a bar diagram')
    categories = ['very positive', 'positive', 'neutral', 'negative', 'very negative']
    values = [very_positive,
            positive,
            neutral,
            negative,
            very_negative]
    diagram(categories, values)
  print('End of script')

if __name__ == '__main__':
  main()
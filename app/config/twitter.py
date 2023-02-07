import tweepy

consumer_key = "8boDLmFaRUJZD7RE0jw1AykvD"
consumer_secret = "G8stbPhwSfRMvrMBBjprj39sP89DPxAvOpsTR80cmY7nHTcbxb"
access_token = "1621846637634293760-WVaY5aRHsjl6c5GwlxrYnhBenaVeax"
access_token_secret = 'RAtNNlO4ySqMhXSoSfAx8xw779vNXBa6yGZvi0rqoAwNA'
bearer = "AAAAAAAAAAAAAAAAAAAAADuKlgEAAAAA5siCrrKx6k97A6q%2B2goBbQ0Rxkc%3DKFrZ99GFjbXkqtH4jGKWzGnzJkAZPFF0C6olJVqA5DMHZERhie"


twitterClient = tweepy.Client(bearer_token=bearer)
auth = tweepy.OAuth2BearerHandler(bearer_token=bearer)
twitterApi = tweepy.API(auth=auth)


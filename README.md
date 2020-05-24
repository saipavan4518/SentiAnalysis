# SentiAnalysis
Sentiment analysis using machine learning and other java jar files

## Description
In this project we evaluate the new raw tweet and we predict the emotion based on the data set we have prepared. <br />
The file we used for giving the class label using StentiStrength jar file. you can know about it [here](http://sentistrength.wlv.ac.uk/).


## Code Description
We have differnet methods in this code, they are listed below. <br />
- [clean_tweet](#cleanTweet)
- storetocsv
- checkscore
- lemmtext
- deemojify
- removestuff
- final_save
- gather_data

## cleanTweet
In this module by using regular expressions we remove different non-significant data like mentios and emoticons and other data.
We also clean by using basic preprocessing by the given [prepocessor](https://pypi.org/project/tweet-preprocessor/) module
> pip install tweet-preprocessor
```
clean_tweet(given tweet)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## About
Venkata Sai Pavan M , you can contact me here [LinkedIN](https://www.linkedin.com/in/venkata-sai-pavan-madabathula-22386819b/) <br />
if you liked the code , you can drop me a like in LinkedIN.













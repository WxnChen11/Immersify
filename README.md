# Immersify
HacktheNorth 2016

To run: Clone repository and run app.py. Requires python Flask and opencv. Note: There are request limits set on the API key! If the request limit has been reached please contact wx.chen@mail.utoronto.ca

## Inspiration

Anyone who's ever tried to learn a new language knows that nothing beats learning through immersion. Now, explore and immerse yourself in countries around the world without ever leaving the comfort of home! Preparing for that upcoming vacation or exchange? Simply visit our site and explore your surroundings as if you were actually there, while simultaneously improving upon your foreign language skills!

## What it does
Our webapp allows users to walk and explore any location in the world accessible through the Google Street View Api. They can press the "immersify" button to gain contextual information about their surroundings, in the language of their choice. This improves their vocabulary in that language and encourages them to associate foreign words with their visual representations, helping them pick up the language faster. Furthermore, our webapp also has a translate feature, which will translate words in the current view to english. This feature is for travellers or immigrants who do not know the area well, and allows them to become familiar with their surroundings quickly and easily. An accompanying mobile app allows users to benefit from our webapp on the fly, with object recognition, translation, as well as example pronunciations of foreign words.

## How we built it
The back end was written in python, using the flask web framework. Multiple google cloud APIs were used, including the google maps API, google vision API, and google translate API. As a result a large portion of the web app is also written in javascript. Our accompanying mobile app is written in javascript using the ionic framework, and also uses a variety of google APIs.

## Challenges we ran into
One of the bigger challenges we ran into was handling the asynchronous nature of JavaScript, which was very non-intuitive and hard to debug at times. We also had trouble initially with the image labels being returned by google vision- most of them were very broad (such as constantly returning "property" for any kind of house, lawn, apartment, etc) and would not be particularly useful to someone using our app. We decided to partition the images into multiple parts in order to achieve a greater level of detail, which turned out to work much better.

## Accomplishments that we're proud of
Seeing our idea take shape, and finishing what we started! We also learned a lot about javascript and http protocols over the weekend.

## What we learned
How to handle asynchronous code, how to use google's API's, how get and post requests work

## What's next for Immersify
Polishing up the user interface, and improving the translation feature, as it currently picks up a lot of noise from the image background

![Demo](/Demo1.png "Demo")

![Demo](/Demo2.png "Demo")

![Demo](/Demo3.png "Demo")

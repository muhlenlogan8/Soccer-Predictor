# Soccer Predictor

Soccer Predictor is a web application that predicts the outcome of a match between two national soccer teams. It uses historical World Cup data and current FIFA rankings to make predictions using a Random Forest Classifier.

## Vision
I started this project to introduce myself to machine learning in Python. I'm a big fan of playing and watching soccer and so I wanted to create an application that predicts who would win between two soccer teams. I intend for this project to be a learning experience where I can learn and experiment with machine learning, web scraping, and Taipy application development.

## Current State
The application is functioning and does attempt to predict soccer match winners based on their FIFA rank. I am using a random forest classification model and, for the most part, the predictions are accurate and reliable, however, I intend to add more variables and data for the model to train on. The data I'm looking to incorporate into the training will be international-friendly and international tournament data.

## How Soccer Predictor Works

### Web Scraping
Packages: beautifulsoup4 & selenium

Two main data sources are pulled from:
Wikipedia: World Cup match data is scraped from Wikipedia for each year of the World Cup using beautifulsoup4. An example of what is pulled is below (https://en.wikipedia.org/wiki/2022_FIFA_World_Cup).
<p align="center"><img src="https://github.com/muhlenlogan8/Soccer-Predictor/assets/100247149/b8d08081-9000-45dc-bb7b-a0d6dd0c89a5" alt="Home Page" style="border:1px solid black; width:75%;"></p>
Soccerway: FIFA rankings are pulled from the Soccerway site using selenium. An example of what is pulled is below (https://us.soccerway.com/teams/rankings/fifa/).
<p align="center"><img src="https://github.com/muhlenlogan8/Soccer-Predictor/assets/100247149/a33173c4-4f7c-412e-8c4d-f42bb0796dbe" alt="Home Page" style="border:1px solid black; width:75%;"></p>

The data is pulled and stored in .json files so the app doesn't have to web scrape for the data on every run.

### Data Cleaning
Packages: pandas

Files: Functions/model.py, Functions/modeltest.py

After pulling the web-scraped data from the sources above, the data is cleaned and organized in a way that allows it to easily be trained on by the machine learning model.
Elements that had to be accounted for when cleaning the data ranged from, country name changes (Soviet Union -> Russia), World Cup rule changes, games that went into penalties, and other political conflicts such as Sweden being awarded a walkover against Austria in 1930 due to the annexation of Austria into the German Reich around this time.

### Machine Learning
Packages: scikit-learn

A random forest classification model is trained and used to predict who will win between two soccer teams. Currently, this model is only using the team's rank as a variable, though I intend on revamping the machine learning part of the app by adding more metrics for the model to train with to improve the model's accuracy.

### Web Application
The web application was made using Taipy and can be seen below.
<p align="center"><img src="https://github.com/muhlenlogan8/Soccer-Predictor/assets/100247149/d01c71dd-892c-4e12-9659-cf0ff5e4ee87" alt="Home Page" style="border:1px solid black; width:100%;"></p>

## Future Enhancements
- Add more variables for the machine learning model to train on. Possible variables could be average goals scored, average goals against, World Cup games played, World Cup wins, average player cost (will need players on each team currently and their salary), and most recent match result.
- Pull more data to train on such as international friendlies and other tournament competitions outside the World Cup.
- Experiment with other machine learning models
- Attempt to implement parallel computing to scrape data to speed up the process.
- Update the accuracy callout in the application since currently, this percentage is misleading. I intend to do this when updating the machine learning aspects mentioned prior.
- Expand to club-level soccer using leagues such as the Premier League and the MLS.

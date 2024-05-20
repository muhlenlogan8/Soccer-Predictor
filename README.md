# Soccer Predictor

Soccer Predictor is a web application that predicts the outcome of a match between two national soccer teams. It uses historical World Cup data and current FIFA rankings to make predictions using a Random Forest Classifier.

## Vision
I started this project to introduce myself to machine learning in Python. I'm a big fan of watching soccer and wanted to see if I could create an application that predicts who would win between two national soccer teams. I intend for this project to be a learning experience where I can learn and experiment with machine learning, web scraping, and Taipy application development.

## Current State
The application is functioning and does attempt to predict soccer match winners based on their FIFA rank. I am using a random forest classification model and, for the most part, the predictions are accurate and reliable, however, I intend to add more variables and data for the model to train on. The data I'm looking to incorporate into the training will be international-friendly and international tournament data.

## How Soccer Predictor Works

#### Web Scraping:
Packages: BeautifulSoup4 & Selenium

Two main data sources are pulled from:
Wikipedia: World Cup match data is scraped from Wikipedia for each year of the World Cup using beautifulsoup4. An example of what is pulled is below (https://en.wikipedia.org/wiki/2022_FIFA_World_Cup).
<p align="center"><img src="https://github.com/muhlenlogan8/Soccer-Predictor/assets/100247149/b8d08081-9000-45dc-bb7b-a0d6dd0c89a5" alt="Home Page" style="border:1px solid black; width:75%;"></p>
Soccerway: FIFA rankings are pulled from the Soccerway site using selenium. An example of what is pulled is below (https://us.soccerway.com/teams/rankings/fifa/).
<p align="center"><img src="https://github.com/muhlenlogan8/Soccer-Predictor/assets/100247149/a33173c4-4f7c-412e-8c4d-f42bb0796dbe" alt="Home Page" style="border:1px solid black; width:75%;"></p>

#### Data Cleaning:
Packages: Pandas

After pulling the web-scraped data from the sources above, the data is cleaned and organized in a way that allows it to easily be trained on by the machine learning model.
Some things that had to be accounted for when cleaning the data are below:
- Since the World Cup data spans from 1930-present, many political conflicts and national changes occurred over this timeframe:
-   test

#### Machine Learning:

#### Web Application:
<p align="center"><img src="https://github.com/muhlenlogan8/Soccer-Predictor/assets/100247149/d01c71dd-892c-4e12-9659-cf0ff5e4ee87" alt="Home Page" style="border:1px solid black; width:100%;"></p>

## Fun Challenges Faced
Most of the challenges I've faced so far have to do with data collection and cleaning. 

#### Future Enhancements
- Add more variables for the machine learning model to train on. Possible variables could be average goals scored, average goals against, World Cup games played, World Cup wins, average player cost (will need players on each team currently and their salary), and most recent match result.
- Pull more data to train on such as international friendlies and other tournament competitions outside the World Cup.
- Experiment with other machine learning models
- Attempt to implement parallel computing to scrape data to speed up the process.

# Can think of the determination of who wins as a scores problem.
# Given the data we have, the score each team is predicted to get can be calculated
# The team with the higher score wins so home score - away score and if 
# the result is positive, home team wins, if negative, away team wins.
# If the scores are near equal then it is classified as a draw.

# Things that are important:
# Home and away team's preformace overall
# Home and away team's preformace more recently (past few years)
# Home and away team's preformace against each other

# More complex:
# Importance of team value (cost of players added up)
# Importance of team's FIFA ranking

# Thinking multiple datasets could be used such as a model for the home team, away team and both teams combined.
# If it would work to just have both teams data together to classify that would be preferable
# but I'm unsure how to classify the values with the correct team for the model to utilize or if this is even possible.


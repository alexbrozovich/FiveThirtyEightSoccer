from bs4 import BeautifulSoup
from requests import get
import datetime
import pandas as pd
        
def getSoccer(url, chosenLeague='ANY', year=str(datetime.date.today().year), month=str(datetime.date.today().month), day=str(datetime.date.today().day)):
    ##Convert the given date to a string that will match the format in the dataframe for filtering
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0'+ month
    chosenDate = year + '-' + month + '-' + day
    

    ##Grab the 538 soccer prediction webpage and whittle it down to a list of the matches to be played
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    matchContainer = html_soup.find_all('tr', class_ = 'sortable-tr')
    
    ##Create the main dataframe to hold the data
    headers = ['Date', 'Country', 'League', 'Team 1', 'Team 2', 'WP1', 'WP2', 'WP3']
    df = pd.DataFrame(columns=headers)

    ##Iterate through the matches, pull relevant information, add them in a row the dataframe
    for match in matchContainer:
        currentMatch = dict.fromkeys(headers, 0)
        
        ##Pull out teams and win percentages into separate holders
        trs = match.find_all('tr')
        currentTeams = []
        currentPercents = []
        for item in trs:
            teamer = item.find_all('div', class_= 'team-div')
            for team in teamer:
                currentTeams.append(team.get_text())
            duo = item.find_all('td', class_ = 'prob')
            for iter in duo:
                currentPercents.append(iter.get_text())
                
        ##Use holders to set team names and win percentages
        currentMatch['Team 1'] = currentTeams[0]
        currentMatch['Team 2'] = currentTeams[1]
        currentMatch['WP1'] = currentPercents[0]
        currentMatch['WP2'] = currentPercents[2]
        currentMatch['WP3'] = currentPercents[1]
        
        ##Pull Country
        countryFinder = match.find('td', class_ = 'league')
        tCountry= countryFinder.find_all('div')
        country = tCountry[1].get_text().strip()
        currentMatch['Country'] = country.strip()
        
        ##Pull League
        leaguer = match.find_all('div', class_ = 'time-league')
        currentMatch['League'] = leaguer[0].get_text().strip()
        
        ##Pull Date
        dater = match.find_all('td', class_ = 'datetime')
        for d in dater:
            dateString = str(d).split('data-str="')
            currentMatch['Date'] = str(dateString[1][0:10])
            
        ##Append the new match the full match dataframe
        tempFrame = pd.DataFrame([currentMatch])
        df = df.append(tempFrame, sort=False)
    
    ##Filter the dataframe down to the given date
    df = df[df['Date'] == chosenDate]
    df = df.set_index(['Date'])
    df = df.sort_values(['Country', 'League'])
    
    print(df)
    
    filename = "soccerOut"  + chosenDate + '.csv'
    df.to_csv(filename)





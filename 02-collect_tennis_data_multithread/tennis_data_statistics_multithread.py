# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 16:45:04 2017

@author: Darek
"""

########## Define required libraries ##########################################

import urllib2
import dateutil.rrule as rrule
from datetime import date
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

########## Function definition ################################################

def extract_wta_data(monday):

    wta_global_df = dict()
    for i in cols:
        wta_global_df[i] = []

    s = monday.strftime('%Y-%m-%d')
    resp = urllib2.urlopen('https://matchstat.com/tennis?wk=' + s)
    A = resp.read()
    tmp = A[A.find('tournament-section category-wta'):A.find('tournament-section category-chw')]
    B = tmp.split('\n')
    for i in range(len(B)):
        if B[i] == '<div class="tournament-item clearfix">':
            get_surface = B[i+1].split('>')[1].split('<')[0]
            get_tour_link = B[i+2].split('href="')[1].split('">')[0]
            resp_loc = urllib2.urlopen(get_tour_link)
            A_loc = resp_loc.read()
            M = A_loc.split('<td class="round">')
            wta_local = dict()
            for j in cols:
                wta_local[j] = []
            
            wta_local['round'].extend([M[i].split('\n')[1].replace(' ', '') for i in range(1, len(M))])
            tmp = [] 
            for i in range(1, len(M)):
                try:
                    if 'Bye' not in M[i]:
                        tmp.append(M[i].split('h2h-odds-bets')[1].split('>')[0].strip('"').replace('%20', ' ')[1:].replace('/', ' - ').replace('%2F', '/'))
                    else:
                        tmp.append(M[i].split('h2h-odds-bets')[0].split('>')[3].replace('</a','- Bye')[2:])
                except:
                    tmp.append('No data')
        
            wta_local['players'].extend(tmp)
            wta_local['score'].extend([M[i].split('score-content')[1].split('</a>')[0].split('>')[2].replace('&#8209;', '-').replace('&#039;d', '.') if 'Bye' not in M[i] else 'NA' for i in range(1, len(M))])
            wta_local['odds_1'].extend([float(M[i].split('\n')[6].split('>')[1].split('<')[0]) if M[i].split('\n')[6].split('>')[1].split('<')[0] else 0 for i in range(1, len(M))])
            wta_local['odds_2'].extend([float(M[i].split('\n')[8].split('>')[1].split('<')[0]) if M[i].split('\n')[8].split('>')[1].split('<')[0] else 0 for i in range(1, len(M))])
            wta_local['tour_id'].extend([M[0].split('<h3>')[-1].split('<')[0].split(' -')[0].replace('&#039;', '')] * (len(M) - 1))
            wta_local['surface'].extend([get_surface] * len(wta_local['odds_1']))
          
            for k in wta_local:
                wta_global_df[k].extend(wta_local[k])
            del wta_local
            
    # calculate other stats outside the loop    
    wta_global_df['no_sets'].extend([i.count('-') for i in wta_global_df['score']])
    wta_global_df['higher_odd'] = [wta_global_df['odds_1'][i] > wta_global_df['odds_2'][i] if wta_global_df['odds_1'][i] > wta_global_df['odds_2'][i] else False for i in range(len(wta_global_df['odds_1']))]
    wta_global_df['player_won'] = [i.split(' - ')[0] for i in wta_global_df['players']]

    return wta_global_df

########## Start the threads ##################################################

if __name__ == '__main__':  
    
    cols = ['tour_id', 'surface', 'round', 'players', 'player_won', 'score', \
    'odds_1', 'odds_2', 'higher_odd', 'no_sets']

    # adjustable variable for desired year
    year = 2016

    # calculate all the mondays for the desired year
    mondays = tuple(rrule.rrule(rrule.WEEKLY, dtstart=date(year, 1, 2), \
    count = 52, byweekday = rrule.MO))

    global_df = dict()
    
    # define number of thread pools
    pool = ThreadPool(len(mondays) + 200) 
    
    # Open the urls in their own threads
    # and return the results
    results = pool.map(extract_wta_data, mondays)

    #close the pool and wait for the work to finish 
    pool.close() 
    pool.join()

    output = [result for result in results if all(result.values())]
    
    # merge list of dictionaries into one big dictionary
    output2 = {}
    for d in output:
        for k, v in d.iteritems():
            output2.setdefault(k, []).extend(v)
        
    # convert dictionary to pandas data frame
    C = pd.DataFrame(output2, columns = cols)

    # skip doubles and qualificaiotn matches
    D = C.ix[(C['round'] != 'QFQ') & (C['round'] != 'SFQ') & (C['round'] != 'FQ') & ~C['players'].str.contains('/')]

    # save the dataframe to CSV file    
    D.to_csv('wta_' + str(year) + '.csv', sep=',', encoding='utf-8')
    
    # delete data
    del C, D, output, output2, results, wta_flobal_df
        
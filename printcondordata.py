# -*- coding: utf-8 -*-
"""
Created on Sat May  9 16:43:23 2015

@author: jmalinchak
"""

class perform:
    def __init__(self,
            symbol = 'SPY'
            ,  minimum_midspread = 0.2
            ,  numberofweeksahead = 1
            ,  expirationday = 'friday' #'friday' #'wednesday for index'
                     ):
                         
        self.find(
            symbol 
            ,  minimum_midspread
            ,  numberofweeksahead 
            ,  expirationday 
            )
    def dayofweek_int(self,dayofweek_word):
        rv = int(-1)
        if dayofweek_word.lower() == 'friday':
            rv = int(4)
        if dayofweek_word.lower() == 'saturday':
            rv = int(5)
        if dayofweek_word.lower() == 'sunday':
            rv = int(6)
        if dayofweek_word.lower() == 'monday':
            rv = int(0)
        if dayofweek_word.lower() == 'tuesday':
            rv = int(1)
        if dayofweek_word.lower() == 'wednesday':
            rv = int(2)
        if dayofweek_word.lower() == 'thursday':
            rv = int(3)
        return rv

    def find(self
            ,  symbol = 'SPY'
            ,  minimum_midspread = 0.2
            ,  numberofweeksahead = 1
            ,  expirationday = 'friday' #'friday' #'wednesday for index'
        ):
            
        import config
        import pandas as pd        
        
        # ##########
        # Parameters    
    #    symbol = 'SPY'
    #    mycomparesym = '^VIX'
    #    numberofweeksahead = 8
    #    expirationday = 'friday' #'friday' #'wednesday for index'
    #    daysbackmid = 0
    #    myspreadindollars = 1
    #    mycumprobthreshold = 80 #Percent in whole number 80 = 80%
    #    mycumprob_to_sell_price_lowrange = 0
    #    mycumprob_to_sell_price_highrange = 100 # was 95
    #    numberofweekstolookback = 150
    #    RollingNumberOfPeriods = 120
    #    showresults = 0
        myoutputfolder = config.myoutputfolder #'C:\\Batches\\rts\\output\\condor\\candidates'
        #mycandidatesfolder = config.mycandidatesfolder #'C:\\Batches\\rts\\output\\condor\\candidates'
        #mysourcedatafolder = config.mysourcedatafolder #'C:\\Batches\\rts\\output\\condor\\candidates'

            
        #import csv
        import os
        #candidatesfolderwithsymbol = os.path.join(mycandidatesfolder,symbol)
        #sourcedatafolderwithsymbol = os.path.join(mysourcedatafolder,symbol)
        import mytools
        #mygeneral = mytools.general()
        #mygeneral.make_sure_path_exists(candidatesfolderwithsymbol) #candidatesfolderwithsymbol
        #mygeneral.make_sure_path_exists(sourcedatafolderwithsymbol) #sourcedatafolderwithsymbol
        ## ##########
        ## Date setup
        #import datetime
        #
        #today_datetime = datetime.datetime.today()
        #today_date = datetime.date.today()
        
        
        # ##########
        # Date setup
        import datetime
        today_datetime = datetime.datetime.today()
        today_date = datetime.date.today()
        today_datestring = today_date.strftime('%Y-%m-%d')
        newdatetime = today_date
        iter_date = today_date
        
        print 'numberofweeksahead',numberofweeksahead
        for expirationcounter in range(numberofweeksahead):
            print 'Range counter',expirationcounter, range(numberofweeksahead)
            newdatetime += datetime.timedelta(7*expirationcounter)   
            print 'newdatetime',newdatetime
            iter_date = newdatetime
            if expirationcounter + 1 == numberofweeksahead:
                print('expirationcounter',expirationcounter) 
                print(' range(numberofweeksahead)', range(numberofweeksahead))
                while iter_date.weekday() != self.dayofweek_int(expirationday):
                    iter_date += datetime.timedelta(1)    
                expirationdate_string = str(iter_date)
                expirationdatetime_string = str(iter_date)+' 16:00'
                #print('expirationdatetime_string',expirationdatetime_string)
                iter_date += datetime.timedelta(1)
                print('Doing...',expirationcounter,expirationdate_string)
            
                while True :
                   # today_date = today_date
                    expire_date = datetime.datetime.strptime(expirationdate_string,'%Y-%m-%d').date()
                    expire_datetime = datetime.datetime.strptime(expirationdatetime_string,'%Y-%m-%d %H:%M')
                    #print('expire_datetime',expire_datetime)
                    if today_date != expire_date:
                        break
                    today_date = today_date - datetime.timedelta(hours=24)
                delta_precise = expire_datetime - today_datetime
                delta_precise_in_seconds = delta_precise.total_seconds()
                delta_precise_in_minutes = delta_precise_in_seconds/60
                delta_precise_in_hours = delta_precise_in_seconds/60.0/60.0
                #print('delta_precise',delta_precise)
                print('delta_precise_in_seconds',delta_precise_in_seconds)
                delta = expire_date - today_date
                
                # ####################################################
                # Get Option Prices
                pricingsymbol = symbol
                if pricingsymbol in ['VIX','RUT']:
                    pricingsymbol = '^'+symbol
                    
                import pullprices as pp
                df_optionpricescurrent = pp.options_to_dataframe(pricingsymbol,expirationdate_string,0)
                #df_stockprice_realtime_to_dataframe = pp.stockprice_realtime_to_dataframe(pricingsymbol)
                #print('$$$$$$$$$$$$$ cvcvcvcvc $$$$$$$$$$$$$$$$$')
                #print(df_optionpricescurrent)
    
                if len(df_optionpricescurrent) == 0:
                    print('-:-:-:-:-:--:-:-:-:-:--:-:-:-:-:- no option prices found for',pricingsymbol,expirationdate_string)
                else:
                    
                    # ########
                    # Initialize notes
                    print('Initialized:','calculatecumulativeprobabilityofpricechangebasedonexpiration.py')
                    print('-----------')
                    print('Symbol:',symbol)
                    print('  Now:',today_datetime)
                    today_datetimestring = today_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    print('  Now string',today_datetimestring)
                    print('  Expire Date:',expire_date )
                    print('  Number of Days to Expiration:',delta.days)
                    print('  Number of Hours to Expiration:',delta_precise_in_hours)
                    print('  Number of minutes to expiration:',delta_precise_in_minutes)
                    #lastprice = df_stockprice_realtime_to_dataframe.iloc[0]['last']
                    #time = df_stockprice_realtime_to_dataframe.iloc[0]['time']
#                    print(df_optionpricescurrent)
#                    print(df_optionpricescurrent.iloc[0])
#                    print(type(df_optionpricescurrent.iloc[0]))
                    stockprice = df_optionpricescurrent.iloc[0]['stockprice']
                    time = df_optionpricescurrent.iloc[0]['time']
                    print('  Last stock trade(price+time):',stockprice,time)

                    #Evaluate spreads
                    #print(df_optionpricescurrent)
                    maxstrikecall = 0
                    maxstrikeput = 10000
                    df_optionpricesindexed = df_optionpricescurrent.set_index(['optionsymbol'])
                    ls_bestcall = []
                    ls_bestput = []
                    ofromsymbol = mytools.get_from_optionsymbol()
                    for index, row in df_optionpricesindexed.iterrows():
                        seriesshort = row
                        #print(row)
                        
                        optiontype = ofromsymbol.optiontype(index)
                        optionsymbolshort = ''
                        if optiontype == 'C':
                            iter_offset = 1
                            if float(row.strike) > float(stockprice):
                                optionsymbolshort = index
                        if optiontype == 'P':
                            iter_offset = -1                            
                            if float(row.strike) < float(stockprice):
                                optionsymbolshort = index
                        if len(optionsymbolshort) > 0:
                            optionsymbollong = ofromsymbol.offsetstrikeoptionsymbol(index,iter_offset)
                            if optionsymbollong in df_optionpricesindexed.index:
                                serieslong = df_optionpricesindexed.loc[optionsymbollong]
                                shortmid = (float(seriesshort.bid) + float(seriesshort.ask))/2
                                longmid = (float(serieslong.bid) + float(serieslong.ask))/2
                                midspread = round(shortmid - longmid,2)
                                deltapct = round((float(seriesshort.strike) - float(stockprice)) / float(stockprice),3)
                                #print('maxstrikecall',maxstrikecall,seriesshort.strike,midspread,seriesshort.bid)
                                if midspread > minimum_midspread:
                                    if optiontype == 'C':
                                        if float(seriesshort.strike) > maxstrikecall:
                                            
                                            maxstrikecall = float(seriesshort.strike)
                                            ls_bestcall = [optionsymbolshort,seriesshort.strike, serieslong.strike,midspread,deltapct]
                                    if optiontype == 'P':
                                        if float(seriesshort.strike) < maxstrikeput:
                                            maxstrikeput = float(seriesshort.strike)
                                            ls_bestput = [optionsymbolshort,seriesshort.strike, serieslong.strike,midspread,deltapct]
                                           
                                        
                    print(ls_bestcall)
                    print(ls_bestput)
#                    for optionsymbol in df_optionpricescurrent['optionsymbol']:
#                        #df.append(Function(x))
#                        iter_strike = mytools.get_from_optionsymbol.strike(optionsymbol)
#                        iter_optiontype = mytools.get_from_optionsymbol.optiontype(optionsymbol)
#                        if iter_optiontype == 'C':
#                            if iter_strike > stockprice:                                
#                                print(iter_optiontype,iter_strike,optionsymbol)
#                                print(df_optionpricesindexed.loc[optionsymbol])
                                

                    callsymbol = ''
                    putsymbol = ''
                    callstrike =  ''
                    putstrike = ''
                    capturecall = ''
                    captureput = ''
                    deltapctcall = ''
                    deltapctput = ''
                    print('ls_bestcall',ls_bestcall)
                    
                    if len(ls_bestcall) >= 3:                    
                        callsymbol = ls_bestcall[0]
                        callstrike = ls_bestcall[1]
                        capturecall = ls_bestcall[3]
                        
                        deltapctcall = ls_bestcall[4]
                    if len(ls_bestput) >= 3:                    
                        putsymbol = ls_bestput[0] 
                        putstrike = ls_bestput[1] 
                        captureput = ls_bestput[3]
                        deltapctput = ls_bestput[4]

                    '''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                                    make dataframe
                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''                    
                    dataframerows = []
                    dataframeheader = [
                              'datestamp',
                              'symbol','minimum_midspread','stockprice','time'
                            , 'callsymbol','putsymbol'
                            , 'callstrike','putstrike'
                            , 'capturecall','captureput'
                            , 'deltapctcall','deltapctput'
                            , 'mintoexp'
                            ]
                    dataframerows.append(dataframeheader)                   
                    dataframerows.append([
                              today_datetimestring
                            , symbol,minimum_midspread,stockprice,time
#                            , ls_bestcall[0],ls_bestput[0]
#                            , ls_bestcall[3],ls_bestput[3]
#                            , ls_bestcall[4],ls_bestput[4]
                            , callsymbol,putsymbol
                            , callstrike,putstrike
                            , capturecall,captureput
                            , deltapctcall,deltapctput
                            , delta_precise_in_minutes
                            ])
                    headers = dataframerows.pop(0)
                    df = pd.DataFrame(dataframerows,columns=headers)
                    df_2 = df.set_index('datestamp')
                    print(df_2)
                    '''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                                    output to CSV
                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''
                    
                    filelocation_string = myoutputfolder + "\\intraday " + today_datestring + ' ' + symbol +'.csv'
                    if os.path.exists(filelocation_string) != True:
                        df_2.to_csv(filelocation_string,columns=(
#                              'datestamp',
                              'symbol','minimum_midspread','stockprice','time'
                            , 'callsymbol','putsymbol'
                            , 'callstrike','putstrike'
                            , 'capturecall','captureput'
                            , 'deltapctcall','deltapctput'
                            , 'mintoexp'
                            )
                        )
                    else:
                        with open(filelocation_string, 'a') as f:
                            df_2.to_csv(f, header=False)
                    print 'file location:',filelocation_string    
                    #print(today_datetime.weekday())
                    #myoutputfolder
                
if __name__=='__main__':
    #o = perform(symbol='NFLX',numberofweeksahead=1)
    import sys
    print(len(sys.argv))
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            minimum_midspread = sys.argv[2]
            if len(sys.argv) > 3:
                numberofweeksahead = sys.argv[3]
        else:
            minimum_midspread = 0.2
        o = perform(symbol=sys.argv[1],minimum_midspread=minimum_midspread,numberofweeksahead=1)
    else:
        o = perform(symbol='NFLX',minimum_midspread = 0.2,numberofweeksahead=2)
        #print 'got here'
    #main(sys.argv[1:])
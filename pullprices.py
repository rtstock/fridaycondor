import sys

def make_sure_path_exists(path):
    import errno
    import os
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def stockhistory(symbol,fromdate,todate):
    from pandas.io.data import DataReader
    #from datetime import datetime
    #dfromdate = fromdate.strftime('%b%d')
    #datetime(2000,1,1), datetime(2012,1,1)
    hist = DataReader(symbol,  "yahoo", fromdate,todate)
    return hist
    #print(hist["Adj Close"])


def stockhistorybackfilledtodictionary(symbol,fromdate,todate):
    
    from pandas.io.data import DataReader
    from datetime import datetime, timedelta
    
    hist = DataReader(symbol,  "yahoo", fromdate,todate)

    date_format = "%Y-%m-%d"
    d = datetime.strptime(fromdate, date_format)
    delta = timedelta(days=1)
    last_adjclose = 'NaN'
    
    dictAdjClose = {}    
    
    while d <= datetime.strptime(todate, date_format):
        #print(d.strftime(date_format))
        d_string = d.strftime(date_format)
        if d_string in hist.index:
            last_adjclose = hist.ix[d_string]['Adj Close']
            print(d_string,last_adjclose)
        else:
            print(d_string,'nothing',last_adjclose)
        dictAdjClose[d_string] = [('AdjClose',last_adjclose)]
        d += delta

    return dictAdjClose

def stockhistorybackfilledtodictionaryofstockhistoryinstances(symbol,fromdate,todate):
    
    from pandas.io.data import DataReader
    from datetime import datetime, timedelta
    import structureforstockhistoryinstance
    hist = DataReader(symbol,  "yahoo", fromdate,todate)
    #print(hist)
    date_format = "%Y-%m-%d"
    d = datetime.strptime(fromdate, date_format)
    delta = timedelta(days=1)


    last_open = 'NaN'
    last_high = 'NaN'
    last_low = 'NaN'
    last_close = 'NaN'
    last_adjclose = 'NaN'
    last_volume = 'NaN'
    backfilled = 'NaN'
    
    dictAdjClose = {}    
    
    while d <= datetime.strptime(todate, date_format):
        stockInstance = structureforstockhistoryinstance.Framework()
        
        stockInstance.symbol = symbol
        
        d_string = d.strftime(date_format)
        if d_string in hist.index:
            last_open = hist.ix[d_string]['Open']
            last_high = hist.ix[d_string]['High']
            last_low = hist.ix[d_string]['Low']
            last_close = hist.ix[d_string]['Close']
            last_adjclose = hist.ix[d_string]['Adj Close']
            last_volume = hist.ix[d_string]['Volume']
            backfilled = 0
            #print(d_string,last_adjclose)
        else:
            backfilled = 1
            #print(d_string,'nothing',last_adjclose)
            
            
        stockInstance.open = last_open
        stockInstance.high = last_high
        stockInstance.low = last_low
        stockInstance.close = last_close
        stockInstance.adjclose = last_adjclose
        stockInstance.volume = last_volume
        stockInstance.backfilled = backfilled
        
        dictAdjClose[d_string] = stockInstance
        d += delta

    return dictAdjClose



def test_builddataframe():
    import pandas as pd
    import numpy as np
    
    df = pd.DataFrame({'a':np.random.randn(5),
                        'b':np.random.randn(5),
                        'c':np.random.randn(5),
                        'd':np.random.randn(5)})
    cols_to_keep = ['a', 'c', 'd']
    dummies = ['d']
    not_dummies = [x for x in cols_to_keep if x not in dummies]
    data = df[not_dummies]
    print(data)


def test_builddataframe2(symbol,fromdate,todate):
    import pandas as pd
    import numpy as np
    from pandas.io.data import DataReader
    from datetime import datetime, timedelta
    

    #print(hist)
    date_format = "%Y-%m-%d"
    d = datetime.strptime(fromdate, date_format)
    delta = timedelta(days=1)

    idates = 0
    while d <= datetime.strptime(todate, date_format):
        idates = idates + 1
        d += delta
    print(idates)
    dfnew = pd.DataFrame({'a':np.random.randn(idates),
                    'b':np.random.randn(idates),
                    'c':np.random.randn(idates),
                    'd':np.random.randn(idates)})
    print(dfnew)                 
#    hist = DataReader(symbol,  "yahoo", fromdate,todate)
#    
#    last_open = 'NaN'
#    last_high = 'NaN'
#    last_low = 'NaN'
#    last_close = 'NaN'
#    last_adjclose = 'NaN'
#    last_volume = 'NaN'
#    backfilled = 'NaN'
#    
#    dictAdjClose = {}    

def stockhistorybackfilledtodatframeofstockhistoryinstancesusingcache(symbol,fromdate,todate):
    print('initialized pullprices.stockhistorybackfilledtodatframeofstockhistoryinstances')
    import pandas as pd
    #import numpy as np
    from pandas.io.data import DataReader
    from datetime import datetime, timedelta
    
    import config
    mycachefolder = config.mycachefolder
    import mytools
    mytools.general().make_sure_path_exists(mycachefolder)
    #dfnew.to_csv(mycachefolder + '\\stockdatabackfilled '+ symbol '.csv',columns=(  'Open',   'High',    'Low',  'Close',    'Volume',  'Adj Close', 'Back Filled'))
    cachedfilepathname = mycachefolder + '\\stockdatabackfilled '+ symbol + ' ' + fromdate+ ' ' + todate + '.csv'
    import os
    if os.path.isfile(cachedfilepathname):
        print('--------------------------')
        print('pullprices.stockhistorybackfilledtodatframeofstockhistoryinstancesusingcache')
        print('   Found cached file:  '+cachedfilepathname)
        dfnew = pd.read_csv(cachedfilepathname,index_col=0)
    else:
        print('Getting new file:'+cachedfilepathname)
        date_format = "%Y-%m-%d"
    
        delta = timedelta(days=1)
    
        todate_date = datetime.strptime(todate, date_format)
        fromdate_date = datetime.strptime(fromdate, date_format)
        
        
    
        idates = 0
        d = datetime.strptime(fromdate, date_format)
        while d <= todate_date:
            idates = idates + 1
            d += delta
            
        # ##############
        # print(idates)
    
        #todays_date = datetime.datetime.now().date()
        index = pd.date_range(fromdate_date, periods=idates, freq='D')
        columns = [
         'Open',   'High',    'Low',  'Close',    'Volume',  'Adj Close', 'Back Filled',     
        ]
        dfnew = pd.DataFrame(index=index, columns=columns)
        dfnew = dfnew.fillna('NaN') # with 0s rather than NaNs
        
        # ############
        # print(dfnew)                 
        
        hist = DataReader(symbol,  "yahoo", fromdate,todate)
        
        # #########
        # print(hist)
        
        last_open = 'NaN'
        last_high = 'NaN'
        last_low = 'NaN'
        last_close = 'NaN'
        last_adjclose = 'NaN'
        last_volume = 'NaN'
        backfilled = 'NaN'
        
        d = datetime.strptime(fromdate, date_format)
        while d <= todate_date:
            d_string = d.strftime(date_format)
            
            #print(d_string)
            if d_string in hist.index:
                last_open = hist.ix[d_string]['Open']
                last_high = hist.ix[d_string]['High']
                last_low = hist.ix[d_string]['Low']
                last_close = hist.ix[d_string]['Close']
                last_volume = hist.ix[d_string]['Volume']
                last_adjclose = hist.ix[d_string]['Adj Close']
                backfilled = 0
                #print(d_string,last_adjclose)
            else:
                backfilled = 1
                #print(d_string,'nothing',last_adjclose)
                
            
            dfnew.ix[d_string]['Open'] = last_open 
            dfnew.ix[d_string]['High'] = last_high 
            dfnew.ix[d_string]['Low'] = last_low
            dfnew.ix[d_string]['Close'] = last_close        
            dfnew.ix[d_string]['Volume'] = last_volume
            dfnew.ix[d_string]['Adj Close'] = last_adjclose
            dfnew.ix[d_string]['Back Filled'] = backfilled
            
            d += delta
        
            
        dfnew.to_csv(cachedfilepathname,columns=('Open',   'High',    'Low',  'Close',    'Volume',  'Adj Close', 'Back Filled'))
        
    
    #print(dfnew)
    return dfnew

def stockhistorybackfilledtodatframeofstockhistoryinstances(symbol,fromdate,todate):
    print('initialized pullprices.stockhistorybackfilledtodatframeofstockhistoryinstances')
    import pandas as pd
    import numpy as np
    from pandas.io.data import DataReader
    from datetime import datetime, timedelta
    

    #print(hist)
    date_format = "%Y-%m-%d"

    delta = timedelta(days=1)

    todate_date = datetime.strptime(todate, date_format)
    fromdate_date = datetime.strptime(fromdate, date_format)
    
    

    idates = 0
    d = datetime.strptime(fromdate, date_format)
    while d <= todate_date:
        idates = idates + 1
        d += delta
        
    # ##############
    # print(idates)

    #todays_date = datetime.datetime.now().date()
    index = pd.date_range(fromdate_date, periods=idates, freq='D')
    columns = [
     'Open',   'High',    'Low',  'Close',    'Volume',  'Adj Close', 'Back Filled',     
    ]
    dfnew = pd.DataFrame(index=index, columns=columns)
    dfnew = dfnew.fillna('NaN') # with 0s rather than NaNs
    
    # ############
    # print(dfnew)                 
    
    hist = DataReader(symbol,  "yahoo", fromdate,todate)
    
    # #########
    # print(hist)
    
    last_open = 'NaN'
    last_high = 'NaN'
    last_low = 'NaN'
    last_close = 'NaN'
    last_adjclose = 'NaN'
    last_volume = 'NaN'
    backfilled = 'NaN'
    
    d = datetime.strptime(fromdate, date_format)
    while d <= todate_date:
        d_string = d.strftime(date_format)
        
        #print(d_string)
        if d_string in hist.index:
            last_open = hist.ix[d_string]['Open']
            last_high = hist.ix[d_string]['High']
            last_low = hist.ix[d_string]['Low']
            last_close = hist.ix[d_string]['Close']
            last_volume = hist.ix[d_string]['Volume']
            last_adjclose = hist.ix[d_string]['Adj Close']
            backfilled = 0
            #print(d_string,last_adjclose)
        else:
            backfilled = 1
            #print(d_string,'nothing',last_adjclose)
            
        
        dfnew.ix[d_string]['Open'] = last_open 
        dfnew.ix[d_string]['High'] = last_high 
        dfnew.ix[d_string]['Low'] = last_low
        dfnew.ix[d_string]['Close'] = last_close        
        dfnew.ix[d_string]['Volume'] = last_volume
        dfnew.ix[d_string]['Adj Close'] = last_adjclose
        dfnew.ix[d_string]['Back Filled'] = backfilled
        
        d += delta
    
    #print(dfnew)
    return dfnew
    
def stock(symbol):
    """ 
    gets last traded price from yahoo for given security
    """        
    import pandas.io.data as pd 
    
    df = pd.get_quote_yahoo(symbol)
    #print(df)
    
    cols = ['PE', 'change_pct', 'last', 'short_ratio', 'time']
    result = pd.DataFrame(df, columns=cols)
    return result.iloc[0]['last']

def stockprice_realtime_to_dataframe(symbol):
    """ 
    gets last traded price from yahoo for given security
    """        
    import pandas.io.data as pd 
    
    df = pd.get_quote_yahoo(symbol)
    #print(df)
    
    cols = ['PE', 'change_pct', 'last', 'short_ratio', 'time']
    result = pd.DataFrame(df, columns=cols)
    return result #result.iloc[0]['last']
    
    
def options(symbol,expirationdate,pathtoexportfile,showresults=0):
    import lxml.html
    import calendar
    #import os

    #################################
    try:
        outstrings = {}
        outstrings[len(outstrings)] = "pullprices: trying"

        #total = len(sys.argv)
        #cmdargs = str(sys.argv)
        #print ("The total numbers of args passed to the script: %d " % total)
        #print ("Args list: %s " % cmdargs)
        # Pharsing args one by one 
        #print ("Script name: %s" % str(sys.argv[0]))

        #import inspect
        from datetime import datetime            
    
        #root = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\data"
        import os
        root = os.path.join(pathtoexportfile,symbol)
        
        #print ("Root: %s" % root)
        outstrings[len(outstrings)] = "Symbol: %s" % str(symbol)
        outstrings[len(outstrings)] = "Expiration: %s" % str(expirationdate)
        
        s_symbol  = str(symbol)
        d_expiration  = str(expirationdate)
    
        dt      = datetime.strptime(d_expiration, '%Y-%m-%d')
        ym      = calendar.timegm(dt.utctimetuple())
        url     = 'http://finance.yahoo.com/q/op?s=%s&date=%s' % (s_symbol, ym,)
        doc     = lxml.html.parse(url)
        table   = doc.xpath('//table[@class="details-table quote-table Fz-m"]/tbody/tr')
        
        rows    = []        
        for tr in table:
            d = [td.text_content().strip().replace(',','') for td in tr.xpath('./td')]
            rows.append(d)
        
        import csv
        
        length = len(rows[0])
        
        import datetime
        i = datetime.datetime.now()
        
        #print ("Current date & time = %s" % i)
        #print ("Date and time in ISO format = %s" % i.isoformat() )
        
        dateString = i.strftime('%Y%m%d%H%M%S')
        
        ##############################################
#        import shutil
#        shutil.rmtree(root, ignore_errors=True)
        ##############################################
        
        wildcardstringforfilestodelete = os.path.join(root,"Options " + s_symbol + ' ' + d_expiration + '*')        
        #print('checking for the existence of: ' + wildcardstringforfilestodelete)
        import glob
        for filename in glob.glob(wildcardstringforfilestodelete) :
            print('removing....  ' + filename)
            os.remove( filename )        
        
        make_sure_path_exists(root)
        # make sure root is clear of all file
        output = os.path.join(root,"Options " + s_symbol + ' ' + d_expiration + ' ' + dateString + '.csv')
        #output = root + "\Options " + s_symbol + ' ' + d_expiration + ' ' + dateString + '.csv'
        
        outstrings[len(outstrings)] = 'Output File: ' + output
        
        stockprice=stock(symbol)        
        
        with open(output, 'w') as test_file:
            csv_writer = csv.writer(test_file, lineterminator = '\n')
            for y in range(length):
                csv_writer.writerow([x[y] for x in rows])
            csv_writer.writerow([stockprice for x in rows])
    #################################
    except Exception as e:
        print("pullprices: There was a problem with this one......................................................pullprices")
        print("pullprices: ",str(e))
    else:
        outstrings = ("pullprices: Success")
    finally:
        if showresults == 1:
            for sout in outstrings:
                print(sout)
        #print("pullprices: Finally")
    #################################

def options_to_dataframe(symbol,expirationdate,showresults=0):
    import lxml.html
    import calendar
    #import os

    #################################
    try:
        outstrings = {}
        outstrings[len(outstrings)] = "pullprices: trying"

        #total = len(sys.argv)
        #cmdargs = str(sys.argv)
        #print ("The total numbers of args passed to the script: %d " % total)
        #print ("Args list: %s " % cmdargs)
        # Pharsing args one by one 
        #print ("Script name: %s" % str(sys.argv[0]))

        #import inspect
        from datetime import datetime            
    
        #root = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\data"
        #import os
        #root = os.path.join(pathtoexportfile,symbol)
        
        #print ("Root: %s" % root)
        outstrings[len(outstrings)] = "Symbol: %s" % str(symbol)
        outstrings[len(outstrings)] = "Expiration: %s" % str(expirationdate)
        
        s_symbol  = str(symbol)
        d_expiration  = str(expirationdate)
    
        dt      = datetime.strptime(d_expiration, '%Y-%m-%d')
        ym      = calendar.timegm(dt.utctimetuple())
        url     = 'http://finance.yahoo.com/q/op?s=%s&date=%s' % (s_symbol, ym,)
        doc     = lxml.html.parse(url)
        table   = doc.xpath('//table[@class="details-table quote-table Fz-m"]/tbody/tr')
        
        rows    = []        
        rows.append(['strike','optionsymbol','last','bid','ask','change','pctchange','volume','openinterest','impliedvolatility'])
        #print('pullprices options_to_dataframe len of table',len(table))
        if len(table) > 0:
            for tr in table:
                #print(tr)
                d = [td.text_content().strip().replace(',','') for td in tr.xpath('./td')]
                rows.append(d)
        
        #stockprice=stock(symbol)
 
        headers = rows.pop(0)
        df_stockprice_realtime_to_dataframe = stockprice_realtime_to_dataframe(symbol)
        
        import pandas as pd
        try:
            df = pd.DataFrame(rows, columns=headers)
            #print('got here')
            #import numpy as np
            stockprice = df_stockprice_realtime_to_dataframe.iloc[0]['last']
            time = df_stockprice_realtime_to_dataframe.iloc[0]['time']
            df['stockprice'] = stockprice
            df['time'] = time
        except:
            import numpy as np
            #rows.append(['strike','optionsymbol','last','bid','ask','change','pctchange','volume','openinterest','impliedvolatility'])
            df=pd.DataFrame(np.zeros(0,dtype=[
                ('strike', 'a50')
                ,  ('optionsymbol', 'a50')
                ,  ('last', 'f2')
                ,  ('ask', 'f2')
                ,  ('change', 'f2')
                ,  ('pctchange', 'f2')
                ,  ('volume', 'f2')
                ,  ('openinterest', 'f2')
                ,  ('impliedvolatility', 'a20')
                ]))
            #df = pd.DataFrame(rows, columns=headers)            
            print('pullprices options_to_dataframe could not create df',symbol,expirationdate)

        return df        
        print(rows.count,rows[0],stockprice)
        
    #################################
    except Exception as e:
        print("pullprices: There was a problem with this one......................................................pullprices")
        print("pullprices: ",str(e))
    else:
        outstrings = ("pullprices: Success")
    finally:
        if showresults == 1:
            for sout in outstrings:
                print(sout)
        #print("pullprices: Finally")
    #################################

def dayofweek_int(dayofweek_word):
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

def findnextoptionexpiration_datetimestring(self
        ,  symbol = 'SPY'
        ,  numberofweeksahead = 1
        ,  expirationday = 'friday' #'friday' #'wednesday for index'
    ):
    
        
    #import csv
    #import os
    #import mytools
    
    # ##########
    # Date setup
    import datetime
    #today_datetime = datetime.datetime.today()
    today_date = datetime.date.today()
    iter_date = today_date
    expirationdatetime_string = ''
    for expirationcounter in range(numberofweeksahead):
        if expirationcounter + 1 == numberofweeksahead:
            print('expirationcounter',expirationcounter) 
            print(' range(numberofweeksahead)', range(numberofweeksahead))
            while iter_date.weekday() != dayofweek_int(expirationday):
                iter_date += datetime.timedelta(1)    
            expirationdate_string = str(iter_date)
            expirationdatetime_string = expirationdate_string+' 16:00'
    return expirationdatetime_string
    
if __name__=='__main__':
    
    #options(sys.argv[1],sys.argv[2],sys.argv[3])
    symbol = 'NFLX'
    expiration_datetimestring = findnextoptionexpiration_datetimestring('NFLX')
    expiration_datestring = expiration_datetimestring.split()[0]
    df = options_to_dataframe(symbol,expiration_datestring)
    print(df)
    #print('hello')
    #myX = df.head(1).T
    #print(myX)
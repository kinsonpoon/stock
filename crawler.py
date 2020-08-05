import csv
import requests
import os
import sys
import pandas as pd

def get_list():
    from bs4 import BeautifulSoup
    result=[]
    
    page = requests.get("https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Hong_Kong_Stock_Exchange#0001_-_0099")
    soup = BeautifulSoup(page.content, 'html.parser')
    td=soup.findAll("td")
    #print(td)
    for href in td:
        stock=href.get_text(separator=" ")
        stock=stock.replace(":", "")
        mystring = " ".join(stock.split())
        if(mystring[0]=="S" and mystring[1]=="E"):
            details=mystring.split(" ", 2)
            result.append(details)
    print("crawl list of stock from wiki success")
    return result

def listoflists_to_csv(listoflists,name,myheader):
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    my_df = pd.DataFrame(listoflists)
    my_df.to_csv(script_dir+'/'+'data'+'/'+name+".csv", index=False, header=myheader)
    print("list to csv success")

def makelistofstocks():
    l=get_list()
    myheader=["country","id","name"]
    listoflists_to_csv(l,"stockslist",myheader)

def makehistorialdata(data,name):
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    my_df = pd.DataFrame(data[1:])
    my_df.to_csv(script_dir+'/'+'data'+'/'+name+".csv", index=False,header=data[0])
    print("list to csv success")

def get_data(stocknum,country):

    CSV_URL = 'https://query1.finance.yahoo.com/v7/finance/download/'+stocknum+'.'+country+'?period1=1564987348&period2=1596609748&interval=1d&events=history'


    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        return my_list

def list_data(csv):
    stockslist=pd.read_csv(csv)
    country="HK"
    stocks_num=stockslist['id']
    stocks_name=stockslist['name']

    for(num,name) in zip(stocks_num,stocks_name):
        numString="{:04d}".format(num)
        print(numString,name)
        data=get_data(numString,country)
        name="historical_data/"+numString+"_"+name+"_"+data[len(data)-1][0]
        try:
            makehistorialdata(data,name)
        except:
            pass

def main():
    #makelistofstocks()
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    csv=script_dir+'/data/stockslist.csv'
    list_data(csv)


if __name__ == "__main__":
    main()
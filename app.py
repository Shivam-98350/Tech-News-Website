import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

res1=requests.get('https://news.ycombinator.com/')
res2=requests.get('https://news.ycombinator.com/?p=2')
res3=requests.get('https://news.ycombinator.com/?p=3')
print(res1)
print(res2)
soup=BeautifulSoup(res1.text,'html.parser')
soup.append(BeautifulSoup(res2.text,'html.parser'))
soup.append(BeautifulSoup(res3.text,'html.parser'))
links=soup.select('.titleline')
subtext=soup.select('.subtext')
def sort_stories_by_votes(hnlist):
    return sorted(hnlist,key=lambda k:k['votes'],reverse=True)

def create_custom_hn(links):
    hn=[]
    for idx,item in enumerate(links):
        title=links[idx].getText()
        a_tag = links[idx].find('a')
        href=a_tag.get('href',None)
        vote = subtext[idx].select('.score ')
        if len(vote):
         points=int(vote[0].getText().replace(' points',""))
         if(points>100):
            hn.append({'title':title,'link':href,'votes':points})
    return sort_stories_by_votes(hn)






@app.route('/')
def index():
    data=create_custom_hn(links)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
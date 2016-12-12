import urllib.request
import re
import time,math,random


def scrape(source,keystr,endchar):
    results = []
    for m in re.finditer(keystr,source):
        start = m.end()
        end = None
        for i in range(0,50):
            if source[start+i] == endchar:
                end = start+i
                break
        if end != None:
            results.append(source[start:end])
    return(results)

def scrapeBackwards(source,keystr,startchar):
    results = []
    for m in re.finditer(keystr,source):
        end = m.start()
        start = None
        for i in range(0,250):
            if source[end-i-1] == startchar:
                start = end-i
                break
        if start != None:
            results.append(source[start:end])
    return(results)

location = []
def searchLocation():
    global location
    location = []
    source = (urllib.request.urlopen("http://www.accuweather.com/en/browse-locations").read()).decode()
    choices = scrapeBackwards(source,'''</em></a></h6>''','>')
    for i in choices[:len(choices)-1]:
        print(i,end=', ')
    print()
    loc = input("Choice: ")

    #while len(scrape(source,'''<li class="drilldown cl" data-href="h''','"')) > 0 and not 'weather-forecast' in 'h'+scrape(source,'''<li class="drilldown cl" data-href="h''','"')[0]:
    for l in range(3):
        urls = scrapeBackwards(source.lower(),'''"><em>%s</em>'''%loc.lower(),'"')
        locURL = urls[len(urls)-1]
        source = (urllib.request.urlopen(locURL).read()).decode()
        choices = scrapeBackwards(source,'''</em></a></h6>''','>')
        for i in choices[:len(choices)-1]:
            print(i,end=', ')
        print()
        loc = input("Choice: ")
        location.append(loc)

    locURL = scrapeBackwards(source.lower(),'''"><em>%s</em>'''%loc.lower(),'"')[0]
    source = (urllib.request.urlopen(locURL).read()).decode()

    locNum = locURL.split('/')
    locNum = locNum[len(locNum)-1]
    return(locNum)
    """
    locNum = 0
    for m in re.finditer('''<li class="drilldown cl" data-href="''',source):
        start = m.end()
        end = start
        for i in range(0,250):
            if source[m.end()+i] == '"':
                end = m.end()+i
                break
        if '-'.join(loc.split()) in source[start:end]:
            splitURL = source[start:end].split('/')
            locNum = splitURL[len(splitURL)-1]
    print(locNum)
    return(locNum)
    """

def weatherData():
    global location
    if input("Browse for location? y/n ").startswith('y'):
        url = "http://www.accuweather.com/en/n/n/n/current-weather/%s"%searchLocation()
        source = (urllib.request.urlopen(url).read()).decode()
        #print(url)
    else:
        id = input('Enter ID: ')
        source = (urllib.request.urlopen("http://www.accuweather.com/en/n/n/n/current-weather/"+id).read()).decode()
        location = [id]
    #else:
    #    source = (urllib.request.urlopen("http://www.accuweather.com/en/n/n/n/current-weather/%s"%input("ID: ")).read()).decode()
    data = {"Temperature":0,"Conditions":''}
    #print(source)
    for i in location:
        print(i,end=' > ')
    print('current weather')

    temp = scrape(source,'''<span class="large-temp">''','&')
    #print(temp)
    data["Temperature"] = temp[len(temp)-1]
    cond = scrape(source,'''<span class="cond">''','<')
    #print(cond)
    data["Conditions"] = cond[len(cond)-1]
    wind = scrape(source,'''<li class="wind"><strong>''',' ')
    #print(wind)
    data["Wind"] = wind[len(wind)-1]

    return(data)


def findMatch(names,levels):
    global data
    for n in names:
        for lvl in range(len(levels)):
            for i in levels[lvl]:
                foundN = (data["Conditions"].lower()).find(n)
                foundI = (data["Conditions"].lower()).find(i)
                if i in data["Conditions"].lower()[foundI:foundN+1]:
                    return((1+(lvl*3))/2)
    for n in names:
        if n in data["Conditions"].lower():
            return(1)
    return(0)

def getConditions():
    global conditions,data
    levels = [['some','partly','little','light','decreasing','less','rather'],['considerabl','more','heavy','mostly','increasing']]

    names = ['cloud']
    conditions['cloudy'] = findMatch(names,levels)

    names = ['rain','shower']
    conditions['rain'] = findMatch(names,levels)

    if 'sun' in data["Conditions"].lower():
        conditions['sunny'] = 2

    names = ['fog','haz']
    conditions['fog'] = findMatch(names,levels)

    names = ['snow']
    conditions['snow'] = findMatch(names,levels)


    if 'thunder' in data["Conditions"].lower():
        conditions['storm'] = 1
        #conditions['wind'] = 4
        conditions['rain'] = 2
        conditions['cloudy'] = 1
    elif 'storm' in data["Conditions"].lower():
        conditions['storm'] = 1
        #conditions['wind'] = 4
        conditions['rain'] = 2
        conditions['cloudy'] = 1
    if 'tornado' in data["Conditions"].lower():
        conditions['storm'] = 2
        #conditions['wind'] = 10
        conditions['rain'] = 2
        conditions['cloudy'] = 1.5

    #conditions = {'cloudy':0,'rain':0,'storm':0,'sunny':0,'wind':0}


    if conditions['cloudy'] < conditions['storm']:
        conditions['cloudy'] = conditions['storm']

    if conditions['rain'] > 0 and not conditions['cloudy'] > 0:
        conditions['cloudy'] = conditions['rain']

    if conditions['snow'] > 0 and not conditions['cloudy'] > 0:
        conditions['cloudy'] = conditions['snow']

    if conditions['cloudy'] > 2:
        conditions['cloudy'] = 2

    #if conditions['cloudy'] > 0 and not conditions['wind'] > 0:
    #    conditions['wind'] = conditions['cloudy']/2

    #if conditions['rain'] > conditions['wind']:
    #    conditions['wind'] = conditions['rain']/4


    #print()
    #print(conditions)

def animate(cloud,rain,storm,sunny,wind,fog,snow):
    global conditions,data,play
    try:
        screen.bgcolor(100-(storm*10)+(sunny*20),100-(storm*10)+(sunny*20),150-(storm*20)+(sunny*20))
    except:
        dif1 = (100-(storm*10)+(sunny*50))
        if dif1 < 0:
            dif1 = 0
        else:
            dif1 = 255
        dif2 = (150-(storm*20)+(sunny*50))
        if dif2 < 0:
            dif2 = 0
        else:
            dif2 = 255
        screen.bgcolor(dif1,dif1,dif2)
    #print(screen.bgcolor())

    posX = []
    posY = []
    size = []
    color = []

    fogPos = []
    if fog > 0:
        for x in range(0,int(fog*5)):
            fogPos.append([random.randint(-600,-200),random.randint(-400,400)])

    snowPos = []
    if snow > 0:
        for x in range(0,int(snow*20)):
            snowPos.append([random.randint(-400,400),random.randint(-400,400)])

    for x in range(0,cloud):
        posX.append(random.randint(-420,420))
        posY.append(random.randint(300-int(cloud*1.5),320))
        size.append(random.randint(120,190))
        color.append(random.randint(200,255)-int(storm*20))

    sunAngles = []

    t.hideturtle()

    play = True

    def stopPlaying(event):
        global play
        play = False
        print()
    
    canvas = turtle.getcanvas()
    canvas.bind_all("<Return>",stopPlaying)
    
    i=0
    while play:
        if i%(1+(10-wind))==0:
            del posX[0]
            del posY[0]
            del size[0]
            del color[0]
            posX.append(random.randint(-420,420))
            posY.append(random.randint(300-int(cloud*1.5),320))
            size.append(random.randint(120,190))
            color.append(random.randint(200,255)-int(storm*20))
        if sunny > 0:
            t.up()
            t.goto(-400,200)
            t.down()
            if i%10==0:
                sunAngles = []
                for e in range(0,random.randint(10,20)+(sunny*2)):
                    sunAngles.append(random.randint(-180,180))
            t.color(255,255,255)
            for a in sunAngles:
                t.seth(a+random.randint(-1,1))
                t.forward(1000)
                t.back(1000)
            if not 150+sunny*50 > 255:
                t.color(150+sunny*50,150+sunny*50,150)
            else:
                t.color(255,255,150)
            t.dot(500+random.randint(-1,1))
            t.color(255,222,0)
            t.dot(225+random.randint(-1,1))
        if fog > 0:
            t.seth(0)
            t.pensize(fog*300)
            rgb = int((int(screen.bgcolor()[0])+int(screen.bgcolor()[1])+int(screen.bgcolor()[2]))/3)
            if not rgb-10 > 255 and not rgb-10 < 0 and not rgb+25 > 255 and not rgb+25 < 0:
                t.color(rgb-10,rgb-10,rgb+25)
            else:
                t.color(125,125,160)
            for f in range(len(fogPos)):
                fogPos[f] = [fogPos[f][0]+0.4,fogPos[f][1]+(random.randint(-1,1)/10)]
                t.up()
                t.goto(fogPos[f][0],fogPos[f][1])
                t.down()
                t.forward(250)
                if fogPos[f][0] > 400:
                    del fogPos[f]
                    fogPos.append([random.randint(-600,-200),random.randint(-400,400)])
            t.pensize(1)
        if snow > 0:
            t.seth(0)
            t.color(255,255,255)
            for s in range(len(snowPos)):
                snowPos[s] = [snowPos[s][0]+(random.randint(-1,1)/10),snowPos[s][1]-random.randint(1,2)]
                t.up()
                t.goto(snowPos[s][0],snowPos[s][1])
                t.down()
                for i in range(0,10):
                    t.left(36)
                    t.forward(15)
                    t.back(15)
                if snowPos[s][1] < -400:
                    del snowPos[s]
                    snowPos.append([random.randint(-400,400),random.randint(300,400)])
            t.pensize(1)
        for a in range(0,cloud):
            if color[a] + (sunny*4) <= 255:
                t.color(color[a]+(sunny*4),color[a]+(sunny*4),color[a])
            else:
                t.color(255,255,255)
            if random.randint(0,1) == 0:
                posX[a] = posX[a]+(random.randint(0,int(wind*10))/10)
                posY[a] = posY[a]+(random.randint(0,int(wind*10))/20)
                size[a] = size[a]+(random.randint(0,2)/2)
            else:
                posX[a] = posX[a]-(random.randint(0,int(wind*10))/10)
                posY[a] = posY[a]-(random.randint(0,int(wind*10))/20)
                size[a] = size[a]-(random.randint(0,2)/2)
            t.up()
            t.goto(posX[a]+(a/2),posY[a])
            t.down()
            if not conditions['cloudy'] <= 0:
                t.dot(size[a])
            if rain > 0 and random.randint(0,30-int(rain*10)) == 0:
                t.color(0,0,180)
                t.seth(270)
                t.forward(320)
            if wind > 0 and random.randint(0,1000-int(wind*100)) == 0:
                t.color(222,222,222)
                t.up()
                t.goto(random.randint(-400,400),random.randint(-400,300))
                t.seth(random.randint(-10,10))
                t.down()
                t.forward(random.randint(10,50))
                if wind > 4 and random.randint(0,20) == 0:
                    loc = [random.randint(-400,400),random.randint(-400,300)]
                    for b in range(0,random.randint(1,int(wind))):
                        t.up()
                        t.goto(loc[0]+random.randint(-100,100),loc[1]-(b*15))
                        t.seth(0)
                        t.down()
                        t.forward(random.randint(100,500))
            if storm > 0 and random.randint(0,1600-int(storm*100)) == 0:
                screen.bgcolor(255,255,255)
                t.color(255,255,125)
                t.seth(270)
                for b in range(0,random.randint(1,2)):
                    num = random.randint(-90,90)
                    t.forward(160)
                    t.left(num)
                    t.forward(200)
                    t.back(200)
                    t.right(num)
                    t.back(160)
                    t.forward(random.randint(0,100))
        t.up()
        t.goto(-len(data["Conditions"])*12,-50)
        t.down()
        rgb = int((int(screen.bgcolor()[0])+int(screen.bgcolor()[1])+int(screen.bgcolor()[2]))/3)
        t.color(255-rgb,255-rgb,255-rgb)
        t.write(data["Conditions"],font=("Comic Sans MS",40))
        turtle.update()
        try:
            screen.bgcolor(100-(storm*10)+(sunny*50),100-(storm*10)+(sunny*50),150-(storm*20)+(sunny*50))
        except:
            dif1 = (160-(storm*10)+(sunny*50))
            if dif1 < 0:
                dif1 = 0
            else:
                dif1 = 255
            dif2 = (220-(storm*20)+(sunny*50))
            if dif2 < 0:
                dif2 = 0
            else:
                dif2 = 255
            screen.bgcolor(dif1,dif1,dif2)
        t.reset()
        t.hideturtle()
        i=i+1
    t.reset()

#data['Wind'] = '100'

#data['Conditions'] = 'tornado'

import turtle
t = turtle.Pen()
turtle.tracer(0,0)

play = False
while True:
    conditions = {'cloudy':0,'rain':0,'storm':0,'sunny':0,'wind':0,'snow':0,'fog':0}
    data = weatherData()
    conditions['wind'] = int(data['Wind'])/10
    print()
    for i in data:
        print("%s: %s"%(i,data[i]))

    getConditions()
    
    screen = turtle.Screen()
    screen.colormode(255)

    cloud = 1+int(conditions['cloudy']*40)
    rain = (conditions['rain'])
    storm = (conditions['storm'])
    sunny = int(conditions['sunny'])
    wind = conditions['wind']
    fog = conditions['fog']
    snow = conditions['snow']

    animate(cloud,rain,storm,sunny,wind,fog,snow)


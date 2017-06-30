import requests,json,random
import turtle

appid = 'a98689d8418b0ca737434c67064bb29d'


def coordinates():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return [lat,lon]


def weather_geoloc(coordinates):
    global appid
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s'%(coordinates[0],coordinates[1],appid))
    return r.json()


def weather(loc):
    global appid
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s'%(loc,appid))
    return r.json()


def findMatch(names, levels):
    global data
    for n in names:
        for lvl in range(len(levels)):
            for i in levels[lvl]:
                foundN = (data["Conditions"].lower()).find(n)
                foundI = (data["Conditions"].lower()).find(i)
                if i in data["Conditions"].lower()[foundI:foundN + 1]:
                    return ((1 + (lvl * 3)) / 2)
    for n in names:
        if n in data["Conditions"].lower():
            return (1)
    return (0)


def get_conditions(data):
    conds = {'cloudy': 0, 'rain': 0, 'storm': 0, 'sunny': 0, 'wind': 0, 'snow': 0, 'fog': 0}
    conds['wind'] = data['Wind']

    levels = [['some', 'partly', 'little', 'light', 'decreasing', 'less', 'rather'],
              ['considerabl', 'more', 'heavy', 'mostly', 'increasing']]

    names = ['cloud']
    conds['cloudy'] = findMatch(names,levels)

    names = ['rain','shower']
    conds['rain'] = findMatch(names,levels)

    if 'sun' in data["Conditions"].lower():
        conds['sunny'] = 2

    names = ['fog','haz']
    conds['fog'] = findMatch(names,levels)

    names = ['snow']
    conds['snow'] = findMatch(names,levels)

    if 'thunder' in data["Conditions"].lower():
        conds['storm'] = 1
        #conds['wind'] = 4
        conds['rain'] = 2
        conds['cloudy'] = 1
    elif 'storm' in data["Conditions"].lower():
        conds['storm'] = 1
        #conds['wind'] = 4
        conds['rain'] = 2
        conds['cloudy'] = 1
    if 'tornado' in data["Conditions"].lower():
        conds['storm'] = 2
        #conds['wind'] = 10
        conds['rain'] = 2
        conds['cloudy'] = 1.5

    if conds['cloudy'] < conds['storm']:
        conds['cloudy'] = conds['storm']

    if conds['rain'] > 0 and not conds['cloudy'] > 0:
        conds['cloudy'] = conds['rain']

    if conds['snow'] > 0 and not conds['cloudy'] > 0:
        conds['cloudy'] = conds['snow']

    if conds['cloudy'] > 2:
        conds['cloudy'] = 2

    return conds


def animate(conds):
    global data, play

    cloud = 1 + int(conds['cloudy'] * 40)
    rain = (conds['rain'])
    storm = (conds['storm'])
    sunny = int(conds['sunny'])
    wind = conds['wind']
    fog = conds['fog']
    snow = conds['snow']

    try:
        screen.bgcolor(100 - (storm * 10) + (sunny * 20), 100 - (storm * 10) + (sunny * 20),
                       150 - (storm * 20) + (sunny * 20))
    except:
        dif1 = (100 - (storm * 10) + (sunny * 50))
        if dif1 < 0:
            dif1 = 0
        else:
            dif1 = 255
        dif2 = (150 - (storm * 20) + (sunny * 50))
        if dif2 < 0:
            dif2 = 0
        else:
            dif2 = 255
        screen.bgcolor(dif1, dif1, dif2)

    posX = []
    posY = []
    size = []
    color = []

    fogPos = []
    if fog > 0:
        for x in range(0, int(fog * 5)):
            fogPos.append([random.randint(-600, -200), random.randint(-400, 400)])

    snowPos = []
    if snow > 0:
        for x in range(0, int(snow * 20)):
            snowPos.append([random.randint(-400, 400), random.randint(-400, 400)])

    for x in range(0, cloud):
        posX.append(random.randint(-420, 420))
        posY.append(random.randint(300 - int(cloud * 1.5), 320))
        size.append(random.randint(120, 190))
        color.append(random.randint(200, 255) - int(storm * 20))

    sunAngles = []

    t.hideturtle()

    play = True

    def stopPlaying(event):
        global play
        play = False
        print()

    canvas = turtle.getcanvas()
    canvas.bind_all("<Return>", stopPlaying)

    i = 0
    while play:
        if i % (1 + int(10/wind)) == 0:
            del posX[0]
            del posY[0]
            del size[0]
            del color[0]
            posX.append(random.randint(-420, 420))
            posY.append(random.randint(300 - int(cloud * 1.5), 320))
            size.append(random.randint(120, 190))
            color.append(random.randint(200, 255) - int(storm * 20))
        if sunny > 0:
            t.up()
            t.goto(-400, 200)
            t.down()
            if i % 10 == 0:
                sunAngles = []
                for e in range(0, random.randint(10, 20) + (sunny * 2)):
                    sunAngles.append(random.randint(-180, 180))
            t.color(255, 255, 255)
            for a in sunAngles:
                t.seth(a + random.randint(-1, 1))
                t.forward(1000)
                t.back(1000)
            if not 150 + sunny * 50 > 255:
                t.color(150 + sunny * 50, 150 + sunny * 50, 150)
            else:
                t.color(255, 255, 150)
            t.dot(500 + random.randint(-1, 1))
            t.color(255, 222, 0)
            t.dot(225 + random.randint(-1, 1))
        if fog > 0:
            t.seth(0)
            t.pensize(fog * 300)
            rgb = int((int(screen.bgcolor()[0]) + int(screen.bgcolor()[1]) + int(screen.bgcolor()[2])) / 3)
            if not rgb - 10 > 255 and not rgb - 10 < 0 and not rgb + 25 > 255 and not rgb + 25 < 0:
                t.color(rgb - 10, rgb - 10, rgb + 25)
            else:
                t.color(125, 125, 160)
            for f in range(len(fogPos)):
                fogPos[f] = [fogPos[f][0] + 0.4, fogPos[f][1] + (random.randint(-1, 1) / 10)]
                t.up()
                t.goto(fogPos[f][0], fogPos[f][1])
                t.down()
                t.forward(250)
                if fogPos[f][0] > 400:
                    del fogPos[f]
                    fogPos.append([random.randint(-600, -200), random.randint(-400, 400)])
            t.pensize(1)
        if snow > 0:
            t.seth(0)
            t.color(255, 255, 255)
            for s in range(len(snowPos)):
                snowPos[s] = [snowPos[s][0] + (random.randint(-1, 1) / 10), snowPos[s][1] - random.randint(1, 2)]
                t.up()
                t.goto(snowPos[s][0], snowPos[s][1])
                t.down()
                for i in range(0, 10):
                    t.left(36)
                    t.forward(15)
                    t.back(15)
                if snowPos[s][1] < -400:
                    del snowPos[s]
                    snowPos.append([random.randint(-400, 400), random.randint(300, 400)])
            t.pensize(1)
        for a in range(0, cloud):
            if color[a] + (sunny * 4) <= 255:
                t.color(color[a] + (sunny * 4), color[a] + (sunny * 4), color[a])
            else:
                t.color(255, 255, 255)
            r = lambda: int((10-(10/wind)) * 10) if wind >= 1 else 0
            if random.randint(0, 1) == 0:
                posX[a] += random.random()*r() / 10
                posY[a] += random.random()*r() / 20
                size[a] += random.random()
            else:
                posX[a] -= random.random()*r() / 10
                posY[a] -= random.random()*r() / 20
                size[a] -= random.random()
            t.up()
            t.goto(posX[a] + (a / 2), posY[a])
            t.down()
            if not conds['cloudy'] <= 0:
                t.dot(size[a])
            if rain > 0 and random.randint(0, 30 - int(rain * 10)) == 0:
                t.color(0, 0, 180)
                t.seth(270)
                t.forward(320)
            if wind > 0 and random.randint(0, round((10/wind) * 10)) == 0:
                t.color(222, 222, 222)
                t.up()
                t.goto(random.randint(-400, 400), random.randint(-400, 300))
                t.seth(random.randint(-10, 10))
                t.down()
                t.forward(random.randint(10, 100))
                if 10-(10/wind) > 4 and random.randint(0, 20) == 0:
                    loc = [random.randint(-400, 400), random.randint(-400, 300)]
                    for b in range(0, random.randint(1, 10-int(10/wind))):
                        t.up()
                        t.goto(loc[0] + random.randint(-100, 100), loc[1] - (b * 15))
                        t.seth(0)
                        t.down()
                        t.forward(random.randint(100, 500))
            if storm > 0 and random.randint(0, 1600 - int(storm * 100)) == 0:
                screen.bgcolor(255, 255, 255)
                t.color(255, 255, 125)
                t.seth(270)
                for b in range(0, random.randint(1, 2)):
                    num = random.randint(-90, 90)
                    t.forward(160)
                    t.left(num)
                    t.forward(200)
                    t.back(200)
                    t.right(num)
                    t.back(160)
                    t.forward(random.randint(0, 100))
        t.up()
        t.goto(-len(data["Conditions"]) * 12, -50)
        t.down()
        rgb = int((int(screen.bgcolor()[0]) + int(screen.bgcolor()[1]) + int(screen.bgcolor()[2])) / 3)
        t.color(255 - rgb, 255 - rgb, 255 - rgb)
        t.write(data["Conditions"], font=("Comic Sans MS", 40))
        turtle.update()
        try:
            screen.bgcolor(100 - (storm * 10) + (sunny * 50), 100 - (storm * 10) + (sunny * 50),
                           150 - (storm * 20) + (sunny * 50))
        except:
            dif1 = (160 - (storm * 10) + (sunny * 50))
            if dif1 < 0:
                dif1 = 0
            else:
                dif1 = 255
            dif2 = (220 - (storm * 20) + (sunny * 50))
            if dif2 < 0:
                dif2 = 0
            else:
                dif2 = 255
            screen.bgcolor(dif1, dif1, dif2)
        t.reset()
        t.hideturtle()
        i += 1
    t.reset()


t = turtle.Pen()
turtle.tracer(0, 0)

screen = turtle.Screen()
screen.colormode(255)


def answer(question,acceptable_answers,tryagain="Unacceptable answer, please try again "):
	a = input(question)
	while a not in acceptable_answers:
		a = input(tryagain)
	return a

while True:
    if answer('Use current location (c) or manually enter location (m) ',('c','m')) == 'm':
        detecto=input('Enter coordinates, address, or city. ').split()
        if detecto[0].isdigit() and detecto[1].isdigit():
            weather_data = weather_geoloc(detecto)
        else:
            weather_data = weather(detecto)
        while 'weather' not in weather_data:
            print("Invalid Location. Please try again. ")
            detecto=input('Enter coordinates, address, or city. ').split()
            if detecto[0].isdigit() and detecto[1].isdigit():
                weather_data = weather_geoloc(detecto)
            else:
                weather_data = weather(detecto)
    else:
        print('Using current location')
        weather_data = weather_geoloc(coordinates())
    data = {'Name':weather_data['name'],
            'Conditions':' \n '.join([i['description'] for i in weather_data['weather']]),
            'Wind':weather_data['wind']['speed'],
            'Temperature':round(float(weather_data['main']['temp'])*1.8-459.67, 1)}
    print(data)

    # conditions = {'cloudy': 0, 'rain': 0, 'storm': 0, 'sunny': 0, 'wind': 100, 'snow': 0, 'fog': 0}
    conditions = get_conditions(data)

    animate(conditions)
    print()

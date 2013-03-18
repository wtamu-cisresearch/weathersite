import feedparser

d = feedparser.parse('http://weather.yahooapis.com/forecastrss?w=12792438&u=f')
print d['feed']['yweather_wind']
print d['feed']['yweather_atmosphere']
print d.entries[0].yweather_condition

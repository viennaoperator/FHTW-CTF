import config, urllib2

urlString = "http://" + config.PORTAL_URL + ":" + config.PORTAL_PORT + "/checkRunTime"

print urllib2.urlopen(urlString).read()

str = "https://es.foursquare.com/dreamguy2/checkin/53155dd4498e6e99a24d199e?s=tZpub3CX1MOO2odFSd_sufUJkvk&ref=tw";
params = str.split('/')
keys = params[len(params)-1].split('?')
checkin_id = keys[0]
lastvars = keys[1].split('&')
almost_signature = lastvars[0].split('=')
signature = almost_signature[1]
print checkin_id
print signature
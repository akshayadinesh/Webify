from flask import Flask, render_template, request
import os
import json
import oauth2 as oauth

app = Flask(__name__)
style = "style1"

consumer_key = "AZydwOuLK6qu9QW73DyKCuLKd"
consumer_secret = "OUPxrDmZVlerLgRYQusw9Ge9QjmWzp211KAG23iFgSdrKajdnl"

access_token = "996239807310434304-ekdJzyfg8Y4fRldHP38yROmAhVoeotq"
access_secret = "zOw1pikKkJAnzVBIdIotbxxKGKhAINTKGKxDCS4S7AUBh"

consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
access_token = oauth.Token(key=access_token, secret=access_secret)
client = oauth.Client(consumer, access_token)

@app.route('/')
def enterLink():
	return render_template('home.html')

@app.route('/customize/<string:username>')
def customize(username):
	banner_endpoint = "https://api.twitter.com/1.1/users/show.json?screen_name=" + username
	response, data = client.request(banner_endpoint)
	tweet_data = json.loads(data.decode())
	response = createNewDict(tweet_data, username)
	return render_template('customize.html', response=response, username=username)

@app.route('/display_page/<string:username>')
def show(username):
	banner_endpoint = "https://api.twitter.com/1.1/users/show.json?screen_name=" + username
	response, data = client.request(banner_endpoint)
	tweet_data = json.loads(data.decode())
	response = createNewDict(tweet_data, username)

	style = request.args.get('style')
	if(style == "style1"):
		return render_template('style1.html', response=response, username=username)
	elif(style == "style2"):
		return render_template('style2.html', response=response, username=username, darker=colorscale(response["profile_link_color"],0.5), lighter=colorscale(response["profile_link_color"],1))
	elif(style == "style3"):
		return render_template('style1.html', response=response, username=username)
	elif(style == "style4"):
		return render_template('style2.html', response=response, username=username)
	else:
		return render_template('page.html')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)

def createNewDict(tweet_data, username):
	categories = ["name", "location", "description", "created_at", "followers_count", "profile_image_url", "profile_banner_url", "profile_link_color", "image_url"]
	organized_dict = {}
	for category in categories:
		for key, val in tweet_data.items():
			if (key == category):
				organized_dict[category] = val
	profile_url = organized_dict["profile_image_url"]
	profile_url = profile_url.replace("_normal", "")
	organized_dict["profile_image_url"] = profile_url

	media_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&count=20&include_rts=False&exclude_replies=True"

	response, data = client.request(media_endpoint)

	tweet_media = json.loads(data.decode())

	for tweet in tweet_media:
		# print tweet['text']
		# print tweet['entities']
		for key, val in tweet.items():
			if (key == 'entities'):
				entities = tweet['entities']
				for key, val in entities.items():
					if(key == "media"):
						media = val
						organized_dict['image_url'] = media[0]['media_url']
						break

	return organized_dict

def colorscale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> colorscale("#DF3C3C", .5)
    #6F1E1E
    >>> colorscale("#52D24F", 1.6)
    #83FF7E
    >>> colorscale("#4F75D2", 1)
    #4F75D2
    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = clamp(r * scalefactor)
    g = clamp(g * scalefactor)
    b = clamp(b * scalefactor)

    return "#%02x%02x%02x" % (r, g, b)
def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

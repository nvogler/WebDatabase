album();
function picview(picid){
	//window.pushState(null,null,"/fcda9697ef8a4a3aac8d/pa3/pic?id=" + picid);
	window.location="/fcda9697ef8a4a3aac8d/pa3/pic?id=" + picid;
};
function album(){
	var query = window.location.search.substring(1);
	var vars = query.split("=");
	var albumid = vars[1];
	var req = new XMLHttpRequest();
	req.open("GET", "/api/v1/album/"+albumid, true);
	req.setRequestHeader("Content-type","application/json");

	req.onreadystatechange = function(){
		if (req.readyState == 4 && req.status == 200){
			var response= JSON.parse(req.response);
			var html = '<p align = \"center\" class=\"important\">Pictues from <b>';
			html += response.title + '</b><br>'
			html += "<p align=\"center\">";
			var length = response.pics.length;
			for (var i = 0; i < length; ++i)
			{
				var pic = response.pics[i]; 
				html += '<a onclick=\"picview(\'' + pic.picid;
				html += '\')\" align=\"center\" id=\"pic_' + pic.picid;
				html += '_link\"><img src=\"/static/images/';
				html += pic.picid + '.' + pic.format + '\" height=\"100\"' + ' width = \"100\"></a>';
			}
			html += "</p>";
			document.getElementById("content").innerHTML = html;
		}
	}
	req.send();
	
};


# -*- coding: utf-8 -*-
import sys
import numpy as np

def fib(num):
	former = 0
	latter = 1
	for (x in range(0, num):
		swapvar = former
		former = latter
		latter += swapvar
	return former
	
for line in sys.stdin:
    print fib(int(line))

	
	
	import sys

###Trade
#key #value #quantity #sequence number

#M = moving wieghted average
#Q = total quantity
#q = current quantity
#v = current value


for line in sys.stdin:
	#Parses input
	#Resets vars

	key_map = {}
	key_totals = {}
	seq_limit = 0
	#Breaks line into trades
	input_splits = line.split(';')
	for x in input_splits:
		
		#Breaks trade in components
		trade_split = x.split(',')
		
		#Checks seq number
		if (int(trade_split[3]) >= seq_limit):
			seq_limit = int(trade_split[3])
		else:
			continue
		
		#Assumes clean input
		trade = []
		#Value
		trade.append(trade_split[1])
		#Quantity
		trade.append(trade_split[2])
		
		#Key exists, append
		if trade_split[0] in key_map.keys():
			key_map[trade_split[0]].append(trade)
		#DNE, add
		else:
			key_val = trade_split[0]
			key_map[key_val] = trade
			
			output_string = str(key_val) + ": " + str(key_map[key_val][0])
			key_totals[key_val] = (key_map[key_val][0], key_map[key_val][0])
			
			print output_string

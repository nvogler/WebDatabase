import os, sys, fnmatch, hashlib

sqlfile = open("load_data.sql", "w")
sqlfile.write("INSERT INTO User VALUES('sportslover', 'Paul', 'Walker', 'sha512$8ec61415f1eb4afba45fa95e164a73e5$a8156f5e122a936e55512ccad145e72581c20853d8ceee8fc4ab535bead173dfb6625dd1d0eaccc9ace73008c135ef5eecb0b452470d007fde088602659ad9a2', 'sportslover@hotmail.com');\n")
sqlfile.write("INSERT INTO User VALUES('traveler', 'Rebecca', 'Travolta', 'sha512$1c662feb81e84cd78cf8d6a96e912ebb$eed150f49e6669c4aee79b0f1ed238ec557e8a6dc1af8c8b4dd393a1a6f0926b97bb537fc7a7af95db36982eaa90a313d4968cdc03112321e9dbb3c4aba65337', 'rebt@explorer.org');\n")
sqlfile.write("INSERT INTO User VALUES('spacejunkie', 'Bob', 'Spacey', 'sha512$523bbfca143d4676b5ecfc8ee42aca6d$fae41640d635cb42c3631e5a66a997e6f6ebfd25f6bb3f9777107d848c24bd2db9767242e803a881dbc5af73ddbf7ee80d1d855db2568061bfb2ca21fcf2dd5f', 'bspace@spacejunkies.net');\n\n")
sqlfile.write("INSERT INTO Album (title, created, lastupdated, username, access) VALUES('I love sports', \'2016-01-01\', \'2016-01-01\', 'sportslover', 'public');\n")
sqlfile.write("INSERT INTO Album (title, created, lastupdated, username, access) VALUES('I love football', \'2016-01-01\', \'2016-01-01\', 'sportslover', 'private');\n")
sqlfile.write("INSERT INTO Album (title, created, lastupdated, username, access) VALUES('Around The World', \'2016-01-01\', \'2016-01-01\', 'traveler', 'public');\n")
sqlfile.write("INSERT INTO Album (title, created, lastupdated, username, access) VALUES('Cool Space Shots', \'2016-01-01\', \'2016-01-01\', 'spacejunkie', 'private');\n\n")

imgfiles = os.listdir("static\images")

username_sports = 'sportslover'
username_world = 'traveler'
username_space = 'spacejunkie'
albumtitle_sports = 'I love sports'
albumtitle_football = 'I love football'
albumtitle_world = 'Around The World'
albumtitle_space = 'Cool Space Shots'
filename_sports = []
filename_football = []
filename_world = []
filename_space = []
seqnum_sports = 0
seqnum_football = 0
seqnum_world = 0
seqnum_space = 0

os.chdir("static\images")
for file in imgfiles:
    if (fnmatch.fnmatch(file, 'sports*.jpg')):
        m = hashlib.md5(username_sports + albumtitle_sports + file)
        sqlfile.write("INSERT INTO Photo VALUES(\'" + m.hexdigest() + "\', 'jpg', \'2016-01-01\');\n")
        filename_sports.append(m)
    if (fnmatch.fnmatch(file, 'football*.jpg')):
        m = hashlib.md5(username_sports + albumtitle_football + file)
        sqlfile.write("INSERT INTO Photo VALUES(\'" + m.hexdigest() + "\', 'jpg', \'2016-01-01\');\n")
        filename_football.append(m)
    if (fnmatch.fnmatch(file, 'world*.jpg')):
        m = hashlib.md5(username_world + albumtitle_world + file)
        sqlfile.write("INSERT INTO Photo VALUES(\'" + m.hexdigest() + "\', 'jpg', \'2016-01-01\');\n")
        filename_world.append(m)
    if (fnmatch.fnmatch(file, 'space*.jpg')):
        m = hashlib.md5(username_space + albumtitle_space + file)
        sqlfile.write("INSERT INTO Photo VALUES(\'" + m.hexdigest() + "\', 'jpg', \'2016-01-01\');\n")
        filename_space.append(m)
    
    ## print(file)
    os.rename(file, m.hexdigest() + ".jpg")
sqlfile.write("\n")

for filename in filename_sports:
    sqlfile.write("INSERT INTO Contain VALUES(1, \'" + filename.hexdigest() + "\', \'\', {});\n".format(seqnum_sports))
    seqnum_sports += 1
for filename in filename_football:
    sqlfile.write("INSERT INTO Contain VALUES(2, \'" + filename.hexdigest() + "\', \'\', {});\n".format(seqnum_football))
    seqnum_football += 1
for filename in filename_world:
    sqlfile.write("INSERT INTO Contain VALUES(3, \'" + filename.hexdigest() + "\', \'\', {});\n".format(seqnum_world))
    seqnum_world += 1
for filename in filename_space:
    sqlfile.write("INSERT INTO Contain VALUES(4, \'" + filename.hexdigest() + "\', \'\', {});\n".format(seqnum_space))
    seqnum_space += 1

sqlfile.close()

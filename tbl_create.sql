CREATE TABLE User
(
	username VARCHAR(20) NOT NULL,
	firstname VARCHAR(20),
	lastname VARCHAR(20),
	password VARCHAR(256),
	email VARCHAR(40),
	PRIMARY KEY(username)
);

CREATE TABLE Album
(
	albumid INT NOT NULL AUTO_INCREMENT,
	title VARCHAR(50),
	created DATE,
	lastupdated DATE,
	username VARCHAR(20),
	access ENUM('public', 'private'),
	PRIMARY KEY(albumid),
	FOREIGN KEY(username) REFERENCES User(username)
	
);

CREATE TABLE Photo
(
	picid VARCHAR(40) NOT NULL,
	format CHAR(3),
	date DATE,
	PRIMARY KEY(picid)
);

CREATE TABLE Contain
(
	albumid INT NOT NULL,
	picid VARCHAR(40) NOT NULL,
	caption VARCHAR(255),
	sequencenum INT,
	PRIMARY KEY (albumid, picid),
	FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE,
	FOREIGN KEY (picid) REFERENCES Photo(picid) ON DELETE CASCADE
);

CREATE TABLE AlbumAccess
(
	albumid INT NOT NULL,
	username VARCHAR(20) NOT NULL,
	PRIMARY KEY (albumid, username),
	FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE,
	FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE
);

delimiter |
CREATE TRIGGER addphoto
BEFORE INSERT ON Contain
	FOR EACH ROW
	BEGIN
		UPDATE Album SET lastupdated = CURDATE()
		WHERE albumid = NEW.albumid;
	END;
|
delimiter ;

delimiter |
CREATE TRIGGER deletephoto
AFTER DELETE ON Contain
	FOR EACH ROW
	BEGIN
		UPDATE Album SET lastupdated = CURDATE()
		WHERE albumid = OLD.albumid;
	END;
|
delimiter ;

delimiter |
CREATE TRIGGER updatephoto
AFTER UPDATE ON Contain
	FOR EACH ROW
	BEGIN
		UPDATE Album SET lastupdated = CURDATE()
		WHERE albumid = OLD.albumid;
	END;
|
delimiter ;

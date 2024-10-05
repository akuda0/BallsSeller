import sqlite3

connection = sqlite3.Connection('balls_seller.sqlite')
cursor = connection.cursor()

cursor.execute("""DROP TABLE Common_Balls""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Common_Balls" (
	"id" INTEGER NOT NULL UNIQUE,
	"type" TEXT NOT NULL,
	"material" TEXT DEFAULT 'latex',
	"color"	TEXT NOT NULL,
	"picture" TEXT NOT NULL UNIQUE,
	"amount" INTEGER NOT NULL DEFAULT 0,
	"price"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id")
	UNIQUE("type", "material", "color", "picture") ON CONFLICT IGNORE
)""")
#
cursor.execute("""INSERT INTO Common_Balls (type, material, color, picture, amount, price) VALUES ('no sign', 'foil', 'green', 'green.jpg', 10, 80)""")
cursor.execute("""INSERT INTO Common_Balls (type, color, picture, amount, price) VALUES ('no sign', 'red', 'red.jpg', 12, 82)""")
cursor.execute("""INSERT INTO Common_Balls (type, material, color, picture, amount, price) VALUES ('Hello, Kitty', 'foil', 'yellow', 'hello_kitty_yellow.jpg', 2, 100)""")
cursor.execute("""INSERT INTO Common_Balls (type, material, color, picture, amount, price) VALUES ('no sign', 'foil', 'blue', 'blue.jpg', 7, 75)""")
cursor.execute("""INSERT INTO Common_Balls (type, material, color, picture, amount, price) VALUES ('no sign', 'foil', 'blue', 'blue_2.jpg', 9, 75)""")
cursor.execute("""INSERT INTO Common_Balls (type, color, picture, amount, price) VALUES ('Happy Birthday!', 'yellow', 'happy_birthday_yellow.jpg', 10, 74)""")
cursor.execute("""INSERT INTO Common_Balls (type, color, picture, amount, price) VALUES ('Hello, Kitty', 'black', 'hello_kitty_black.jpg', 3, 65)""")
cursor.execute("""INSERT INTO Common_Balls (type, material, color, picture, amount, price) VALUES ('Hello, Kitty', 'latex', 'black', 'hello_kitty_black.jpg', 3, 65)""")

cursor.execute("""DROP TABLE Shaped_Balls""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Shaped_Balls" (
	"id" INTEGER NOT NULL UNIQUE,
	"type" TEXT NOT NULL,
	"subtype" TEXT NOT NULL,
	"picture" TEXT NOT NULL UNIQUE,
	"amount" INTEGER NOT NULL DEFAULT 0,
	"price"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id")
	UNIQUE("type", "subtype", "picture") ON CONFLICT IGNORE
)""")

cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('digit', 'one', '1.jpg', 10, 80)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('animal', 'cow', 'cow.jpg', 12, 82)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('animal', 'cat', 'cat.jpg', 2, 100)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('animal', 'cat', 'cat2.png', 6, 72)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('animal', 'cat', 'cat3.png', 3, 71)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('animal', 'cat', 'cat4.png', 8, 65)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('star', '5-triangle', 'star.jpg', 7, 75)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('digit', 'nine', 'nine.jpg', 10, 74)""")
cursor.execute("""INSERT INTO Shaped_Balls (type, subtype, picture, amount, price) VALUES ('digit', 'zero', 'zero.jpg', 3, 65)""")


cursor.execute("""DROP TABLE Customers""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Customers" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nickname"	TEXT NOT NULL,
	PRIMARY KEY("id")
	UNIQUE("nickname") ON CONFLICT IGNORE
)""")

cursor.execute("""INSERT INTO Customers (nickname) VALUES ('@andy')""")
cursor.execute("""INSERT INTO Customers (nickname) VALUES ('@andy')""")
cursor.execute("""INSERT INTO Customers (nickname) VALUES ('@mike')""")


cursor.execute("""DROP TABLE Orders""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Orders" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ball"	INTEGER NOT NULL DEFAULT 0,
	"type"	TEXT NOT NULL DEFAULT 'Blow up',
	"amount"	INTEGER NOT NULL DEFAULT 0,
	"nickname"	INTEGER NOT NULL,
	"status" TEXT NOT NULL DEFAULT 'not paid',
	"notes" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("nickname") REFERENCES "Customers"("id")
	UNIQUE("ball", "type", "nickname", "status", "notes") ON CONFLICT IGNORE
)""")
# UNIQUE("ball", "type", "nickname") ON CONFLICT UPDATE ("ball", "type", "nickname")



cursor.execute("""DROP TABLE IF EXISTS Orders_history""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Orders_history" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ball"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	"amount"	INTEGER NOT NULL DEFAULT 0,
	"nickname"	INTEGER NOT NULL,
	"status" TEXT NOT NULL DEFAULT 'Completed',
    "notes" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("nickname") REFERENCES "Customers"("id")
)""")


connection.commit()
connection.close()

Make sure to create db name simpleturf and create table turfdatas.
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int          | NO   | PRI | NULL    | auto_increment |
| city         | varchar(255) | NO   |     | NULL    |                |
| turf         | varchar(255) | NO   |     | NULL    |                |
| details      | text         | YES  |     | NULL    |                |
| slot         | varchar(255) | YES  |     | NULL    |                |
| booking_date | date         | YES  |     | NULL    |                |
| bookings     | text         | YES  |     | NULL    |                |
| is_blocked   | tinyint(1)   | YES  |     | 1       |                |
| block_time   | datetime     | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
struture should look like this . 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Use this command for inserting data in database and make sure to add 3 cities atleast
INSERT INTO turfdatas (city, turf, details, slot) VALUES
('Hubli', 'Unit 1  turf', 'location: Opposite Sector 1  phone no: 9179876116', '9am-10am,10am-11am,11am-12pm,12pm-1pm,1pm-2pm,2pm-3pm,3pm-4pm,4pm-5pm,5pm-6pm,6pm-7pm,7pm-8pm,8pm-9pm,9pm-10pm'),
('Hubli', 'Unit 2  turf', 'location: Near Pakwan resto  phone no: 9199876176', '9am-10am,10am-11am,11am-12pm,12pm-1pm,1pm-2pm,2pm-3pm,3pm-4pm,4pm-5pm,5pm-6pm,6pm-7pm,7pm-8pm,8pm-9pm,9pm-10pm'),
 ('Hubli', 'Unit 3  turf',' location: Behind AB lodge phone no: 9819879376', '9am-10am,10am-11am,11am-12pm,12pm-1pm,1pm-2pm,2pm-3pm,3pm-4pm,4pm-5pm,5pm-6pm,6pm-7pm,7pm-8pm,8pm-9pm,9pm-10pm'),
 ('Hubli', 'Vidyagiri   turf',' location :Near BEC Boys hostel phone no: 4879873116','9am-10am,10am-11am,11am-12pm,12pm-1pm,1pm-2pm,2pm-3pm,3pm-4pm,4pm-5pm,5pm-6pm,6pm-7pm,7pm-8pm,8pm-9pm,9pm-10pm'),
 ('Hubli', 'Navanagar turf',' location :Behind Lions School phone no :9879179876', '9am-10am,10am-11am,11am-12pm,12pm-1pm,1pm-2pm,2pm-3pm,3pm-4pm,4pm-5pm,5pm-6pm,6pm-7pm,7pm-8pm,8pm-9pm,9pm-10pm');
 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Also replace Vonage key and secret key with your original , vonage will only send sms to registered number in vonage if u want to send all, You guys need to upgrade account to send all numbers

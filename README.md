# sltest [Brett Johnson <brett@johnsonit.com.au> 26-01-2021]


SL Practical Coding Exercise

# Pre-Requisites

MySQL/MariaDB


## Setup

``
$ pip install flask flask-jsonpify flask-restful mysql-connector-python flask_restful
``

MySQL

``
MariaDB [(none)]> create database sltest;

Query OK, 1 row affected (0.004 sec)

MariaDB [(none)]> use sltest;

Database changed

MariaDB [sltest]> create table todo (id int auto_increment, name varchar(128) not null, description blob, due date, completed bool, primary key(id));


Query OK, 0 rows affected (0.018 sec)

MariaDB [(none)]> grant all privileges on sltest.* to sltest@localhost identified by 'sillypassword';

Query OK, 0 rows affected (0.012 sec)
``




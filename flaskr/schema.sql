create database flasker;
use flasker;
drop table if exists entries;

create table `entries` (
       id int(20)  NOT NULL AUTO_INCREMENT,
       title varchar(255)  not null,
       text varchar(255)  not null,
       PRIMARY KEY (`id`)

);

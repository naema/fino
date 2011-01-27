create database if not exists tvdb;
use database tvbd;

drop table genres;
drop table series;
drop table episodes;

create table genres(
  id              integer not null primary key auto_increment,
  genre           varchar (255) not null
);

create table series(
  id              integer not null primary key auto_increment,
  title           varchar (255) not null,
  url             varchar (255),
  genre_id        integer references genres(id)
);

create table episodes(
  id              integer not null primary key auto_increment,
  series_id       integer references series(id),
  season          integer not null,
  episode         integer not null,
  title           varchar(255),
  nr              integer,
  airdate         date
);

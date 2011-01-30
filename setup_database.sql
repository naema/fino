create database if not exists tvdb;

drop table if exists genres, series, episodes;

create table genres(
  id              integer not null primary key auto_increment,
  genre           varchar (255) not null
);

create table series(
  id              integer not null primary key auto_increment,
  title           varchar (255) not null unique,
  url             varchar (255) unique,
  genre_id        integer references genres(id)
);

create table episodes(
  id              integer not null primary key auto_increment,
  series_id       integer not null references series(id),
  season          integer not null,
  episode         integer not null,
  title           varchar(255),
  nr              integer,
  airdate         date,
  status          ENUM('pending','downloading','existent'),
  unique key se_key (season, episode)
);

drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    firstname text not null,
    lastname text not null,
    username text not null,
    password text not null
);
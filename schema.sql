drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    firstname text not null,
    lastname text not null,
    username text not null,
    password text not null,
    college text,
    class_year text,
    gender text,
    orientation text,
    preference text
);

drop table if exists friends;
    create table friends (
    id integer primary key autoincrement,
    username text not null,
    friend text not null,
    FOREIGN KEY (username) references users(username)
);

drop table if exists inbox;
    create table inbox (
    id integer primary key autoincrement,
    username text not null,
    matched_user text not null,
    FOREIGN KEY (username) references users(username)
);

drop table if exists inbox;
    create table inbox (
    primary_friend text not null,
    username text not null,
    PRIMARY KEY (primary_friend),
    FOREIGN KEY (username) references users(username)
);
drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    firstname text not null,
    lastname text not null,
    username text not null,
    password text not null
);


drop table if exists friends;
    create table friends (
    id integer primary key autoincrement,
    primary_friend TEXT,
    PRIMARY KEY (primary_friend),
    FOREIGN KEY (username) references users(username)
);
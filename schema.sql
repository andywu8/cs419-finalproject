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
    primary_friend text not null,
    username text not null,
    PRIMARY KEY (primary_friend),
    FOREIGN KEY (username) references users(username)
);
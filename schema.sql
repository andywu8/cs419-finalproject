-- drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    username text not null,
    password text not null,
    phone_number text,
    college text,
    class_year text,
    gender text,
    orientation text,
    preference text
);

-- insert into users (first_name, last_name, username, password) 
-- VALUES 
--     ('dummy-Andy', 'Wu', 'dummy-andywu', 'andywu'),
--     ('dummy-Allen', 'Chun', 'dummy-allenchun', 'allenchun'),
--     ('dummy-Annette', 'Lee', 'dummy-annettelee', 'annettelee'),
--     ('dummy-Kishan', 'Patel', 'dummy-kishanpatel', 'kishanpatel');


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
    matched_user1 text not null,
    matched_user2 text not null,
    user1_matched_boolean boolean, 
    user2_matched_boolean boolean,
    FOREIGN KEY (username) references users(username)
);



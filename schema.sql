create table users(
	id integer primary key autoincrement,
	name text not null,
	password text not null,
	admin boolean not null
);

create table task_url(
	task_id integer primary key autoincrement,
	url text not null
);

create table progress_check(
	user_id integer primary key,
	task_completed integer not null
);
CREATE TABLE IF NOT EXISTS guilds(
	GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "+"
);

CREATE TABLE IF NOT EXISTS economy(
    UserID integer PRIMARY KEY,
    Wallet integer DEFAULT 100,
    Bank integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS warn(
    UserID integer PRIMARY KEY,
    warnCount integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS exp(
	UserID integer PRIMARY KEY,
	XP integer DEFAULT 0,
	Level integer DEFAULT 0,
	XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mutes(
	UserID integer PRIMARY KEY,
	mute integer DEFAULT 0
);
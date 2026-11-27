-- Rep: take a real-world domain (an order system, a ticketing system) and design the schema on paper to 3NF. Then write the DDL. Save to work/03-postgres/schema-design/

-- Requirements
-- Movie
-- Ticket
-- Show
-- Screen
-- Seat


-- CREATE TABLE Movie (
--     movie_id serial,
--     movie_name text NOT NULL,
--     language text,
--     genre text[]

-- );

-- CREATE TABLE Seat (
--     Seat_unq_id uuid,
--     seat_name text,
--     seat_type ["Gold","Silver","Bronze","Other"],
--     Screen_no int
--     FOREIGN KEY REFERENCES Screen(Screen_no) 
-- )

-- CREATE TABLE Screen (
--     Screen_no int,
--     Screen_name text,
--     Seats Seat []
-- )

-- CREATE TABLE Show (
--     show_id int, 
--     movie_id serial 
--     FOREIGN KEY REFERENCES Movie(movie_id),
--     Screen_no serial
--     FOREIGN KEY REFERENCES Screen(Screen_no),
--     start_date_time TIMESTAMP,
--     end_time TIMESTAMP,

-- )

-- CREATE TABLE Ticket (
--     ticket_id serial,
--     show_id Show
--     FOREIGN KEY REFERENCES Show(show_id),
--     seats_booked Seat [],
--     amount float,

-- )


CREATE TABLE Movie (
    movie_id serial,
    movie_name text NOT NULL,
    language text,
    year DATE NOT NULL,
    genre text[],
    PRIMARY KEY(movie_id)

);

CREATE TABLE Screen (
    screen_no int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Screen_name text,
    PRIMARY KEY(screen_no)
);

-- Natural Key  seat_name, screen_no

CREATE TABLE Seat (
    seat_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seat_name text NOT NULL,
    seat_type text,
    PRIMARY KEY(seat_name,screen_no),
    constraint Seat_Screen_fk
    FOREIGN KEY(screen_no) REFERENCES Screen(screen_no) 
);




CREATE TABLE Show (
    show_id int, 
    movie_id serial,
    screen_no serial,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    PRIMARY KEY(show_id),
    constraint show_movie_fk
    FOREIGN KEY(movie_id) REFERENCES Movie(movie_id),
    constraint show_screen_fk
    FOREIGN KEY(screen_no) REFERENCES Screen(screen_no)

);

CREATE TABLE Ticket (
    ticket_id uuid,
    show_id Show,
    seats_booked Seat [],
    amount float,
    constraint ticket_show
    FOREIGN KEY show_id REFERENCES Show(show_id)

);

Feedback from claude
The schema breaks 1NF because table Movie has a genre column which is a list , so it has no referential integrity 

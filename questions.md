### 1
if the shell expands globs before the program runs, how would you pass a literal * to a program like find -name "*.txt"? Why does find need the quotes? What would go wrong without them if the directory had a.txt and b.txt in it?

Work out what find receives in each case and tell me.

### 2
Normalization theory gaps (come back after the ticketing design is drafted):
1. One-sentence reason for each normal form: which anomaly does 2NF remove that 1NF leaves? And 3NF versus 2NF?
2. Compute candidate keys for R(A,B,C,D,E) with A->B, BC->D, D->E using attribute closure. Show the steps.
3. A read-heavy analytics system joins 6 normalized tables on every dashboard load. What would you do, what is the cost of that fix, and who keeps the copies consistent?
4. Why is a surrogate key (id SERIAL) not an escape from normalization? If you add `id` to the quiz Purchase table, does Title -> Artist stop being a problem?

### 3
Ticketing schema, normalization review (after the design pass):
1. `genre text[]` in Movie: keep the array or use a movie_genre junction table? Defend in two sentences (identity, FK integrity, renames, genre attributes).
2. `Seats Seat[]` in Screen and `seats_booked Seat[]` in Ticket: what mechanism prevents double-booking seat A2 for show 7 with an array? With one row per booked seat (UNIQUE (show_id, seat_id))?
3. BCNF vs 3NF: which original constraint is lost when splitting Student/Coach/Sport, and can it still be enforced in one table?

### 4

CREATE TABLE t_serial (id bigserial PRIMARY KEY, pad text);
CREATE TABLE t_uuid   (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), pad text);

INSERT INTO t_serial (pad) SELECT 'x' FROM generate_series(1, 1000000);
INSERT INTO t_uuid   (pad) SELECT 'x' FROM generate_series(1, 1000000);

SELECT pg_size_pretty(pg_relation_size('t_serial_pkey')) AS serial_index,
       pg_size_pretty(pg_relation_size('t_uuid_pkey'))   AS uuid_index;
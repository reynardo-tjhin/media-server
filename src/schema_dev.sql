DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS movie_genre;
DROP TABLE IF EXISTS user;

-- for movies
CREATE TABLE "movie" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	"imdb_rating"	REAL,
	"rotten_tomatoes_rating"	INTEGER,
	"metacritic_rating"	INTEGER,
	"release_date"	TEXT NOT NULL,
	"media_location"	TEXT NOT NULL UNIQUE,
	"poster_location"	TEXT NOT NULL UNIQUE,
	"duration"	INTEGER,
	PRIMARY KEY("id")
);

-- genre table for movies
CREATE TABLE "genre" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

-- relationship table between movie and genre
CREATE TABLE "movie_genre" (
	"movie_id"	TEXT NOT NULL,
	"genre_id"	TEXT NOT NULL,
	PRIMARY KEY("movie_id","genre_id"),
	FOREIGN KEY("genre_id") REFERENCES "genre" ON DELETE CASCADE,
	FOREIGN KEY("movie_id") REFERENCES "movie" ON DELETE CASCADE
);

-- for users
CREATE TABLE "user" (
	"id"	TEXT NOT NULL UNIQUE, -- str(uuid.uuid4())
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"is_admin"	TEXT NOT NULL, -- True/False
	PRIMARY KEY("id")
);



-- ================================================
-- POPULATING THE DATA
-- ================================================

-- create an admin user
INSERT INTO user VALUES(
	'688fd6c6-4e9b-49f1-a077-c68ab7b2980a', 
	'admin', 
	'scrypt:32768:8:1$g4f9PQW6G7Ci3tHW$505aafaebc266fed3240cf673686ea07d9d74bfc21394ef777abc29984d3a5da7cf387a2f21eb46772b68613da6e755a09599830c13704d7588adb73652d0aec', 
	'True'
);

-- create a normal user
INSERT INTO user VALUES(
	'89b5f5f5-857f-43e2-a93c-7b57a3512295', 
	'user', 
	'scrypt:32768:8:1$3GYsb6BnUEPuuXzn$8769c64c04fb5a949e4d26758aec106039d12ea67755da9ccac28dcd46a5b6f0c3f14f719a98781a82c5b9f826f8713aa7a3c70718f0da9901ad3164f0b36b3a', 
	'False'
);

-- create a genre data
INSERT INTO genre VALUES(
	'1c0547c5-59c3-4e40-bd46-15db44f115ff',
	'Action',
	'Should contain numerous scenes where action is spectacular and usually destructive. Often includes non-stop motion, high energy physical stunts, chases, battles, and destructive crises (floods, explosions, natural disasters, fires, etc.)'
);

-- create a genre data
INSERT INTO genre VALUES(
	'091f7e75-357d-4ec5-853f-b15cbbc01fe3',
	'Adult',
	'Reserved for explicit works of consenting hardcore sex or sexual activity, or strong fetish material involving adults, specifically those created for the purposes of titillation or arousal. Must be used with the plot keywords of ''hardcore'' and ''sex'' or ''special-sexual-interest''. Documentaries about this type of material do not use the Adult genre.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'a65e45ff-c74e-495e-a614-e532fcd1a7d1',
	'Adventure',
	'Should contain numerous consecutive and inter-related scenes of characters participating in hazardous or exciting experiences for a specific goal. Often include searches or expeditions for lost continents and exotic locales, characters embarking in treasure hunt or heroic journeys, travels, and quests for the unknown. Not to be confused with Action, and should only sometimes be supplied with it.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'd42577b4-8303-4aab-b328-b261f2a2128d',
	'Animation',
	'Over 75% of the title''s running time should have scenes that are wholly, or part-animated. Any form of animation is acceptable, e.g., hand-drawn, computer-generated, stop-motion, etc. Puppetry does not count as animation, unless a form of animation such as stop-motion is also applied. Incidental animated sequences should be indicated with the keywords part-animated or animated-sequence instead. Please note that motion capture elements within ''real-world'' films such as Paddington are not eligible for this genre. Additionally although the overwhelming majority of video games are a form of animation it''s okay to forgo this genre when adding them as this is implied by the title type.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'2891a948-8b07-4349-a2f2-87fab5681fe6',
	'Biography',
	'Primary focus is on the depiction of activities and personality of a real person or persons, for some or all of their lifetime. Events in their life may be reenacted, or described in a documentary style. If re-enacted, they should generally follow reasonably close to the factual record, within the limitations of dramatic necessity. A real person in a fictional setting would not qualify a production for this genre. If the focus is primarily on events, rather than a person, use History instead.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'0cad58ec-7f8a-4dcd-a606-f142a2c85748',
	'Comedy',
	'Virtually all scenes should contain characters participating in humorous or comedic experiences. The comedy can be exclusively for the viewer, at the expense of the characters in the title, or be shared with them. Please submit qualifying keywords to better describe the humor (i.e. spoof, parody, irony, slapstick, satire, dark-comedy, comedic-scene, etc.). If the title does not conform to the ''virtually all scenes'' guideline then please do not add the comedy genre; instead, submit the same keyword variations described above to signify the comedic elements of the title. The subgenre keyword "dramedy-drama" can also be used to categorize titles with comedic undertones that qualify for the Drama genre but not necessarily the Comedy genre.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'afbedc0f-6d3f-4107-9047-2697b794865e',
	'Crime',
	'Whether the protagonists or antagonists are criminals this should contain numerous consecutive and inter-related scenes of characters participating, aiding, abetting, and/or planning criminal behavior or experiences usually for an illicit goal. Not to be confused with Film-Noir, and only sometimes should be supplied with it.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'045b677f-1504-434e-927f-49bc5404ddd0',
	'Documentary',
	'Should contain numerous consecutive scenes of real personages and not characters portrayed by actors. This does not include fake or spoof documentaries, which should instead have the fake-documentary keyword. A documentary that includes actors re-creating events should include the keyword "reenactment" so that those actors are not treated as "Himself." This genre should also be applied to all instances of stand-up comedy and concert performances.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'2382a019-ee31-484f-a758-06e3aa1acdbf',
	'Drama',
	'Should contain numerous consecutive scenes of characters portrayed to effect a serious narrative throughout the title, usually involving conflicts and emotions. This can be exaggerated upon to produce melodrama.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'006013fd-3542-447e-85ec-77a583af7fab',
	'Family',
	'Should be universally accepted viewing for a younger audience. e.g., aimed specifically for the education and/or entertainment of children or the entire family. Often features children or relates to them in the context of home and family. Note: Usually, but not always, complementary to Animation.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'f69a93bb-2170-42e3-9af1-8c83189cbaa8',
	'Fantasy',
	'Should contain numerous consecutive scenes of characters portrayed to effect a magical and/or mystical narrative throughout the title. Usually has elements of magic, supernatural events, mythology, folklore, or exotic fantasy worlds.Note: not to be confused with Sci-Fi which is not usually based in magic or mysticism.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'2c9f6c48-826b-425b-8369-c5a2f666eb88',
	'Film-Noir',
	'Typically features dark, brooding characters, corruption, detectives, and the seedy side of the big city. Almost always shot in black and white, American, and set in contemporary times (relative to shooting date). We take the view that this genre began with Underworld (1927) and ended with Touch of Evil (1958). Note: neo-noir should be submitted as a keyword instead of this genre for titles that do not fit all criteria.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'57c1370a-d6f0-4ab2-9412-720f630e5989',
	'Game-Show',
	'Competition, other than sports, between, usually, non-professional contestants. The competition can include a physical component, but is usually primarily mental or strategic as opposed to athletic. This also includes what are known as "quiz shows." Talent contests staged expressly for the program are considered Game-Shows.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'22fa6ae2-931e-4596-a7c5-fc53a608e591',
	'History',
	'Primary focus is on real-life events of historical significance featuring real-life characters (allowing for some artistic license); in current terms, the sort of thing that might be expected to dominate the front page of a national newspaper for at least a week; for older times, the sort of thing likely to be included in any major history book. While some characters, incidents, and dialog may be fictional, these should be relatively minor points used primarily to bridge gaps in the record. Use of actual persons in an otherwise fictional setting, or of historic events as a backdrop for a fictional story, would not qualify. If the focus is primarily on one person''s life and character, rather than events of historical scope, use Biography instead.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'8182143e-0c34-4d1b-a062-d9af52efb60e',
	'Horror',
	'Should contain numerous consecutive scenes of characters effecting a terrifying and/or repugnant narrative throughout the title. Note: not to be confused with Thriller which is not usually based in fear or abhorrence.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'6f865fdf-3886-427c-9db9-a11c8cfa3468',
	'Musical',
	'Should contain several scenes of characters bursting into song aimed at the viewer (this excludes songs performed for the enjoyment of other characters that may be viewing) while the rest of the time, usually but not exclusively, portraying a narrative that alludes to another Genre. Note: not to be added for titles that are simply music related or have music performances in them; e.g., pop concerts do not apply. Also, classical opera, since it is entirely musical, does not apply and should instead be treated as Music.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'6619ebab-0da5-4c97-9cf6-7f29bc3c34be',
	'Music',
	'Contains significant music-related elements while not actually being a Musical; this may mean a concert, or a story about a band (either fictional or documentary).'
);

-- create a genre data
INSERT INTO genre VALUES(
	'6e5cb0be-4960-4cf3-84ee-7091e4de124b',
	'Mystery',
	'Should contain numerous inter-related scenes of one or more characters endeavoring to widen their knowledge of anything pertaining to themselves or others. Note: Usually, but not always associated with Crime.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'0b6f181a-1538-4459-b0ea-536c8fb48d13',
	'News',
	'Reports and discussion of current events of public importance or interest. This generally includes newsreels, newsmagazines, daily news reports, and commentary/discussion programs that focus on news events. If the events are not current (at the time the title was initially released), use History instead. News titles are normally made for television, podcasts, or (in the case of newsreels) short films. Feature films, direct-to-video titles, and videogames would not normally be included in the News genre.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'4e3ce421-3456-467e-a7ba-c8e2916424dc',
	'Reality-TV',
	'Often, but not always, features non-professionals in an unscripted, but generally staged or manipulated, situation. May or may not use hidden cameras; generally, but not always, in a non-studio setting.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'0afb1540-d096-4f3e-bb6b-702396e01501',
	'Romance',
	'Should contain numerous inter-related scenes of a character and their personal life with emphasis on emotional attachment or involvement with other characters, especially those characterized by a high level of purity and devotion. Note: Reminder, as with all genres if this does not describe the movie wholly, but only certain scenes or a subplot, then it should be submitted as a keyword instead.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'2de89c73-664c-497a-831c-38939e3e5d2f',
	'Sci-Fi',
	'Numerous scenes, and/or the entire background for the setting of the narrative, should be based on speculative scientific discoveries or developments, environmental changes, space travel, or life on other planets.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'b9a46bbc-49e3-48e7-b4c4-bdcdb90338c8',
	'Short',
	'Any theatrical film or made-for-video title with a running time of less than 45 minutes, i.e., 44 minutes or less, or any TV series or TV movie with a running time of less than 22 minutes, i.e. 21 minutes or less. (A "half-hour" television program should not be listed as a Short.) If known, please submit the running time if we do not have one on record.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'a87ddcd2-ba61-48f6-abb0-08319ff27d62',
	'Sport',
	'Focus is on sports or a sporting event, either fictional or actual. This includes fictional stories focused on a particular sport or event, documentaries about sports, and television broadcasts of actual sporting events. In a fictional film, the sport itself can also be fictional, but it should be the primary focus of the film.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'af6700d8-7eda-47c9-a75b-b41e4735fa6c',
	'Talk-Show',
	'Discussion or interviews of or with a series of guests or panelists, generally appearing as themselves in a non-fictional setting (though fictional programs that mimic the form are also included). (aka "chat show").'
);

-- create a genre data
INSERT INTO genre VALUES(
	'a7febfe1-10c2-416f-9161-0d3a6f2c4200',
	'Thriller',
	'Should contain numerous sensational scenes or a narrative that is sensational or suspenseful. Note: not to be confused with Mystery or Horror, and should only sometimes be accompanied by one (or both).'
);

-- create a genre data
INSERT INTO genre VALUES(
	'2bf00715-1790-4843-93dd-b394cc62089b',
	'War',
	'Should contain numerous scenes and/or a narrative that pertains to a real war (i.e., past or current). Note: for titles that portray fictional war, please submit it as a keyword only.'
);

-- create a genre data
INSERT INTO genre VALUES(
	'32bd668f-512b-4fef-ab5b-0339ba01c09f',
	'Western',
	'Should contain numerous scenes and/or a narrative where the portrayal is similar to that of frontier life in the American West during 1600s to contemporary times.'
);

-- create a movie data
INSERT INTO movie VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a',
	'Big Hero 6',
	'A special bond develops between plus-sized inflatable robot Baymax and prodigy Hiro Hamada, who together team up with a group of friends to form a band of high-tech heroes.',
	7.8, -- IMDb
	91,  -- Rotten Tomatoes
	74,  -- metacritic
	'2014-11-07', -- release date
	'.\vids\Big Hero 6.mp4', -- movie location
	'posters/Big Hero 6.webp', -- poster location
	102 -- duration
);

-- create a movie data
INSERT INTO movie VALUES(
	'ac4c9da6-b943-47fa-ac07-4a63dd43728d',
	'Conclave',
	'Cardinal Lawrence has one of the world''s most secretive and ancient events, participating in the selection of a new pope. Surrounded by powerful religious leaders in the halls of the Vatican, he soon uncovers a trail of deep secrets that could shake the very foundation of the Roman Catholic Church.',
	7.4, -- IMDb
	93,  -- Rotten Tomatoes
	79,  -- metacritic
	'2024-10-25', -- release date
	'.\vids\Conclave.mp4', -- movie location
	'posters/Conclave.webp', -- poster location
	120 -- duration
);

-- create a movie data
INSERT INTO movie VALUES(
	'c9ae3de0-d0e3-440c-b66d-d17d3b524ff4',
	'Kung Fu Panda 4',
	'After Po is tapped to become the Spiritual Leader of the Valley of Peace, he needs to find and train a new Dragon Warrior, while a wicked sorceress plans to re-summon all the master villains whom Po has vanquished to the spirit realm.',
	6.3, -- IMDb
	84,  -- Rotten Tomatoes
	54,  -- metacritic
	'2024-03-08', -- release date
	'.\vids\Kung Fu Panda 4.mp4', -- movie location
	'posters/Kung Fu Panda 4.webp', -- poster location
	94 -- duration
);

-- create a movie data
INSERT INTO movie VALUES(
	'62ba8d65-540e-4176-964b-c10f095e3f0e',
	'The Wild Robot',
	'After a shipwreck, an intelligent robot called Roz is stranded on an uninhabited island. To survive the harsh environment, Roz bonds with the island''s animals and cares for an orphaned baby goose.',
	8.2, -- IMDb
	98,  -- Rotten Tomatoes
	85,  -- metacritic
	'2024-09-27', -- release date
	'.\vids\The Wild Robot.mp4', -- movie location
	'posters/The Wild Robot.webp', -- poster location
	102 -- duration
);

-- create a relationship table
-- Big Hero 6 and Action
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'1c0547c5-59c3-4e40-bd46-15db44f115ff' -- genre_id
);

-- Big Hero 6 and Adventure
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'a65e45ff-c74e-495e-a614-e532fcd1a7d1' -- genre_id
);

-- Big Hero 6 and Animation
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'd42577b4-8303-4aab-b328-b261f2a2128d' -- genre_id
);

-- Big Hero 6 and Comedy
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'0cad58ec-7f8a-4dcd-a606-f142a2c85748' -- genre_id
);

-- Big Hero 6 and Crime
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'afbedc0f-6d3f-4107-9047-2697b794865e' -- genre_id
);

-- Big Hero 6 and Family
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'006013fd-3542-447e-85ec-77a583af7fab' -- genre_id
);

-- Big Hero 6 and Sci-Fi
INSERT INTO movie_genre VALUES(
	'016f78ba-38fa-41f7-bc22-adc47389ae4a', -- movie_id
	'2de89c73-664c-497a-831c-38939e3e5d2f' -- genre_id
);

-- Conclave and Drama
INSERT INTO movie_genre VALUES(
	'ac4c9da6-b943-47fa-ac07-4a63dd43728d', -- movie_id
	'2382a019-ee31-484f-a758-06e3aa1acdbf' -- genre_id
);

-- Conclave and Thriller
INSERT INTO movie_genre VALUES(
	'ac4c9da6-b943-47fa-ac07-4a63dd43728d', -- movie_id
	'a7febfe1-10c2-416f-9161-0d3a6f2c4200' -- genre_id
);

-- Kung Fu Panda 4 and Action
INSERT INTO movie_genre VALUES(
	'c9ae3de0-d0e3-440c-b66d-d17d3b524ff4', -- movie_id
	'c9ae3de0-d0e3-440c-b66d-d17d3b524ff4' -- genre_id
);

-- Kung Fu Panda 4 and Adventure
INSERT INTO movie_genre VALUES(
	'c9ae3de0-d0e3-440c-b66d-d17d3b524ff4', -- movie_id
	'a65e45ff-c74e-495e-a614-e532fcd1a7d1' -- genre_id
);

-- Kung Fu Panda 4 and Animation
INSERT INTO movie_genre VALUES(
	'c9ae3de0-d0e3-440c-b66d-d17d3b524ff4', -- movie_id
	'd42577b4-8303-4aab-b328-b261f2a2128d' -- genre_id
);

-- Kung Fu Panda 4 and Comedy
INSERT INTO movie_genre VALUES(
	'c9ae3de0-d0e3-440c-b66d-d17d3b524ff4', -- movie_id
	'0cad58ec-7f8a-4dcd-a606-f142a2c85748' -- genre_id
);

-- The Wild Robot and Adventure
INSERT INTO movie_genre VALUES(
	'62ba8d65-540e-4176-964b-c10f095e3f0e', -- movie_id
	'a65e45ff-c74e-495e-a614-e532fcd1a7d1' -- genre_id
);

-- The Wild Robot and Animation
INSERT INTO movie_genre VALUES(
	'62ba8d65-540e-4176-964b-c10f095e3f0e', -- movie_id
	'd42577b4-8303-4aab-b328-b261f2a2128d' -- genre_id
);

-- The Wild Robot and Family
INSERT INTO movie_genre VALUES(
	'62ba8d65-540e-4176-964b-c10f095e3f0e', -- movie_id
	'006013fd-3542-447e-85ec-77a583af7fab' -- genre_id
);

-- The Wild Robot and Sci-Fi
INSERT INTO movie_genre VALUES(
	'62ba8d65-540e-4176-964b-c10f095e3f0e', -- movie_id
	'2de89c73-664c-497a-831c-38939e3e5d2f' -- genre_id
);

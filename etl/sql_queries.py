sql_movies = """SELECT
   fw.id,
   fw.rating as imdb_rating,
   array_agg(DISTINCT g.name) as genre,
   fw.title,
   fw.description,
   fw.modified, 
   COALESCE(
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='director'), '' ) as director,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='actor') as actors_names,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='writer') as writers_names,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='writer'),
       '[]'
   ) as writers
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified::timestamp without time zone > '{}'::timestamp without time zone
GROUP BY fw.id
ORDER BY fw.modified; """


sql_persons = """SELECT
   fw.id,
   fw.rating as imdb_rating,
   array_agg(DISTINCT g.name) as genre,
   fw.title,
   fw.description,
   MAX(p.modified) as modified,
   COALESCE(
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='director'), '' ) as director,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='actor') as actors_names,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='writer') as writers_names,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='writer'),
       '[]'
   ) as writers
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
LEFT JOIN content.film_work fw ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE p.modified > '{}'
GROUP BY fw.id
ORDER BY modified; """


sql_genres = """SELECT
   fw.id,
   fw.rating as imdb_rating,
   array_agg(DISTINCT g.name) as genre,
   fw.title,
   fw.description,
   MAX(g.modified) as modified,
   COALESCE(
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='director'), '' ) as director,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='actor') as actors_names,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='writer') as writers_names,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='writer'),
       '[]'
   ) as writers
FROM content.genre g
LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
LEFT JOIN content.film_work fw ON g.id = gfw.genre_id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE g.modified > '{}'
GROUP BY fw.id
ORDER BY modified; """


sql_movie = """SELECT modified as "st [timestamp]" FROM content.film_work ORDER BY modified DESC;"""
sql_person = """SELECT modified as "st [timestamp]" FROM content.person ORDER BY modified DESC;"""
sql_genre = """SELECT modified as "st [timestamp]" FROM content.genre ORDER BY modified DESC;"""
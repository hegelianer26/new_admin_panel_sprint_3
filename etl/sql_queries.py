small_sql_query = """ SELECT
    fw.modified as modified
    FROM content.film_work fw
    UNION SELECT
    p.modified as modified
    FROM content.person p
    UNION SELECT
    g.modified as modified
    FROM content.genre g
    ORDER BY modified DESC; """


big_sql_query = """SELECT
   fw.id,
   fw.rating as imdb_rating,
   array_agg(DISTINCT g.name) as genre,
   fw.title,
   fw.description,
   GREATEST(MAX(g.modified), fw.modified, MAX(p.modified)) as great,
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
WHERE g.modified > '{upd}' or fw.modified > '{upd}' or p.modified > '{upd}'
GROUP BY fw.id
ORDER BY great DESC; """

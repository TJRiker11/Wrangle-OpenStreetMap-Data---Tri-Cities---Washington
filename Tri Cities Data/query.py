# Number of Nodes
query = "SELECT count(DISTINCT(id)) FROM nodes;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Number of Ways
query = "SELECT count(DISTINCT(id)) FROM ways;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Top Contributing Users
query= 'SELECT e.user, COUNT(*) as num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e GROUP BY e.user ORDER BY num DESC LIMIT 25;'
cur.execute(query)
rows = cur.fetchall()
pprint.pprint(rows)

# Type and Number of Nodes
query = "SELECT type , count(*) as num  FROM nodes_tags group by type order by num desc;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Type and Number of Ways
query = "SELECT type , count(*) as num  FROM ways_tags group by type order by num desc;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Biggest Religions
query="select value, count(*) as num from (select key,value from nodes_tags UNION ALL select key,value from ways_tags) as e  where key='religion' group by value order by num desc limit 10;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Top Quisines
query="select value,count(*) as num from (select key,value from nodes_tags UNION ALL select key,value from ways_tags) as e where e.key like '%cuisine%' group by value order by num desc limit 25;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Top Amenities
query="select value, count(*) as num from nodes_tags where key='amenity' group by value order by num desc limit 25;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)

# Number of Unique Users
query = "SELECT COUNT(DISTINCT(e.uid))FROM (SELECT uid FROM Nodes UNION ALL SELECT uid FROM Ways) as e;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)
 

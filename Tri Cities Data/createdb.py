# Connect to the database
mydb = 'tricities.db'
conn = sqlite3.connect(mydb)
cur = conn.cursor()



# Drop table if already exists
query="DROP TABLE IF EXISTS nodes;"
cur.execute(query);
conn.commit()
query = "CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT);"
cur.execute(query)
conn.commit()

# Open CSV file and formatting data
with open('nodes.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['lat'].decode("utf-8"),i['lon'].decode("utf-8"),i['user'].decode("utf-8"),i['uid'].decode("utf-8"),i['version'].decode("utf-8"),i['changeset'].decode("utf-8"),i['timestamp'].decode("utf-8")) for i in dr]

# Insert Data
cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?,?,?);", to_db)
conn.commit()
f.close()




# Drop table if already exists
query="DROP TABLE IF EXISTS nodes_tags;"
cur.execute(query);
conn.commit()
query = "CREATE TABLE nodes_tags (id INTEGER,key TEXT,value TEXT,type TEXT,FOREIGN KEY (id) REFERENCES nodes(id));"
cur.execute(query)
conn.commit()

# Open CSV file and formatting data
with open('nodes_tags.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['key'].decode("utf-8"),i['value'].decode("utf-8"),i['type'].decode("utf-8")) for i in dr]

# Insert Data
cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
conn.commit()
f.close()




# Drop table if already exists
query="DROP TABLE IF EXISTS ways;"
cur.execute(query);
conn.commit()
query = "CREATE TABLE ways(id INTEGER PRIMARY KEY NOT NULL,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT);"
cur.execute(query)
conn.commit()

# Open CSV file and formatting data
with open('ways.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['user'].decode("utf-8"),i['uid'].decode("utf-8"),i['version'].decode("utf-8"),i['changeset'].decode("utf-8"),i['timestamp'].decode("utf-8")) for i in dr]
    
# Insert Data
cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?);", to_db)
conn.commit()
f.close()




# Drop table if already exists
query="DROP TABLE IF EXISTS ways_tags;"
cur.execute(query);
conn.commit()
query = "CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id));"
cur.execute(query)
conn.commit()

# Open CSV file and formatting data
with open('ways_tags.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['key'].decode("utf-8"),i['value'].decode("utf-8"),i['type'].decode("utf-8")) for i in dr]

# Insert Data
cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
conn.commit()
f.close()




# Drop table if already exists
query="DROP TABLE IF EXISTS ways_nodes;"
cur.execute(query);
conn.commit()
query = "CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id));"
cur.execute(query)
conn.commit()

# Open CSV file and formatting data
with open('ways_nodes.csv','rb') as f: 
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode("utf-8"),i['node_id'].decode("utf-8"),i['position'].decode("utf-8")) for i in dr]

# Insert Data
cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?,?,?);", to_db)
conn.commit()
f.close()



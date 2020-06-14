# OpenStreetMap Data Case Study

### Map Area
Tri-Cities, WA, USA

All files for this project can be seen [Here](https://github.com/TrikerDev/Wrangle-OpenStreetMap-Data---Tri-Cities---Washington) and full report with all work can be seen [Here](https://github.com/TrikerDev/Wrangle-OpenStreetMap-Data---Tri-Cities---Washington/blob/master/Tri%20Cities%20Data/Wrangle%20OpenStreetMap%20Data%20-%20Tri-Cities%2C%20Washington.ipynb)


### Problems Encountered

- Inconsistent street addresses (some end in 'Street' or 'street' or 'st' or 'St.' etc
- Inconsistent and incorrect postal codes (some have 5 digits '11111' some have 9 '11111-1111' and some dont have enough digits to form a correct zip code
- Tags have many problem characters such as hyphens, dashes, underscores, etc

### Benefits to fixing these problems
The reason for doing a project like this is to clean messy data and make it consistent. With so many different endings for streets and post codes, it can get confusing to read a map. Changing all data for an area to have completely consistent data with all other data makes the map much more readable and less messy. It will also make it easier for users to find specific places. For example, if a user typed in 'Horn Rapids Street' but the actual map said something like 'Horn Rapids St.' they might not find the correct area they are looking for. Creating a uniform database allows all users always find what they need as long as they are using they know the standard syntax that all the data is written in.


### Auditing Tags
```Python
# Adding variables for the tags to be stored under, definitions above
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
    
# Function starting on our dataset
def process_keys_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

# Iterating through tags and adding them up
def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] = keys['problemchars'] + 1
        else:    
            keys['other'] += 1  
    return keys


# Opening file and starting process_keys_map function
with open(OSM_FILE,'rb') as f:
    keys = process_keys_map(OSM_FILE)
    pprint.pprint(keys)

# Closing file
f.close()
```


### Auditing Street Names - Expected values and mapping to values
```Python
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# The values we expect to see. This is the end result of all street name endings we want
expected = ["Street", "Avenue","Loop", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Freeway","Circle","Strand","Sterling","Way","Highway",
            "Terrace","South","East","West","North","Landing"]

# Mapping shortened version of common street name endings to the ending we want
mapping = {
            " St ": " Street ",
            " St": " Street ",
            " St.": " Street ",
            " ST": " Street ",
            " Rd.": " Road ",
            " Rd ": " Road ",
            " Rd": " Road ",
            " Ave ": " Avenue ", 
            " Ave": " Avenue ", 
            " Ave.": " Avenue ",
            " Av ": " Avenue ", 
            " Dr ": " Drive ",
            " Dr.": " Drive",
            " Dr": " Drive",
            " Pl ": " Place",
            " Pl": " Place",
            " Blvd ": " Boulevard ",
            " Blvd": " Boulevard",
            " Blvd.": " Boulevard",
            " Ct ": " Court ",
            " Ct": " Court ",
            " Ctr": " Center",
            " Pl ": " Place ",
            " Ln ": " Lane ",
            " Cir ": " Circle ",
            " Wy": " Way ",
            " S ": " South ",
            " E ": " East ",
            " W ": " West ",
            " N ": "North"
}
```

### Auditing Post Codes
```Python
# The way to audit the postcodes is to make them all uniform. Since the vast majority of them are 5 digits, we will be
# auditing the longer codes by stripping off the extra digits and he '-'. This will make every post code a uniform 5 digits
def update_postcode(name): 
    if "-" in name:
        name = name.split("-")[0].strip()
    elif len(str(name))>5:
        name=name[0:5]
    elif len(str(name))<5:
        name = '00000'
    return name



def audit_postcode_tag(element,regex=re.compile(r'\b\S+\.?$', re.IGNORECASE)):
    post_code=element.get('v')
    m = regex.search(post_code)
    if m:
        better_postcode=update_postcode(post_code)
        return better_postcode
    return post_code
```



### Size of Files
```Python
#links to the csv files
nodes_csv = 'nodes.csv'
ways_csv = 'ways.csv'
nodestags_csv = 'nodes_tags.csv'
waystags_csv = 'ways_tags.csv'
waysnodes_csv = 'ways_nodes.csv'

# Get the size (in bytes) of specified path  
size_tricitiesdb = os.path.getsize('tricities.db')
size_osm_xml = os.path.getsize('map.osm')
size_nodes = os.path.getsize(nodes_csv) 
size_ways = os.path.getsize(ways_csv) 
size_nodestags = os.path.getsize(nodestags_csv) 
size_waystags = os.path.getsize(waystags_csv) 
size_waysnodes = os.path.getsize(waysnodes_csv) 
  
# Print the size (in bytes) of specified path  
print("Size (In bytes) of '%s':" %'tri_cities.db', size_tricitiesdb)
print("Size (In bytes) of '%s':" %'map.osm', size_osm_xml)
print("Size (In bytes) of '%s':" %nodes_csv, size_nodes)
print("Size (In bytes) of '%s':" %ways_csv, size_ways)
print("Size (In bytes) of '%s':" %nodestags_csv, size_nodestags)
print("Size (In bytes) of '%s':" %waystags_csv, size_waystags)
print("Size (In bytes) of '%s':" %waysnodes_csv, size_waysnodes)
```
```
("Size (In bytes) of 'tri_cities.db':", 42356736L)
("Size (In bytes) of 'map.osm':", 82031159L)
("Size (In bytes) of 'nodes.csv':", 31701618L)
("Size (In bytes) of 'ways.csv':", 2396620L)
("Size (In bytes) of 'nodes_tags.csv':", 1158419L)
("Size (In bytes) of 'ways_tags.csv':", 4416724L)
("Size (In bytes) of 'ways_nodes.csv':", 10807215L)
```




### Exploring Data

### Number of Nodes
```XML
query = "SELECT count(DISTINCT(id)) FROM nodes;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)
```
368263

### Number of Ways
```XML
query = "SELECT count(DISTINCT(id)) FROM ways;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)
```
38417


### Number of Unique Users
```XML
query = "SELECT COUNT(DISTINCT(e.uid))FROM (SELECT uid FROM Nodes UNION ALL SELECT uid FROM Ways) as e;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)
```
447

### Top 5 Contributing Users
```XML
query= 'SELECT e.user, COUNT(*) as num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e GROUP BY e.user ORDER BY num DESC LIMIT 25;'
cur.execute(query)
rows = cur.fetchall()
pprint.pprint(rows)
```
```
Jessica12345, 102374
Howpper, 68010
DJ Cane, 38615
OrcaDan, 23035
woodpeck_fixbot, 15212
```

### Top 5 Quisines
```XML
query="select value,count(*) as num from (select key,value from nodes_tags UNION ALL select key,value from ways_tags) as e where e.key like '%cuisine%' group by value order by num desc limit 25;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)
```
```
burger, 36
coffee_shop, 23
pizza, 19
mexican, 18
sandwich, 13
 ```
 
 
### Top 5 Amenities
```XML
query="select value, count(*) as num from nodes_tags where key='amenity' group by value order by num desc limit 25;"
cur.execute(query)
rows=cur.fetchall()

pprint.pprint(rows)
```
```
bench, 151
restaurant, 52
toilets, 51
fast_food, 46
parking, 30
 ```
 
 
 
 ### Ideas for Additional Improvement
 Additional improvement that could be made to the dataset is just overall human error correction. Any dataset this large that is entirely comprised of human input will have errors and doing cleaning and analysis like this on all types of different data points would make the data much more uniform across the dataset. This could be improved by having a uniform data entering scheme that all users of OpenStreetMaps have to follow to submit data. This could help keep the data between different users much more uniform in general.
 
 A drawback to having a standing scheme for entering data is that it might get less people to enter data in the first place. Having a standard scheme to enter the data will require users to enter more data and in a different format than they otherwise might have. This might deter users from entering data in the first place, as it would make the process longer and more tedious. This could potentially have the problem of cutting down even further on the already small userbase. 
 
  The dataset overall was also very incomplete in general. With an open source map such as this, things are bound to be missing, and as this is a relatively small area compared to large cities, there are less users, and therefore less information. An idea for getting more users to add more data could be some sort of gamification system where users get points with some type of rewards and competition for updating the maps. This can be seen as a very small number of users make up a giant portion of all the data to the maps. So a very small group of people are the ones trying to update this. The top 10 users makes up nearly 95% of all updates to the map. Getting more users to contribute to this would help the data be updated much quicker.
  
  However, there is also a drawback to the gamification system. First off, the rewards would have to be something that people actually care about earning. And with an already free system such as OpenStreetMaps, there is hardly any incentive to earn anything, such as credits for the site, as it is already free. Also, if there are points to earn, based on amount of posts or some other form of data, it may incentivise users to enter as much as possible, to rack up points. This could easily turn into users just entering as much false or incorrect data as possible without fact checking first, just to earn points before other users can. 
 
 ### Conclusion
 This dataset is very large and comprised entirely of information provided by many different users. Different users entering different data at different times leads to some messy data. Going through and cleaning the data like this helps to make the data overall much more uniform and readable. Having a standardized data entering scheme would keep the data much more uniform from the start, however, for a completely open-source website that anyone can enter on, the data was overall very clean. It certainly could have been much worse. The way users enter data is probably about as good as it can be, and for users who prefer more clean data, and analysis such as this could be carried out to standardize all the data.

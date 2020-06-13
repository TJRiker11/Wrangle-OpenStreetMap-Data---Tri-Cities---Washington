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



# Handling expected and unexpected street names
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    
    
# Getting street names and sending them to audit_street_type function
def audit(file):
    file = open(file, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    file.close()
    return street_types
    
    
# Function for replace 'old' names with 'new' names
def update_street_name(name, mapping):
    for key,value in mapping.items():
        if key in name:
            return name.replace(key,value)
    return name 

def audit_street_name_tag(element): 
    street_name=element.get('v')
    m = street_type_re.search(street_name)
    if m:
        better_street_name=update_street_name(street_name,mapping)
        return better_street_name
    return street_name
    
# Variable for new street names to be stored
st_types = audit(OSM_FILE)

for st_type, ways in st_types.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)

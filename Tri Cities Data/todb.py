NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


SCHEMA = schema


NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']





# Cleaning and shaping elemnents to Python dict

"""Clean and shape node or way XML element to Python dict"""

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = [] # Handle secondary tags the same way for both node and way elements
             

   

    if element.tag=='node':
        for field in node_attr_fields:
            node_attribs[field]=element.get(field)
                 
        if element.find('tag') is None:
            pass
           
        elif element.find('tag') is not None:
            tag_attrib={}
            node_tag_fields=NODE_TAGS_FIELDS
            for tag in element.iter('tag'):
                if PROBLEMCHARS.search(tag.attrib['k']):
                    pass
                elif LOWER_COLON.search(tag.attrib['k']):
                    tag_attrib[node_tag_fields[0]]=element.get('id')
                    tag_attrib[node_tag_fields[1]]=tag.get('k')[(tag.get('k').find(':')+1):]
                    if tag.attrib['k']== "addr:street":
                        tag_attrib[node_tag_fields[2]]=audit_street_name_tag(tag)
                    elif tag.attrib['k']== "addr:postcode":
                        tag_attrib[node_tag_fields[2]]=audit_postcode_tag(tag)       
                    else:
                        tag_attrib[node_tag_fields[2]]=tag.get('v')
                    tag_attrib[node_tag_fields[3]]=tag.get('k').split(':')[0]
                    tags.append(tag_attrib.copy())
                
                else:
                    tag_attrib[node_tag_fields[0]]=element.get('id')
                    tag_attrib[node_tag_fields[1]]=tag.get('k')
                    if tag.attrib['k']== "addr:street":
                        tag_attrib[node_tag_fields[2]]=audit_street_name_tag(tag)
                    elif tag.attrib['k']== "addr:postcode":
                        tag_attrib[node_tag_fields[2]]=audit_postcode_tag(tag)    
                    else:    
                        tag_attrib[node_tag_fields[2]]=tag.get('v')
                    tag_attrib[node_tag_fields[3]]=default_tag_type
                    tags.append(tag_attrib.copy())
             
        
                
    elif element.tag=='way':
        for field in way_attr_fields:
            way_attribs[field]=element.get(field)
    
        way_node_attrib={}
        way_node_fields=WAY_NODES_FIELDS
        for nd in element.findall('nd'):
            way_node_attrib[way_node_fields[0]]=element.get('id')
            way_node_attrib[way_node_fields[1]]=nd.get('ref')
            way_node_attrib[way_node_fields[2]]=element.findall('nd').index(nd)
            way_nodes.append(way_node_attrib.copy())
        
        
        
        
        if element.find('tag') is None:
            pass
           
        elif element.find('tag') is not None:
            way_tag_attrib={}
            way_tag_fields=WAY_TAGS_FIELDS
            for tag in element.iter('tag'):
                if PROBLEMCHARS.search(tag.attrib['k']):
                    pass
                elif LOWER_COLON.search(tag.attrib['k']):
                    way_tag_attrib[way_tag_fields[0]]=element.get('id')
                    way_tag_attrib[way_tag_fields[1]]=tag.get('k')[(tag.get('k').find(':')+1):]
                    if tag.attrib['k']== "addr:street":
                        way_tag_attrib[way_tag_fields[2]]=audit_street_name_tag(tag)
                    elif tag.attrib['k']== "addr:postcode":
                        way_tag_attrib[way_tag_fields[2]]=audit_postcode_tag(tag)    
                    else:
                        way_tag_attrib[way_tag_fields[2]]=tag.get('v')
                    way_tag_attrib[way_tag_fields[3]]=tag.get('k').split(':')[0]
                    tags.append(way_tag_attrib.copy())
                    
                else:
                    way_tag_attrib[way_tag_fields[0]]=element.get('id')
                    way_tag_attrib[way_tag_fields[1]]=tag.get('k')
                    if tag.attrib['k']== "addr:street":
                        way_tag_attrib[way_tag_fields[2]]=audit_street_name_tag(tag) 
                    elif tag.attrib['k']== "addr:postcode":
                        way_tag_attrib[way_tag_fields[2]]=audit_postcode_tag(tag)    
                    else:   
                        way_tag_attrib[way_tag_fields[2]]=tag.get('v')
                    way_tag_attrib[way_tag_fields[3]]=default_tag_type
                    tags.append(way_tag_attrib.copy())
        
    

    
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
        
        
        
        
        
        
    # Get Element
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
            
            
            
            # Validate Element
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))
        
        
        
        # Dict Writer
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
            
            
            
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
                    
                    
             # Starting the process
if __name__ == '__main__':
    process_map(OSM_FILE, validate=True)

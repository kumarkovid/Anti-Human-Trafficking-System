from rdflib import Graph, Literal, BNode, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, DC
from rdflib.namespace import XSD
import os
from rdflib import Graph, plugin

from rdflib.serializer import Serializer
import escort_fish as s


PHONE_BASE_URI = 'http://htkg.stevens.edu/phone/'
LOCATION_BASE_URI = 'http://htkg.stevens.edu/location/'
PHONE_RAW_URI = PHONE_BASE_URI + 'raw/'
PHONE_INSTANCE_URI = PHONE_BASE_URI + 'instance/'
PHONE_AREA_URI = PHONE_BASE_URI + 'area_code/'
PHONE_AREA_INSTANCE = PHONE_BASE_URI + 'area_code/instance/'
store = Graph()
phone = Graph(identifier=URIRef(PHONE_BASE_URI))
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
GEORSS = Namespace('http://www.georss.org/georss/')

# Bind a few prefix, namespace pairs for pretty output
store.bind("dc", DC)
store.bind("foaf", FOAF)
store.bind('geo', GEO)
store.bind('georss', GEORSS)

GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

  
def floatToStrWithDecimals(n: float) -> str:
    """Function to format a float to a string, suppressing scientific notation
    and displaying up to 10 decimal places.
    
    Arguments:
        n {float} -- Float to be formatted.
    
    Returns:
        str -- Formatted float.
    """

    return '{0:.10f}'.format(n)

# Create an identifier to use as the subject for Donna.
def saveAdToRDF(dictionay):
    advertisement = BNode()

    # Add triples using store's add method.
    store.add((advertisement, RDF.type, FOAF.Person))
    # store.add((advertisement, FOAF.phone, Literal(a[i]['phone'],datatype=XSD.integer)))
    store.add((advertisement, FOAF.age, Literal(dictionay['age'],datatype=XSD.integer)))
    store.add((advertisement, FOAF.location, Literal(dictionay['location'],datatype=XSD.string)))
    store.add((advertisement, FOAF.ad_text, Literal(dictionay['ad_text'],datatype=XSD.string)))
    store.add((advertisement, FOAF.time, Literal(dictionay['time'],datatype=XSD.time)))
    store.add((advertisement, FOAF.date, Literal(dictionay['date'],datatype=XSD.date)))
    store.add((advertisement, FOAF.image, Literal(dictionay['image'],datatype=XSD.anyURI)))

    # Geospatial Data (if available)
    if dictionay['latitude'] is not None:
        # Geographic coordinates
        point = BNode()
        store.add((point, RDF.type, GEO.Point))
        store.add((point, GEO.lat, Literal(floatToStrWithDecimals(dictionay['latitude']),datatype=XSD.decimal)))
        store.add((point, GEO.long, Literal(floatToStrWithDecimals(dictionay['longitude']),datatype=XSD.decimal)))

        # Adding point to graph
        store.add((advertisement, GEORSS.where, point))


    # Extracting phone number area code
    area_code = str(dictionay['phone'])[:3]

    # Phone number subgraph
    phone_node = URIRef(PHONE_INSTANCE_URI + str(dictionay['phone']))
    phone.add((phone_node, URIRef(PHONE_RAW_URI), Literal(dictionay['phone'], datatype=XSD.integer)))
    phone.add((phone_node, URIRef('http://dbpedia.org/ontology/areaCode'), Literal(area_code, datatype=XSD.integer)))

    store.add((advertisement, FOAF.phone, phone_node))

# Iterate over triples in store and print them out.
#print(store.serialize(format='turtle'))

    with open('advertisements.ttl', 'wb') as f:
    	f.write(store.serialize(format='turtle'))

    with open('phones.ttl', 'wb') as f:
        f.write(phone.serialize(format='turtle'))
def download(n):
	s.scrape(n, save_func=saveAdToRDF)

download(1000)

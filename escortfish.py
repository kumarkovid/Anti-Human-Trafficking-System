from rdflib import Graph, Literal, BNode, RDF, URIRef
from rdflib.namespace import FOAF, DC
from rdflib.namespace import XSD
import os
from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import escortfish as s


PHONE_BASE_URI = 'http://htkg.stevens.edu/phone/'
PHONE_RAW_URI = PHONE_BASE_URI + 'raw/'
PHONE_INSTANCE_URI = PHONE_BASE_URI + 'instance/'
PHONE_AREA_URI = PHONE_BASE_URI + 'area_code/'
PHONE_AREA_INSTANCE = PHONE_BASE_URI + 'area_code/instance/'

if __name__ == '__main__':

    store = Graph()
    phone = Graph(identifier=URIRef(PHONE_BASE_URI))

    # Bind a few prefix, namespace pairs for pretty output
    store.bind("dc", DC)
    store.bind("foaf", FOAF)

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

        # Extracting phone number area code
        area_code = str(dictionay['phone'])[:3]

        # Phone number subgraph
        phone_node = URIRef(PHONE_INSTANCE_URI + str(dictionay['phone']))
        phone.add((phone_node, URIRef(PHONE_RAW_URI), Literal(dictionay['phone'], datatype=XSD.integer)))
        phone.add((phone_node, URIRef('http://dbpedia.org/ontology/areaCode'), Literal(area_code, datatype=XSD.integer)))

        store.add((advertisement, FOAF.phone, phone_node))

    # Iterate over triples in store and print them out.
    #print(store.serialize(format='turtle'))

        with open('advertisements.ttl', 'ab') as f:
        	f.write(store.serialize(format='turtle'))

        with open('phones.ttl', 'ab') as f:
            f.write(phone.serialize(format='turtle'))

s.scrape(n=5, save_func=saveAdToRDF)
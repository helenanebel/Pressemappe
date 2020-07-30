from OCR.get_texts import get_texts
from NLP.nlp_pressemappe import get_entities
from GND.gnd_request import get_gnd
from GND.select_entities import select_gnd
from RDF.rdf_generator import make_rdf

tesseract_path = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
get_texts(tesseract_path)
get_entities()
get_gnd()
select_gnd()
make_rdf()

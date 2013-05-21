import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
import sets

def mapper(record):
    doc_id = record[0]
    text = record[1]
    words = text.split()
    for word in words:
      mr.emit_intermediate(word, doc_id)

def reducer(word, list_of_doc_ids):
    inverted_set = set([])
    for doc_id in list_of_doc_ids:
      inverted_set.update([doc_id])
    mr.emit((word, list(inverted_set)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

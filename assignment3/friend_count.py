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
    friend = record[0]
    mr.emit_intermediate(friend, 1)

def reducer(friend, list_of_counts):
    total = 0
    for count in list_of_counts:
      total += count
    mr.emit((friend, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
from collections import defaultdict;

def mapper(record):
	mr.emit_intermediate(record[0], (record[1], "has"))
	mr.emit_intermediate(record[1], (record[0], "is"))

def reducer(person, friends_list):
	friends_dict = defaultdict(list)
	for friend_relation in friends_list:
		friends_dict[friend_relation[0]].append(friend_relation[1])
	for friend, relations in friends_dict.iteritems():
		if(len(relations) == 1):
			mr.emit((person, friend))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

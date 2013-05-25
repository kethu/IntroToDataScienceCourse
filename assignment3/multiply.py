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
	matrix = record[0]
	row = record[1]
	column = record[2]
	value = record[3]
	if(matrix == "a"):
		for k in range(5):
			mr.emit_intermediate((row, k), (matrix, column, value))
	else:
		for i in range(5):
			mr.emit_intermediate((i, column), (matrix, row, value))

def reducer(common_key, list_of_cells):
	matrix = defaultdict(dict)
	for cell in list_of_cells:
		matrix[cell[0]][cell[1]] = cell[2]
	cell_value = 0
	for a in matrix[u'a'].iteritems():
		for b in matrix[u'b'].iteritems():
			if(a[0]==b[0]):
				cell_value += a[1]*b[1]
	mr.emit((common_key[0], common_key[1], cell_value))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

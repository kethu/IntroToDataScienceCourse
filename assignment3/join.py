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
    type_of_record = record[0]
    order_id = record[1]
    mr.emit_intermediate(order_id, {type_of_record: record})

def reducer(order_id, records):
    cross_join = []
    for left_record in records:
      left_key = left_record.keys()[0]
      for right_record in records:
        right_key = right_record.keys()[0]
        if((left_key == "order") and (left_key != right_key) and (right_key != "joined")):
          cross_join.append(left_record[left_key]+right_record[right_key])
    for joins in cross_join:
      mr.emit(joins)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

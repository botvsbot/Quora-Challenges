#Quora Nearby Challenge

from math import sqrt
from collections import OrderedDict
import operator

def topic_search():
	global topic_sorted_dict
	global topic_sorted
	source_vector = [query_XY for i in xrange(0,T)]
	dest_vector = [j for j in T_ID.itervalues()]
	dist_vector = []
	id = [id for id in T_ID.iterkeys()]
	for k in xrange(0,T):
		dist_vector.append([round(sqrt((dest_vector[k][0] - query_XY[0])**2 + \
                                       (dest_vector[k][1] - query_XY[1])**2)), id[k]])
	q_temp = sorted(dist_vector, key = lambda id:id[1], reverse = True)
	q = sorted(q_temp, key = lambda id:id[0])
	l = 0
	result = []
	if query_ID == 't':
		while(l < query_N and l < len(q)):
			result.append(q[l][1])
			l+=1
		l = 0
	topic_sorted = []
	topic_sorted_dict.clear()
	while (l < len(q)):
		topic_sorted_dict[q[l][1]] = q[l][0]
		topic_sorted.append(q[l][1])
		l+=1
	return result
	
def query_search():
    topic_search()
    global query_sorted_dict, query_sorted
    query_sorted = []
    query_sorted_dict = dict()
    for key in topic_sorted:
        temp_query_sorted = (topic_to_query_dict[key])
        temp_query_reverse_sorted = sorted(temp_query_sorted, reverse = True)
        for items in temp_query_reverse_sorted:
            query_sorted.append(items)
        
    #Remove duplicates from query_sorted:
    query_sorted = list(OrderedDict.fromkeys(query_sorted))
    
    l = 0
    result = []
    if query_ID == 'q':
		while(l < query_N and l < len(query_sorted)):
			result.append(query_sorted[l])
			l+=1
     
    return result




ip = raw_input()
input_strings = ip.split(" ")
T = int(input_strings[0])
Q = int(input_strings[1])
N = int(input_strings[2])

T_ID = dict()

topic_sorted_dict = dict()
query_sorted_dict = dict()

for i in xrange(0,T):
	ip = raw_input()
	input_strings = ip.split(" ")
	T_ID[int(input_strings[0])] = [float(input_strings[1]), float(input_strings[2])]

Q_ID = dict()	
	
for i in xrange(0,Q):
	ip = raw_input()
	input_strings = ip.split(" ")
	if input_strings[1] != "0":
		Q_ID[int(input_strings[0])] = [int(j) for j in input_strings[2:]]

query_ID_array = []
query_N_array = []
query_XY_array = []

for i in xrange(0,N):
	ip = raw_input()
	input_strings = ip.split(" ")
	query_ID_array.append(input_strings[0])
	query_N_array.append(int(input_strings[1]))
	query_XY_array.append([float(input_strings[2]), float(input_strings[3])])

    
#Build a dictionary of topic -> associated queries, with queries in descending order.

topic_to_query_dict = dict()
for (query,topics) in Q_ID.iteritems():
    for topic in topics:
        if topic in topic_to_query_dict:
            temp_val = topic_to_query_dict[topic]
            temp_val.append(query)
            topic_to_query_dict[topic] = temp_val
        else:
            topic_to_query_dict[topic] = [query]

for i in xrange(0,N):
	query_ID = query_ID_array[i]
	query_N = query_N_array[i]
	query_XY = query_XY_array[i]
	if query_ID == 't':
		#code for topic search
		res_T = topic_search()
		for j in xrange(0,len(res_T)):
			print res_T[j],
		print
	else:
		#code for query search
		res_T = query_search()
		for j in xrange(0,len(res_T)):
			print res_T[j],
		print

print topic_to_query_dict

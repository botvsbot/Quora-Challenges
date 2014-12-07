'''
Quora typeahead search using Trie - All 9 testcases pass.

'''


# Class Trie
class Trie(object):

	def __init__(self):
		self.word = None
		self.qid = set()	
		self.children = {}

	def insert(self, word, qid):
		for letter in word.lower():
			if letter not in self.children:
				self.children[letter] = Trie()
			self = self.children[letter]
			self.qid.add(qid)
		self.word = word.lower()

	def search(self, word):
		for letter in word.lower():
			if letter not in self.children:
				local_var = set()
				return local_var
			self = self.children[letter]
		return (self.qid)

	def delete(self, word, qid):
		deepest_tree = self
		suffix = ""
		for letter in word.lower():
			if letter not in self.children:
				return # the word to be deleted is not in the trie
			if self.word != None or len(self.children) > 1: # A possible prefix exists to the word to be deleted
				deepest_tree = self
				suffix = letter
			else:
				suffix = suffix+letter
			self.children[letter].qid.discard(qid)
			self = self.children[letter]
		if self.word == word.lower():
			if not self.children: # the word is not a prefix of an existing word
				self.qid.discard(qid)
				# Delete the branch
				if len(self.qid) == 0:
					for i in xrange(0, len(suffix) - 1):
						if i < len(suffix)-2:
							grand_child = (deepest_tree.children[suffix[0]]).children[suffix[i+1]].children[suffix[i+2]]
							deepest_tree.children[suffix[0]].children[suffix[i+2]] = grand_child
							if suffix[i+2] == suffix[i+1]:
								continue
						del(deepest_tree.children[suffix[0]].children[suffix[i+1]])
					del(deepest_tree.children[suffix[0]])
						
			else: # the word is a prefix of another word in the trie
				self.word = None
				self.qid.discard(qid)
			return
		else:
			return # the word to be deleted is not in the trie




# Global variables
trie = Trie()
database = {}
no_of_queries = 0
no_of_cmds = 0
results = {}
database_boost = {}




# Helper Functions
def resolve_conflicts(array):
	for i in xrange(0,len(array)-1):
		if array[i][1] == array[i+1][1]:
			if (array[i][2] > array[i+1][2]):
				temp = array[i+1][:]
				array[i+1][:] = array[i][:]
				array[i][:] = temp
	return array





# Add/Delete Operations
def add_id(query, no_of_cmds):
	global trie
	for word in query[4:]:
		trie.insert(word, query[2])
	database[query[2]] = { "type":query[1],
							"score":float(query[3]),
							"data":query[4:],
							"age":no_of_cmds,
							"boosted_score":float(query[3])}
	if query[1] in database_boost:
		database_boost[query[1]].append(query[2])
	else:
		database_boost[query[1]] = [query[2]]

def delete_id(query):
	global database
	global trie
	if query[1] in database:
		for word in database[query[1]]["data"]:
			trie.delete(word,query[1])
		if query[1] in database_boost[database[query[1]]["type"]]:
			database_boost[database[query[1]]["type"]].remove(query[1])
		del database[query[1]]
	
		

# Normal Queries
def populate_normal_query(query):
	global database
	global no_of_queries
	global results
	global trie
	no_of_queries += 1
	local_count = 0
	all_queries = set()
	id_score_age = []
	result_to_display = []
	for word in query[2:]:
		if word == "":
			continue
		if local_count == 0:
			all_queries = trie.search(word)
		else:
			all_queries = all_queries & (trie.search(word))
			if len(all_queries) == 0:
				results[no_of_queries] = []
				return
		local_count += 1
	for qid in all_queries:
		id_score_age.append([qid,database[qid]["score"],database[qid]["age"]])
	
	temp_array_sorted = sorted(id_score_age, key = lambda id:id[1], reverse = True)
	# Code for score conflict
	array_sorted = resolve_conflicts(temp_array_sorted)
	results_to_display = [array_sorted[i][0] for i in xrange(0,min(int(query[1]), len(array_sorted)))]

	results[no_of_queries] = results_to_display

def populate_weighted_query(query):
	global database
	global no_of_queries
	global results
	global trie
	no_of_queries += 1
	elements_changed = []
	# Loop for number of boosts
	for boost_query in query[3:3+int(query[2])]:
		type_or_id = boost_query.split(":")[0]
		boost_factor = float(boost_query.split(":")[1])
		if (type_or_id == "user" or type_or_id == "topic" or
			type_or_id == "question" or type_or_id == "board"):
			# Find all matching types from db and update boosted_score
			if type_or_id in database_boost:
				for element in database_boost[type_or_id]:
					database[element]["boosted_score"] *= boost_factor
					elements_changed.append(element)
			else:
				continue
		else:
			# Find unique id from db and update boosted_score
			if type_or_id in database:
				database[type_or_id]["boosted_score"] *= boost_factor
				elements_changed.append(type_or_id)
			else:
				continue

	local_count = 0
	all_queries = set()
	id_score_age = []
	result_to_display = []
	for word in query[3+int(query[2]):]:
		if local_count == 0:
			all_queries = trie.search(word)
		else:
			all_queries = all_queries & trie.search(word)
			if len(all_queries) == 0:
				break
		local_count += 1
	for qid in all_queries:
		id_score_age.append([qid,database[qid]["boosted_score"],database[qid]["age"]])
	
	temp_array_sorted = sorted(id_score_age, key = lambda id:id[1], reverse = True)
	# Code for score conflict
	array_sorted = resolve_conflicts(temp_array_sorted)
	results_to_display = [array_sorted[i][0] for i in xrange(0,min(int(query[1]), len(array_sorted)))]

	results[no_of_queries] = results_to_display
	for qid in elements_changed:
		database[qid]["boosted_score"] = database[qid]["score"]



# Main
no_of_cmds = int(raw_input())
while(no_of_cmds>0):
	query = str(raw_input()).split()
	if query[0] == "ADD":
		add_id(query, no_of_cmds)
	elif query[0] == "DEL":
		delete_id(query)
	elif query[0] == "QUERY":
		populate_normal_query(query)
	elif query[0] == "WQUERY":
		populate_weighted_query(query)
	no_of_cmds -= 1
for result_id in results:
	for result in results[result_id]:
		if result:
			print result,
	print

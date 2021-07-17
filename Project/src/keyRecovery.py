from collections import defaultdict
import sys

# lookahead window size
lookahead = None
lookahead = int(sys.argv[1])

####################################
# function to backtrack the DP array to get edit actions
def editDistance(s1, s2, dp):  
	i = len(s1)
	j = len(s2)
	edits = []
	  
   	# Check till the end 
	while(i > 0 and j > 0):  
		# If characters are same 
		if s1[i - 1] == s2[j - 1]:
			edits.append("NA")
			i -= 1
			j -= 1
			 
		# Replace
		elif dp[i][j] == dp[i - 1][j - 1] + 1:
			edits.append("r"+str(s2[j-1]))
			j -= 1
			i -= 1
			  
		# Delete
		elif dp[i][j] == dp[i - 1][j] + 1:
			edits.append("d")
			i -= 1
			  
		# Insert
		elif dp[i][j] == dp[i][j - 1] + 1:
			edits.append("i" + str(s2[j-1]))
			j -= 1

	while(j>0):
		edits.append("i" + str(s2[j-1]))
		j -= 1

	while(i>0):
		edits.append("d")
		i -= 1

	edits.reverse()
	return edits	
			  
# Function to compute the DP matrix for Edit distance 
def editDP(s1, s2, flag):
	# edits = ["NA"]*(len(s1)+1)
	len1 = len(s1)
	len2 = len(s2)
	dp = [[0 for i in range(len2 + 1)]
			 for j in range(len1 + 1)]
	  
	# Initilize by the maximum edits possible 
	for i in range(len1 + 1):
		dp[i][0] = i
	for j in range(len2 + 1):
		dp[0][j] = j
	  
	# Compute the DP Matrix
	for i in range(1, len1 + 1):
		for j in range(1, len2 + 1):
			  
			# If the characters are same 
			# no changes required 
			if s2[j - 1] == s1[i - 1]:
				dp[i][j] = dp[i - 1][j - 1]
				  
			# Minimum of three operations possible 
			else:
				dp[i][j] = 1 + min(dp[i][j - 1],
								   dp[i - 1][j - 1],
								   dp[i - 1][j])

	if(flag):
		edits = editDistance(s1, s2, dp)
		return edits, dp[len1][len2]
	else:
		return None, dp[len1][len2] 	
####################################

####################################
# majority function to check which what is the majority element of all the given list of lists 
# for a given particular index
def majority(st,idx):
	counter = defaultdict(int)
	for l in st:
		try:
			counter[l[idx]] += 1
		except:
			counter["NAE"] += 1
	return max(counter,key=counter.get)
####################################	

####################################
# code to read the traces from a file
keys = []
with open("data.txt") as f:
	lst = f.readlines()
	original_key = lst[0][:-1]
	ll = lst[1:]
	for s in ll:
		# print(editDP(s[:-1], original_key, False))
		keys.append(list(s)[:-1])
####################################


key = [] #key is the final output key
i=0

while(True):
	keybit = majority(keys,i) # majority bit in all the traces for i index
	if(keybit=="NAE"):
		break

	key.append(keybit)
	correct = []
	wrong = []
	
	####################################
	#This block places all the traces with the majority bit in correct
	#and the rest in wrong
	for idx,k in enumerate(keys):
		if(i<len(k) and k[i]==keybit):
			correct.append(idx)
		else:
			wrong.append(idx)
	####################################			

	for kw in wrong:
		actions = [] #actions is a list of lists
		for kc in correct:
			actions.append(editDP(keys[kw][i:i+lookahead],keys[kc][i:i+lookahead], True)[0])  
			#editDP returns list which says which action(replace,delete or insert) to be applied on which index of a wrong trace
		ai=0
		no_of_deletes=0 #these are just helper variables
		no_of_inserts=0
		while(i<len(keys[kw]) and keys[kw][i]!=keybit):
			action = majority(actions,ai) #action is the majority of all the lists in actions for a particular index 
			if(action == "NAE"):
				break
			
			# apply action to the index of a wrong trace
			if(action=="d"):
				keys[kw].pop(i+ai-no_of_deletes)

				no_of_deletes += 1

			elif(action[0]=="i"):
				keys[kw].insert(i+ai-no_of_deletes, action[1])
				no_of_inserts += 1
				
			elif(action[0]=="r"):
				keys[kw][i+ai-no_of_deletes] = action[1]

			ai+=1

		
	i+=1
	

final_key = "".join(key)
# checking if the recovered key matches with the original key 	
print("edit distance between final key and original key:", editDP(final_key, original_key, False)[1])
print("Key recovered:", final_key == original_key)
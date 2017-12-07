"""
***all variables begin with the tag % and end with the tag . ***

***all logical connectives begin with the tag @ ***
	bool.ops = ['@~', '@n', '@v', '@i', '@b']

***all quantifiers begin with the tag # ***
	bool.quants = ['A', 'E']

***all constants begin with the tag $ ***

***syntax charcaters***
	syntax = ['(' ,')']

***identity symbol***
	identity = ['=']
"""
constants = ['$T', '$F']
connectives = ['@~', '@n', '@v', '@i', '@b']
quantifiers = ['#A', '#E']

"""********************************************************************************************"""

def tag(string):
	return string[0]

def endtag(string):
	return string[-1]

def interior(string):
	return string[1:-1]
"""********************************************************************************************"""

def num_ops(string):
	count = 0
	for i in string:
		if (i=='@'):
			count += 1
	return count

def num_quants(string):
	count = 0
	for i in string:
		if (i=='#'):
			count += 1
	return count

"""********************************************************************************************"""

def is_clean(string):
	for i in string:
		if (i==' '):
			return False
	return True

def is_braced(string):
	if ((string[0] == '(') and string[-1] == ')'):
		return True
	return False

def is_atomic(string):
	if (not is_clean(string)):
		return False
	if ((num_ops(string) + num_quants(string)) == 0):
		return True
	else:
		return False

"""********************************************************************************************"""

def is_const(string):
	if (not is_atomic(string)):
		return False
	for i in constants:
		if (string == i):
			return True
	return False

def is_var(string):
	if (
		(tag(string) == '%') and
		(endtag(string) == '.')
		):
		return True
	return False


def is_conn(string):
	if (
		(len(string)==2) and
		(string in connectives)
		):
		return True
	return False

def is_quant(string):
	if (
		(len(string)==2) and
		(string in quantifiers)
		):
		return True
	return False

"""********************************************************************************************"""

def find_top_op(string, depth=0):
	top_op = None
	parse_depth = 0
	for j in range(0,len(string)):
		i = string[j]
		if (i=='('):
			parse_depth += 1
		elif (i==')'):
			parse_depth -= 1
		elif (
				(parse_depth==0) and
				((i=='@') or (i=='#'))
			):
			if (top_op == None):
				loc = j
				top_op = string[loc:loc+2]
				if (
						(not is_conn(top_op)) and
						(not is_quant(top_op))
					):
					print('Error finding top operation: Invalid operation symbol detected: ' + top_op + ' found at location ' + str(location))
					return False
				print(
						'operator detected: '+ top_op + '\n' +
						'location: '+ str(loc)
					  )
			else:
				print('Error finding top operation: Multiple top operations detected: ' + top_op + ', ' + i)
				return False
		if (
				(parse_depth < 0)
			):
			print('Error finding top operation: Unbalanced Parentheses. Parse depth is ' + str(parse_depth))
			return False
	if (parse_depth != 0):
		print('Error finding top operation: Unbalanced Parentheses. Parse depth is ' + str(parse_depth))
		return False
	return (top_op, loc)

def find_top_clause(string, depth=0):
	top_clause = None
	parse_depth = 0
	for j in range(0,len(string)):
		i = string[j]
		if (i=='('):
			if (parse_depth==0):
				loc = j
			parse_depth += 1
		elif (i==')'):
			parse_depth -= 1
		
		if (
				(parse_depth==0) and
				(i==')')
			):
			term = j
			found_clause = string[loc:term+1]
			print('clause detected: ' + found_clause)
			return (found_clause, loc, term)


"""********************************************************************************************"""

def is_wff(string):
	print('Testing: ' + string)
	if (not is_clean(string)):
		return False

	if (is_atomic(string)):
		if (is_var(string)):
			name = interior(string)
			print('variable detected: ' + name)
			return True
		elif (is_const(string)):
			print('constant detected: ' + string[1:])
			return True
		return False

	else:
		if (not is_braced(string)):
			print('Error parsing braces: string is non-atomic and not properly braced: ' + string)
			return False
		#Get top-level operations and try again. This can be achieved by parsing braces.
		inter = interior(string)
		top_op, loc = find_top_op(inter)
		op_type = tag(top_op)
		op_symb = endtag(top_op)
		print(
			'top operation identified. Type: ' + op_type + '\n' +
			'location: ' + str(loc)
			)

		if (op_type == '@'):
			if (not op_symb == '~'):
				clause1 = inter[:loc]
				clause2 = inter[loc+2:]
				clauses = [clause1, clause2]
			else:
				clause = inter[loc+2:]
				clauses = [clause]
			top_op_data = [top_op, clauses]
			print(string + ' ---> ' + str(top_op_data))
			print('\n')

		elif (op_type == '#'):
			clause, clause_loc, clause_term = find_top_clause(inter)
			var_str = inter[2:clause_loc]
			if (not ((tag(var_str)=='%') and (endtag(var_str)=='.'))):
				print('Error reading quantified variable; incorrectly tagged: ' + var_str)
				return False
			var = interior(var_str)
			clauses = [clause]
			top_op_data = [top_op, var, clauses]
			print(string + ' ---> ' + str(top_op_data))
			print('\n')

		for clause in clauses:
			if (not is_wff(clause)):
				return False
		print('\n')
		return True

"""********************************************************************************************"""

"""TEST ENVIRONMENT"""

print(is_wff('(#E%var1.(((%var1.@n$T)@v%var$.)@n$F))'))
print('\n')
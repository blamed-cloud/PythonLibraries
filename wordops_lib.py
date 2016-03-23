#!/usr/bin/python
#wordops_lib.py
###USAGE### wordops_lib.py ; sms=N ; $#=0
import sys
import re
import prgm_lib
import matrix_lib
memo = prgm_lib.memo
is_adjacent=matrix_lib.is_adjacent

DEFAULT_DICT='/home/denver/lib/word_data/allwords.txt'
#Function that retrieves the words from the given dictionary file (or the default dictionary if none is given)
def dict_words(dict_file='default'):
	if dict_file=='default':
		dict_file=DEFAULT_DICT
	DICT = open(dict_file, 'r')
	allwords=DICT.read()
	DICT.close()
	word_list=re.split("\n+", allwords)
	return word_list



@memo
def levenshtein(word1, word2):
	value = 0
	if word1 == word2:
		value = 0
	else:
		if len(word1) * len(word2) == 0:
			if len(word1) >= len(word2):
				value = len(word1)
			else:
				value = len(word2)
		else:
			a=word1[0]
			b=word2[0]
			if a == b:
				new1=word1[1:]
				new2=word2[1:]
				value = levenshtein(new1,new2)
			else:
				trial1 = levenshtein(word1[1:],word2[1:])
				trial2 = levenshtein(word1[:],word2[1:])
				trial3 = levenshtein(word1[1:],word2[:])
				value = 1 + min([trial1,trial2,trial3])
	return value

def num2word(num):
	if int(num)==0:
		return 'zero'
	if int(num)<0:
		ngtv=1
		num=str(abs(int(num)))
	else:
		ngtv=0
	digits=len(str(num))
	d_list=[int(x) for x in str(num)]
	m=len(d_list) / 3
	d_list3=d_list
	d_list2=[]
	if ( len(d_list) % 3 ) != 0:
		m=m+1
	for x in range(m):
		d_list2.insert(0,d_list[-3:])
		d_list=d_list[:-3]
	for x in range(len(d_list2)):
		d_list=d_list2[x]
		if len(d_list) > 1:
			if d_list[-2]==1:
				d_list[-2]=10*d_list[-2] + d_list[-1]
				d_list2[x]=d_list[:-1]
	d_words=['','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
	tens_p=['','','twenty-','thirty-','forty-','fifty-','sixty-','seventy-','eighty-','ninety-','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
	places=['','','thousand','million','billion','trillion','quadrillion','pentillion','sextillion','septillion','octillion','nonillion','decillion']
	trips=len(d_list2)
	if trips > 12:
		raise SystemExit
	if ngtv==0:
		string=''
	else:
		string='negative '
	for x in range(trips):
		pl=trips-x
		lst=d_list2[x]
		if sum(lst)==0:
			pass
		elif len(lst)==1:
			string=string + d_words[lst[0]] + ' ' + places[pl] + ' '
		elif len(lst)==2 and lst[1]<10:
			string=string + tens_p[lst[0]] + d_words[lst[1]] + ' ' + places[pl] + ' '
		elif len(lst)==2 and lst[1]>=10:
			if lst[0]==0:
				string=string + d_words[lst[1]] + ' ' + places[pl] + ' '
			else:
				string=string + d_words[lst[0]] + ' hundred and ' + d_words[lst[1]] + ' ' + places[pl] + ' '
		elif len(lst)==3 and lst[0]==0 and lst[1]==0:
			string=string + d_words[lst[2]] + ' ' + places[pl] + ' '
		elif len(lst)==3 and lst[0]==0:
			string=string + tens_p[lst[1]] + d_words[lst[2]] + ' ' + places[pl] + ' '
		elif len(lst)==3:
			string=string + d_words[lst[0]] + ' hundred and ' + tens_p[lst[1]] + d_words[lst[2]] + ' ' + places[pl] + ' '
		dontdoit=0
		if pl==1:
			if len(lst)==3 and lst[0]!=0 and lst[1]==0 and lst[2]==0 and trips>1:
				dontdoit=1
	dd=0
	string=re.sub(' and  ', ' ', string)
	string=re.sub('- ',' ',string)
	while dd==0:
		if len(string) > 1:
			if string[-1]==' ' or string[-1]=='-':
				string=string[:-1]
			else:
				dd=1
		else:
			dd=1
	if dontdoit==1:
		string=string[:-8]
	if ' ' in string:
		letters=[x for x in string]
		ltrs2=[]
		ltrs2.append(letters.pop())
		while ltrs2[-1]!=' ':
			ltrs2.append(letters.pop())
		if len(letters) > 4:
			and_w=str(letters[-4])+str(letters[-3])+str(letters[-2])+str(letters[-1])
			if and_w!=' and':
				letters.append(' and')
				while ltrs2!=[]:
					letters.append(ltrs2.pop())
				string2=''
				for x in letters:
					string2=string2 + str(x)
				string=string2
	if dontdoit==1:
		string=string + ' hundred'
	return string

def snake_search(word,tiles_list2,xgrid=4,one_d=False,out_tf=False,progress='',pos=-1,last_pos=-1,dr=[-7,-7]):
	possibles=[]
	outcome=0
	if pos==-1:
		for x in range(len(tiles_list2)):
			let=tiles_list2[x]
#			print let,word[0]
			if let==word[0]:
				possibles.append(x)
		progress=word[0]
#		print possibles,progress
		for x in possibles:
			temp_tiles2=tiles_list2
			temp_tiles2[x]=str(0)
			outcome=outcome+snake_search(word,temp_tiles2,xgrid,one_d,False,progress,x,-1,[-7,-7])
	else:
		if (progress==word):
			return 1
		else:
			if (len(progress)==2):
				if (one_d==True) and (dr==[-7,-7]):
					cr1=matrix_lib.coor_split(last_pos,xgrid)
					cr2=matrix_lib.coor_split(pos,xgrid)
					dr=[cr2[0]-cr1[0],cr2[1]-cr1[1]]
			num_lets=len(progress)
			current_let=word[num_lets]
			last_let=word[num_lets-1]
			for x in range(len(tiles_list2)):
				let=tiles_list2[x]
				if dr==[-7,-7]:
					if (let==current_let) and is_adjacent(pos,x,xgrid):
						possibles.append(x)
				else:
					cr1=matrix_lib.coor_split(pos,xgrid)
					cr2=matrix_lib.coor_split(x,xgrid)
					dr2=[cr2[0]-cr1[0],cr2[1]-cr1[1]]
					if (let==current_let) and (is_adjacent(pos,x,xgrid)) and (dr==dr2):
						possibles.append(x)
			progress=progress+current_let
#			print possibles,progress
			for x in possibles:
#				print pos,x,is_adjacent(pos,x)
				temp_tiles2=tiles_list2
				temp_tiles2[x]=str(num_lets)
				outcome=outcome+snake_search(word,temp_tiles2,xgrid,one_d,False,progress,x,pos,dr)
	if outcome>=1:
		if out_tf:
			return True
		else:
			return outcome
	else:
		if out_tf:
			return False
		else:
			return 0

def occurences(let,object1):
	num=0
	for x in object1:
		if x==let:
			num=num+1
	return num



def boggle_helper(tiles,quiet=False,dict_file='/home/denver/lib/scrabble.dict',use_out_file=False,out_file='/home/denver/lib/boggle.wl_py'):
	if quiet==1:
		quiet=True
	elif quiet==0:
		quiet==False
	alphnum='abcdefghijklmnopqrstuvwxyz0123456789_'
	alph='abcdefghijklmnopqrstuvwxyz'
	num='0123456789'
	if dict_file=='default':
		dict_file='/home/denver/lib/scrabble.dict'
	DICT= open(dict_file, 'r')
	allwords=DICT.read()
	DICT.close()
	allwords=re.sub('[q][u]','@',allwords)
	word_list=re.split("\n+", allwords)
	tiles=re.sub('[q][u]','@',tiles)
	tiles_list=[l for l in tiles]
	sorted_list=[l for l in tiles]
	sorted_list.sort()
	no_dupes=[]
	for let in sorted_list:
		if let not in no_dupes:
			no_dupes.append(let)
	let_freq=[occurences(let,sorted_list) for let in no_dupes]
	refined_wl=[]
	for word in word_list:
		num_lets=0
		word_fail=0
		for x in range(len(no_dupes)):
			letter=no_dupes[x]
			occ=let_freq[x]
			num1=occurences(letter,word)
			if (num1 > occ):
				word_fail=1
			else:
				num_lets=num_lets+num1
		if (word_fail==1) or (num_lets < 3) or ( num_lets != len(word) ):
			pass
		else:
			refined_wl.append(word)
	refined_wl2=[]
	for word in refined_wl:
		tiles_list=[l for l in tiles]   ### this line shouldn't be neccessary, but it is. somehow, the function snake_search is editing the real value of tiles_list ###
		outcome=snake_search(word,tiles_list)
		if (outcome!=0):
			refined_wl2.append(word)
#			print re.sub('[@]','qu',word)
	if use_out_file==True:
		output=open(out_file, 'w')
	word_list_s=sorted(refined_wl2, key=lambda k: len(k), reverse=True)
	for word in word_list_s:
		text=re.sub('[@]','qu',word)
		if quiet==False:
			print text
		if use_out_file==True:
			output.write(text)
			output.write('\n')
	if use_out_file==True:
		output.close()

#!/usr/bin/python
#chess_lib.py
###USAGE### chess_lib.py ; sms=N ; $#=0
import sys
import re
import blessings
import matrix_lib
import prgm_lib
clear=prgm_lib.cls
get_xy=matrix_lib.coor_split
T=blessings.Terminal()
opg=matrix_lib.opg

piece_values={'p':1,'r':5,'n':3,'b':3,'q':9,'k':9001}

def startfen():
	return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

def threat_matrices(fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	turn=splitFEN[1]
	wtm=[]
	btm=[]
	for y1 in range(8):
		wtm.append([])
		btm.append([])
		for x1 in range(8):
			pc=matrix[y1][x1]
			if turn=='w':
				matrix[y1][x1]='n'
				w_fen=join_fen([matrix,'w',splitFEN[2],splitFEN[3],splitFEN[4],splitFEN[5]])
				matrix[y1][x1]='N'
				b_fen=join_fen([matrix,'b','-','-',splitFEN[4],splitFEN[5]])
			else:
				matrix[y1][x1]='N'
				b_fen=join_fen([matrix,'b',splitFEN[2],splitFEN[3],splitFEN[4],splitFEN[5]])
				matrix[y1][x1]='n'
				w_fen=join_fen([matrix,'w','-','-',splitFEN[4],splitFEN[5]])
			matrix[y1][x1]=pc
			tempw=0
			tempb=0
			if pc=='P':
				tempw=1
			elif pc=='p':
				tempb=1
			for y0 in range(8):
				for x0 in range(8):
					pcf=matrix[y0][x0]
					if is_valid_move(x0,y0,x1,y1,w_fen):
						if pcf=='P':
							if is_p_capture(x0,y0,x1,y1,w_fen):
								tempw=tempw+1
						else:
							tempw=tempw+1
					if is_valid_move(x0,y0,x1,y1,b_fen):
						if pcf=='p':
							if is_p_capture(x0,y0,x1,y1,b_fen):
								tempb=tempb+1
						else:
							tempb=tempb+1
			wtm[-1].append(tempw)
			btm[-1].append(tempb)
	return [wtm,btm]
	
def total_tm(wtm,btm):
	ttm=[]
	for y in range(8):
		ttm.append([])
		for x in range(8):
			ttm[-1].append(wtm[y][x] - btm[y][x])
	return ttm
	
def points(fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	wp=0
	bp=0
	for y in range(8):
		for x in range(8):
			if is_white(matrix[y][x]):
				wp=wp+piece_values[low(matrix[y][x])]
			elif is_black(matrix[y][x]):
				bp=bp+piece_values[low(matrix[y][x])]
	return [wp,bp,wp-bp]		

def split_fen(fen):
	split=re.split(' ',fen)
	board_string=split[0]
	temp_s=''
	for x in board_string:
		if re.search('[0-9]',x):
			for k in range(int(x)):
				temp_s = temp_s + '1'
		else:
			temp_s = temp_s + x
	grid0=re.split('/',temp_s)
	temp_l=[[k for k in l] for l in grid0]
	split[0]=temp_l
	return split

def join_fen(splitFEN):
	matrix=splitFEN[0]
	num=False
	string=''
	s=' '
	temp_num=0
	for y in range(8):
		for x in range(8):
			if matrix[y][x]=='1':
				num=True
				temp_num=temp_num+1
			else:
				if num==True:
					string=string + str(temp_num) + matrix[y][x]
					num=False
					temp_num=0
				else:
					string=string + matrix[y][x]
		if num==True:
			string=string + str(temp_num)
			num=False
			temp_num=0
		if y!=7:
			string=string+'/'
	fen=string +s+ splitFEN[1] +s+ splitFEN[2] +s+ splitFEN[3] +s+ splitFEN[4] +s+ splitFEN[5]
	return fen

def get_board(fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	return matrix

def is_white(piece):
	if re.search('[A-Z]',piece):
		return True
	else:
		return False
def is_black(piece):
	if re.search('[a-z]',piece):
		return True
	else:
		return False
to_upper={'a':'A','b':'B', 'c':'C','d':'D','e':'E','f':'F','g':'G', 'h':'H','i':'I','j':'J','k':'K','l':'L','m':'M','n':'N','o':'O', 'p':'P','q':'Q','r':'R','s':'S', 't':'T','u':'U','v':'V', 'w':'W', 'x':'X', 'y':'Y', 'z':'Z'}

def up(string):
	if string in to_upper:
		return to_upper[string]
	else:
		return string

def low(string):
	if string in to_upper.values():
		return to_upper.keys()[to_upper.values().index(string)]
	else:
		return string

def unicode_piece(pc):
#	if pc=='P':
#		return ''
#	if pc=='K':
#		return ''
#	if pc=='Q':
#		return ''
#	if pc=='R':
#		return ''
#	if pc=='B':
#		return ''
#	if pc=='N':
#		return ''
#	if pc=='k':
#		return ''
#	if pc=='q':
#		return ''
#	if pc=='r':
#		return ''
#	if pc=='b':
#		return ''
#	if pc=='n':
#		return ''
#	if pc=='p':
#		return ''
#	if pc=='1':
#		return ' '
	return pc

def print_board(fen,help_alg=True,black_flip=True,use_uni=False):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	turn=splitFEN[1]
	if black_flip and turn=='b':
		help_str='    h  g  f  e  d  c  b  a    '
	else:
		help_str='    a  b  c  d  e  f  g  h    '
	if help_alg:
		print help_str
	for k in range(8):
		if black_flip and turn=='b':
			y=7-k
		else:
			y=k
		if help_alg:
			print ' ' + str(8-y),
		for j in range(8):
			if black_flip and turn=='b':
				x=7-j
			else:
				x=j
			if use_uni:
				thing=unicode_piece(matrix[y][x])
			else:
				thing=up(matrix[y][x])
			if ((y+x) % 2) == 0:
				if matrix[y][x]=='1':
					print T.on_white + '  ',
				elif re.search('[a-z]',matrix[y][x]):
					print T.black + T.on_white + ' ' + thing,
				else:
					print T.red + T.on_white + ' ' + thing,
			else:
				if matrix[y][x]=='1':
					print T.on_blue + '  ',
				elif re.search('[a-z]',matrix[y][x]):
					print T.black + T.on_blue + ' ' + thing,
				else:
					print T.red + T.on_blue + ' ' + matrix[y][x],
		if help_alg:
			print T.normal + ' ' + str(8-y) + ' '
		else:
			print T.normal
	if help_alg:
		print help_str

def sqrs_btwn(x0,y0,x1,y1):
	if x1-x0>1:
		xs=range(x0+1,x1)
		dx='i'
	elif x0-x1>1:
		dx='d'
		xs=range(x1+1,x0)
	else:
		xs=[x0]
	if y1-y0>1:
		dy='i'
		ys=range(y0+1,y1)
	elif y0-y1>1:
		dy='d'
		ys=range(y1+1,y0)
	else:
		ys=[y0]
	if len(xs)==1 or len(ys)==1:
		if len(xs)==len(ys):
			if [xs[0],ys[0]]==[x0,y0]:
				return []
			else:
				return [(xs[0],ys[0])]
		else:
			if len(xs)==1:
				return [zip(xs,[ys1])[0] for ys1 in ys]
			else:
				return [zip([xs1],ys)[0] for xs1 in xs]
	elif len(xs)==len(ys):
		if dx==dy:
			return zip(xs,ys)
		else:
			return zip(xs,reversed(ys))
	else:
		return []

def empty_btwn(x0,y0,x1,y1,fen):
	matrix=get_board(fen)
	sqrs=sqrs_btwn(x0,y0,x1,y1)
#	print x0,y0,x1,y1
#	print sqrs   #############################
	if sqrs==[]:
		return True
	else:
		for tup in sqrs:
			if matrix[tup[1]][tup[0]]!='1':
				return False
	return True

def is_n_move(x0,y0,x1,y1):
	if (abs(x1-x0)==2) and (abs(y1-y0)==1):
		return True
	elif (abs(x1-x0)==1) and (abs(y1-y0)==2):
		return True
	else:
		return False

def is_b_move(x0,y0,x1,y1):
	if abs(y1-y0)==abs(x1-x0):
		return True
	else:
		return False

def is_r_move(x0,y0,x1,y1):
	if (x0!=x1) and (y0==y1):
		return True
	elif (x0==x1) and (y0!=y1):
		return True
	else:
		return False

def is_q_move(x0,y0,x1,y1):
	if is_b_move(x0,y0,x1,y1) or is_r_move(x0,y0,x1,y1):
		return True
	else:
		return False

def is_k_move(x0,y0,x1,y1):
	dx=abs(x1-x0)
	dy=abs(y1-y0)
	if ((dx+dy)<=2) and ((dx+dy)>0) and (dx<=1) and (dy<=1):
		return True
	else:
		return False

def is_castle(x0,y0,x1,y1,fen):
	splitFEN=split_fen(fen)
	turn=splitFEN[1]
	cstle=splitFEN[2]
	matrix=splitFEN[0]
	if y1!=y0:
		return False
	if abs(x1-x0)!=2:
		return False
	if check_in_check(fen):
		return False
	if turn=='w':
		xk=4
		yk=7
		king='K'
		rook='R'
		checks=['K','Q']
	else:
		xk=4
		yk=0
		king='k'
		rook='r'
		checks=['k','q']
	if x0!=xk or y0!=yk:
		return False
	if x1-x0==2:
		num=0
		xr=7
		yr=yk
		dx=1
	else:
		num=1
		xr=0
		yr=yk
		dx=-1
	if checks[num] not in cstle:
		return False
	if matrix[yr][xr]!=rook:
		return False
	if not empty_btwn(xk,yk,xr,yr,fen):
		return False
	matrix[yk][xk]='1'
	matrix[yk][xk+dx]=king
#	print 'test'
#	print_board(join_fen([matrix,turn,'-','-',splitFEN[4],splitFEN[5]]))
	if check_in_check(join_fen([matrix,turn,'-','-',splitFEN[4],splitFEN[5]])):
		return False
	matrix[yk][xk+dx]='1'
	matrix[yk][xk+dx+dx]=king
	if check_in_check(join_fen([matrix,turn,'-','-',splitFEN[4],splitFEN[5]])):
		return False
	return True

def is_p_move(x0,y0,x1,y1,fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	if is_white(matrix[y0][x0]):
		is_w=True
	else:
		is_w=False
	if matrix[y1][x1]!='1':
		return False
	if x0!=x1:
		return False
	if (is_w):
		if y1==7:
			return False
		if y0==6:
			if y1==5 or y1==4:
				return True
			else:
				return False
		else:
			if (y0-y1)==1:
				return True
			else:
				return False
	else:
		if y1==0:
			return False
		if y0==1:
			if y1==2 or y1==3:
				return True
			else:
				return False
		else:
			if (y1-y0)==1:
				return True
			else:
				return False

def is_p_capture(x0,y0,x1,y1,fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	if is_white(matrix[y0][x0]):
		is_w=True
		if not is_black(matrix[y1][x1]):
			return False
	else:
		is_w=False
		if not is_white(matrix[y1][x1]):
			return False
	if matrix[y1][x1]=='1':
		return False
	if abs(x1-x0)!=1:
		return False
	if (is_w):
		if (y0-y1)==1:
			return True
		else:
			return False
	else:
		if (y1-y0)==1:
			return True
		else:
			return False

x_dict={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
rxdict={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

def not_string(x,y):
	y1=8-y
	string=x_dict[x]+str(y1)
	return string

def not2coors(alg):
	x=int(rxdict[alg[0]])
	y=8-int(alg[1])
	return [x,y]

def is_ep(x0,y0,x1,y1,fen):
	splitFEN=split_fen(fen)
	algn=not_string(x1,y1)
	if algn!=splitFEN[3]:
		return False
	if abs(x1-x0)!=1:
		return False
	if abs(y1-y0)!=1:
		return False
	return True

def is_any_p_move(x0,y0,x1,y1,fen):
	if is_ep(x0,y0,x1,y1,fen) or is_p_capture(x0,y0,x1,y1,fen) or is_p_move(x0,y0,x1,y1,fen):
		return True
	else:
		return False

def is_valid_move(x0,y0,x1,y1,fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	if 0>int(x0) or 7<int(x0):
		return False
	if 0>int(y0) or 7<int(y0):
		return False
	if 0>int(x1) or 7<int(x1):
		return False
	if 0>int(y1) or 7<int(y1):
		return False	
	pc=matrix[y0][x0]
	fpc=matrix[y1][x1]
	if pc=='1':
		return False
	else:
		if is_white(pc):
			if splitFEN[1]=='b':
				return False
			else:
				if is_white(fpc):
					return False
		else:
			if splitFEN[1]=='w':
				return False
			else:
				if is_black(fpc):
					return False
	if not empty_btwn(x0,y0,x1,y1,fen):
#		print 'quit because pieces between'
		if not re.search('[n]',pc,re.I):
			return False
	if re.search('[p]',pc,re.I):
		if is_any_p_move(x0,y0,x1,y1,fen):
			return True
		else:
#			print 'quit because its not a pawn move'
			return False
	elif re.search('[r]',pc,re.I):
		if is_r_move(x0,y0,x1,y1):
			return True
		else:
			return False
	elif re.search('[n]',pc,re.I):
		if is_n_move(x0,y0,x1,y1):
			return True
		else:
			return False
	elif re.search('[b]',pc,re.I):
		if is_b_move(x0,y0,x1,y1):
			return True
		else:
			return False
	elif re.search('[q]',pc,re.I):
		if is_q_move(x0,y0,x1,y1):
			return True
		else:
			return False
	elif re.search('[k]',pc,re.I):
		if is_k_move(x0,y0,x1,y1) or is_castle(x0,y0,x1,y1,fen):
			return True
		else:
			return False
	else:
		return False

def check_in_check(fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	if splitFEN[1]=='w':
		plyr='b'
		king='K'
	else:
		plyr='w'
		king='k'
	cons=[matrix,plyr,'-','-',splitFEN[4],splitFEN[5]]
	newfen=join_fen(cons)
	for y in range(8):
		for x in range(8):
			if matrix[y][x]==king:
				x1=x
				y1=y
	for y in range(8):
		for x in range(8):
			if is_valid_move(x,y,x1,y1,newfen):
				return True
	return False

def check_gameover(fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	if int(splitFEN[4])>=50:
		return True
	for y0 in range(8):
		for x0 in range(8):
			for y1 in range(8):
				for x1 in range(8):
					if x1!=x0 and y1!=y0:
						if is_valid_move(x0,y0,x1,y1,fen):
							new=move(x0,y0,x1,y1,fen)
							if check_check(fen,new)==new:
								return False
	return True

def check_check(last,fen):
#	print last
#	print fen
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	turn=splitFEN[1]
	if turn=='w':
		king='k'
	else:
		king='K'
	for y in range(8):
		for x in range(8):
#			print y,x
			if matrix[y][x]==king:
				x1=x
				y1=y
	for y in range(8):
		for x in range(8):
			if is_valid_move(x,y,x1,y1,fen):
				return last
	return fen


def cr2str(cr):
	string=''
	if cr[0]==1:
		string=string+'K'
	if cr[1]==1:
		string=string+'Q'
	if cr[2]==1:
		string=string+'k'
	if cr[3]==1:
		string=string+'q'
	if string=='':
		string='-'
	return string

def str2cr(cstle):
	cr=[]
	if 'K' in cstle:
		cr.append(1)
	else:
		cr.append(0)
	if 'Q' in cstle:
		cr.append(1)
	else:
		cr.append(0)
	if 'k' in cstle:
		cr.append(1)
	else:
		cr.append(0)
	if 'q' in cstle:
		cr.append(1)
	else:
		cr.append(0)
	return cr

def move(x0,y0,x1,y1,fen,check=False):
	if check:
		if not is_valid_move(x0,y0,x1,y1,fen):
			return fen
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	pc=matrix[y0][x0]
	fpc=matrix[y1][x1]
	cstle=splitFEN[2]
	cr=str2cr(cstle)
	if splitFEN[1]=='w':
		new_turn='b'
		new_num=splitFEN[5]
	else:
		new_turn='w'
		new_num=str(int(splitFEN[5])+1)
	if re.search('[p]',pc,re.I):
		new_hnum='0'
		if (x1==x0) and abs(y1-y0)==2:
			if new_turn=='b':
				ep_sqr=not_string(x0,y1+1)
			else:
				ep_sqr=not_string(x0,y0+1)
		elif not_string(x1,y1)==splitFEN[3]:
			matrix[y0][x0]='1'
			if new_turn=='b':
				matrix[y1][x1]='P'
			else:
				matrix[y1][x1]='p'
			matrix[y0][x1]='1'
			return join_fen([matrix,new_turn,cstle,'-',new_hnum,new_num])
		else:
			ep_sqr='-'
	else:
		ep_sqr='-'
		new_hnum=str(int(splitFEN[4])+1)
	if re.search('[k]',pc,re.I):
		if new_turn=='b':
			cr=[0,0,cr[2],cr[3]]
		else:
			cr=[cr[0],cr[1],0,0]
		if abs(x1-x0)!=1:
			if new_turn=='b':
				rook='R'
				king='K'
			else:
				rook='r'
				king='k'
			if x1-x0==2:
				matrix[y0][x0]='1'
				matrix[y0][x0+1]=rook
				matrix[y0][x1]=king
				matrix[y0][x1+1]='1'
			else:
				matrix[y0][0]='1'
				matrix[y0][x1]=king
				matrix[y0][x1+1]=rook
				matrix[y0][x0]='1'
			return join_fen([matrix,new_turn,cr2str(cr),ep_sqr,new_hnum,new_num])
	if re.search('[r]',pc,re.I):
		if y0==0 and x0==0:
			cr=[cr[0],cr[1],cr[2],0]
		if y0==0 and x0==7:
			cr=[cr[0],cr[1],0,cr[3]]
		if y0==7 and x0==0:
			cr=[cr[0],0,cr[2],cr[3]]
		if y0==7 and x0==7:
			cr=[0,cr[1],cr[2],cr[3]]
	matrix[y0][x0]='1'
	matrix[y1][x1]=pc
	new_fen=join_fen([matrix,new_turn,cr2str(cr),ep_sqr,new_hnum,new_num])
#	print new_fen
	return new_fen

def get_alg_move(prompt=''):
	if prompt!='':
		print prompt
	while True:
		try1=raw_input()
		if re.match('^[o][-][o]([-][o])?$',try1,re.I):
			return try1
		if len(try1)==2:
			if re.search('[a-h]',try1[0],re.I) and re.search('[1-8]',try1[1],re.I):
				return 'p'+try1
		elif len(try1)==3:
			if re.search('[xprnbkq]',try1[0],re.I) and re.search('[a-h]',try1[1],re.I) and re.search('[1-8]',try1[2],re.I):
				return try1
		elif len(try1)==4:
			if re.search('[prnbkq]',try1[0],re.I) and re.search('[xa-h1-8]',try1[1],re.I) and re.search('[a-h]',try1[2],re.I) and re.search('[1-8]',try1[3],re.I):
				return try1
		elif len(try1)==5:
			if re.search('[prnbkq]',try1[0],re.I) and re.search('^[a-h]$ | ^[1-8]$',try1[1],re.I) and re.search('[x]',try1[2],re.I) and re.search('[a-h]',try1[3],re.I) and re.search('[1-8]',try1[4],re.I):
				return try1
		print 'That was not a correct move in algebraic notation, try again: ',


def algmove2coors(alg,fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	turn=splitFEN[1]
	files='abcdefgh'
	ranks='12345678'
	capture=False
	if re.match('^[o][-][o]([-][o])?$',alg,re.I):
		if turn=='w':
			x0=4
			y0=7
		else:
			x0=4
			y0=0
		if len(alg)==3:
			y1=y0
			x1=x0+2
		else:
			y1=y0
			x1=x0-2
	else:
		end_sqr=alg[-2] + alg[-1]
		rest=alg[:-2]
		fincrs=not2coors(end_sqr)
		x1=fincrs[0]
		y1=fincrs[1]
		if len(rest)==0:
			move='p'
		elif len(rest)==1:
			if rest=='x':
				capture=True
				move='p'
			else:
				move=low(rest)
		elif len(rest)==2:
			if rest[-1]=='x':
				capture=True
			else:
				if re.search('[a-h]',rest[-1],re.I):
					files=low(rest[-1])
				else:
					ranks=low(rest[-1])
			move=low(rest[0])
		elif len(rest)==3:
			capture=True
			move=low(rest[0])
			if re.search('[a-h]',rest[1],re.I):
				files=low(rest[1])
			else:
				ranks=low(rest[1])
		if turn=='w':
			pc=up(move)
		else:
			pc=low(move)
		unf=True
		for k in ranks:
			y=int(k)-1
			for h in files:
				x=rxdict[h]
				if matrix[y][x]==pc:
					if is_valid_move(x,y,x1,y1,fen):
						if unf==True:
							x0=x
							y0=y
							unf=False
						else:
							return [-1,-1,-1,-1]
		if unf:
			return [-1,-1,-1,-1]
	return [x0,y0,x1,y1]


def get_alg(prompt=''):
	if prompt!='':
		print prompt
	while True:
		try1=raw_input()
		if len(try1)==2:
			if re.search('[a-h]',try1[0],re.I) and re.search('[1-8]',try1[1],re.I):
				return try1
		print 'That was not correct algebraic notation (i.e. "a4" or "g6") please try again: ',

def end_cond(fen):
	splitFEN=split_fen(fen)
	matrix=splitFEN[0]
	if splitFEN[1]=='w':
		player='Black'
	else:
		player='White'
	if int(splitFEN[4])>=50:
		print 'Game ended due to 50 move draw.'
		return [.5,.5]
	if check_in_check(fen):
		print player + ' won the game'
		if player=='Black':
			return [0,1]
		else:
			return [1,0]
	else:
		print 'Game ended due to a stalemate.'
		return [.5,.5]
	

def play_2h(start_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
	fen_l=[]
	fen_l.append(start_fen)
	while True:
		current=fen_l[-1]
		splitFEN=split_fen(current)
		clear()
		print 'The current Forsyth-Edwards Notation is:'
		print '	' + current
		print
		print_board(current)
		if splitFEN[1]=='w':
			player='White'
		else:
			player='Black'
		string=player + ', it is your turn. Enter your next move. (in algebraic notaion) > '
#		sqr1=get_alg()
#		print 'what square do you want to move to? (also in alg. notation)'		
##		threat_mats=threat_matrices(current)
##		print 'White\'s threat matrix:'
##		opg(threat_mats[0])
##		print 'Black\'s threat matrix'
##		opg(threat_mats[1])
#		sqr2=get_alg()
		coors=[-1,-1,-1,-1]
		while coors==[-1,-1,-1,-1]:
			alg=get_alg_move(string)
			coors=algmove2coors(alg,current)
		coor0=coors[:2]
		coor1=coors[-2:]
		if is_valid_move(coor0[0],coor0[1],coor1[0],coor1[1],current):
			newfen=move(coor0[0],coor0[1],coor1[0],coor1[1],current)
			pos=check_check(current,newfen)
			if pos==newfen:
				if check_gameover(newfen):
					clear()
					print 'Game Over:'
					print_board(newfen)
					score=end_cond(newfen)
					fen_l.append(newfen)
					return fen_l
				fen_l.append(newfen)



size = 8

# file Index to File Letter
def numToLetter(num, BW):
	return 'ABCDEFGH'[num] if BW else 'HGFEDCBA'[num]

def numToRank(num, BW):
	return size-num if BW else num+1

def indToCoord(rankIndex, fileIndex, BW):
	return numToLetter(fileIndex, BW) + str(numToRank(rankIndex, BW))

# Doesn't actually depend on BW
def calcColor(rankIndex, fileIndex, BW):
	return 'black' if (rankIndex + fileIndex) % 2 else 'white'

pieceMap = {
	'king' : '9818',
	'queen' : '9819',
	'rook' : '9820',
	'bishop' : '9821',
	'knight' : '9822',
	'pawn' : '9823'
}

boardLayout = [
	'♜♞♝♛♚♝♞♜', 
	'♟♟♟♟♟♟♟♟',
	'        ',
	'        ',
	'        ',
	'        ',
	'♟♟♟♟♟♟♟♟',
	'♜♞♝♛♚♝♞♜', 
]

colorOffset = 6		# Black unicode chess piece codes are 
					#  6 greater than the corresponding white piece

def pieceInfo(rankIndex, fileIndex, BW):
	if not BW:
		rankIndex, fileIndex = 7-rankIndex, 7-fileIndex
	pieceChar = boardLayout[rankIndex][fileIndex];
	if pieceChar.isspace():
		return ''
	code = ord(pieceChar)
	color = 'black' if rankIndex < 4 else 'white'
	return '''
	<div class="piece {COLOR}">
		<div class="piece-outline">
			&#{OUTLINE_CODE};
		</div>
		<div class="piece-content">
			&#{PIECE_CODE};
		<div>
	</div>
	'''.format(COLOR=color, OUTLINE_CODE=code-colorOffset, PIECE_CODE=code)

def tr(rankIndex, BW):
	out = '\t<tr>\n'
	out += '\t\t<th class="rank axis axis_left" data-hide-axis="true">{RANK}</th>\n'.format(RANK=numToRank(rankIndex, BW))
	for fileIndex in range(size):
		out += '\t\t<td class="square {COLOR}" id={BW}_{COORD}>{PIECE}</td>\n'.format(
			BW='BW'[BW], 
			COLOR=calcColor(rankIndex, fileIndex, BW), 
			COORD=indToCoord(rankIndex, fileIndex, BW),
			PIECE=pieceInfo(rankIndex, fileIndex, BW)
			)
		
	out += '\t\t<th class="rank axis axis_righ" data-hide-axis="true">{RANK}</th>\n'.format(RANK=numToRank(rankIndex, BW))
	out += '\t</tr>\n'
	return out

def tr_label(top_bot, BW):
	out = '\t<tr>\n'
	out += '\t\t<th></th>\n'
	for i in range(size):
		out += '\t\t<th class="file axis axis_{TOP_BOT}" data-hide-axis="true">{FILE}</th>\n'.format(TOP_BOT=top_bot, FILE=numToLetter(i,BW))
	out += '\t\t<th></th>\n'
	out += '\t</tr>\n'
	return out

def makeBoard(BW):
	out = '<table class="board" id="{BW}_board"{HIDDEN}>\n'.format(BW='BW'[BW], HIDDEN=' data-hide-board="true"' if not BW else '')
	out += tr_label('top', BW)
	for rankIndex in range(size):
		out += tr(rankIndex, BW)
	out += tr_label('bot', BW)
	out += '</table>'
	return out

boards = makeBoard(True) + '\n' + makeBoard(False)

template = open('index.template.html').read()
contents = template.replace('#board#', boards)
open('../index.html', 'w').write(contents)

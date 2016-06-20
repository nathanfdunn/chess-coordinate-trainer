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

def tr(rankIndex, BW):
	out = '\t<tr>\n'
	out += '\t\t<th class="rank axis axis_left" data-hide-axis="false">{RANK}</th>\n'.format(RANK=numToRank(rankIndex, BW))
	for fileIndex in range(size):
		out += '\t\t<td class="square {COLOR}" id={BW}_{COORD}></td>\n'.format(
			BW='BW'[BW], 
			COLOR=calcColor(rankIndex, fileIndex, BW), 
			COORD=indToCoord(rankIndex, fileIndex, BW))
		
	out += '\t\t<th class="rank axis axis_righ" data-hide-axis="false">{RANK}</th>\n'.format(RANK=numToRank(rankIndex, BW))
	out += '\t</tr>\n'
	return out

def tr_label(top_bot, BW):
	out = '\t<tr>\n'
	out += '\t\t<th></th>\n'
	for i in range(size):
		out += '\t\t<th class="file axis axis_{TOP_BOT}" data-hide-axis="false">{FILE}</th>\n'.format(TOP_BOT=top_bot, FILE=numToLetter(i,BW))
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

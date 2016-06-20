
var indicator = document.getElementById('indicator');
var timeoutId;
function indicate(status){
	indicator.className = status;
	indicator.textContent = status.toUpperCase();
	clearTimeout(timeoutId);
	timeoutId = setTimeout(function(){
		indicator.className = '';
		indicator.textContent = '';
	}, 400);
}

var state = {};

state.targetCoord = null;

state.mode = 'type';

state.publishGuess = function (guess, inputSource) {
	if (this.mode !== inputSource) return;

	if (this.targetCoord === guess) {
		indicate('correct');
		this.randomizeTargetCoord();
	} else {
		indicate('incorrect');
		if (this.newOnFail){
			this.randomizeTargetCoord();
		}
	}
};

state.setOrientation = function (perspectiveIsWhite) {
	var whiteBoard = document.getElementById('W_board');
	var blackBoard = document.getElementById('B_board');

	if (perspectiveIsWhite) {
		whiteBoard.setAttribute('data-hide-board', 'false');
		blackBoard.setAttribute('data-hide-board', 'true');
	} else {
		whiteBoard.setAttribute('data-hide-board', 'true');
		blackBoard.setAttribute('data-hide-board', 'false');
	}
};

document.getElementById('mode-type').onchange = function(){
	state.mode = 'type';
	document.getElementById('input-group').setAttribute('data-hide-input', 'false');
	document.getElementById('click-mode-group').setAttribute('data-hide-input', 'true');
	state.randomizeTargetCoord();
};

document.getElementById('mode-click').onchange = function(){
	state.mode = 'click';
	document.getElementById('input-group').setAttribute('data-hide-input', 'true');
	document.getElementById('click-mode-group').setAttribute('data-hide-input', 'false');
	state.randomizeTargetCoord();
};

document.getElementById('failure').onchange = function(){
	state.newOnFail = document.getElementById('failure').checked;
};


state.randomizeTargetCoord = function () {
	var newCoord;
	do {
		var file = Math.floor(Math.random() * 8);
		var rank = Math.floor(Math.random() * 8)+1;
		newCoord = 'ABCDEFGH'[file] + rank;
	} while (this.targetCoord === newCoord);

	this.targetCoord = newCoord;

	// Clear type-mode stuff
	var squares = document.getElementsByClassName('square');
	for (var i=0; i<squares.length; i++){
		squares[i].removeAttribute('highlighted');
	}

	// Clear click-mode stuff
	document.getElementById('target-coord').textContent = '';

	if (this.mode === 'click'){
		document.getElementById('target-coord').textContent =this.targetCoord;
		// = canonincalToFormattedCoord( this.targetCoord, this.orientation );
	} else {
		document.getElementById('W_'+this.targetCoord).setAttribute('highlighted', 'true');
		document.getElementById('B_'+this.targetCoord).setAttribute('highlighted', 'true');
	}
};

document.getElementById('show-labels').onclick = function () {
	var axes = document.getElementsByClassName('axis');
	for (var i=0; i<axes.length; i++){
		if (this.checked) {
			axes[i].removeAttribute('data-hide-axis');
		} else {
			axes[i].setAttribute('data-hide-axis','true');
		}
	}	
};

document.getElementById('coord-input').onkeydown = function (event){
	if (event.keyCode == 13){ 		// ENTER
		var guess = this.value.trim().toUpperCase();
		state.publishGuess(guess, 'type');
		this.value = '';
	}
};

document.getElementById('player-white').onchange = function () {
	state.setOrientation(true);
};

document.getElementById('player-black').onchange = function () {
	state.setOrientation(false);
};

var squares = document.getElementsByClassName('square');
for (var i=0; i<squares.length; i++){
	squares[i].onclick = function () {
		state.publishGuess(this.id.split('_')[1], 'click');
	};
}

state.randomizeTargetCoord();

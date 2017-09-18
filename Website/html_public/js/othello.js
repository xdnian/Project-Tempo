/*
  prepare the new board for the new game
*/
function restart() {
	currentplayer = pieces[0];
	for (var i = 0; i < 8; i++) {
		for (var j = 0; j < 8; j++) {
			gameboard[i][j] = ".";
		}
	}

	record = "";
	update_old();

	gameboard[3][3] = pieces[1];
	gameboard[3][4] = pieces[0];
	gameboard[4][3] = pieces[0];
	gameboard[4][4] = pieces[1];

	validateAndCount();
	display();
	handleEvent();
	$("#downloadRecord").remove();
}

/*
  let the oldboard updated with the gameboard
*/
function update_old() {
	for (var i = 0; i < 8; i++) {
		for (var j = 0; j < 8; j++) {
			oldboard[i][j] = gameboard[i][j];
		}
	}
}

/*
  clean the old element
*/
function cleanboard() {
	for (var i = 0; i < 8; i++) {
		for (var j = 0; j < 8; j++) {
			for (var k = 0; k < 2; k++) {
				var chess_id = elementName[k] + i + j;
				$('#' + chess_id).remove();
			}
		}
	}
}


/*
  display all the pieces and let the valid possible moves to be seen when hovered on
*/
function display() {

	var top = $("#chessboard").position().top; // top posotion of the whole chess board
	var left = $("#chessboard").position().left; // left posotion of the whole chess board
	var edge = 40;
	var chess_size = 65;
	if ($( window ).width() < 768){
		edge = 40/600 * $( window ).width();
		chess_size = 65/600 * $( window ).width();
	}

	var board = $("#board");
	board.css("top", top + "px");
	board.css("left", left + "px");

	cleanboard();
	update_old();

	for (var i = 0; i < 8; i++) {
		for (var j = 0; j < 8; j++) {
			for (var k = 0; k < 2; k++) {
				if (gameboard[i][j] == pieces[k]) {

					var chess_id = elementName[k] + i + j;

					var xcoor = left + edge + j * chess_size;
					var ycoor = top + edge + i * chess_size;
					$("#chessboard").append('<div class="chess" id="' + chess_id + '"></div>');
					$("#" + chess_id).css({
						"top": ycoor + "px",
						"left": xcoor + "px"
					});
					$("#" + chess_id).append('<img src="' + photoScource[k] + '">');
				}

				// here we want to add the possible moves to be elements
				if (validboard[k][i][j] == currentplayer) {
					var chess_id = elementName[k] + i + j;
					var xcoor = left + edge + j * chess_size;
					var ycoor = top + edge + i * chess_size;
					$("#chessboard").append('<div class="chess hover" id="' + elementName[k] + i + j + '"></div>');
					$("#" + chess_id).css({
						"top": ycoor + "px",
						"left": xcoor + "px"
					});
					$("#" + chess_id).append('<img src="' + photoScource[k + 2] + '">');
				}
			}
		}
	}

	$("#blackstones").text(stones[0]);
	$("#whitestones").text(stones[1]);
}

function handleEvent() {

	for (var k = 0; k < 2; k++) {
		$(".chess.hover").children('img').hide();
		if (currentplayer == pieces[k]) {
			if ((currentplayer == pieces[0]) == user_is_black){
				$(".chess.hover").mouseenter(function() {
					$(this).children('img').show();
				});
				$(".chess.hover").mouseleave(function() {
					$(this).children('img').hide();
				});
				$(".chess.hover").click(function() {
					var name = $(this).get(0).id;
					update(Number(name[5]), Number(name[6]));
				});
			}
			else {
				if (!(stones[0] == 0 || stones[1] == 0 || stones[0] + stones[1] == 64 || (validmoves[0] == 0 && validmoves[1] == 0)))
				{
					$.post('http://172.31.115.212:8888/', {"board": get_board(), "wait_time": 3}, 
					function(data, status){
						if (status == 'success'){
							console.log(data);
							move = get_move(data["move"]);
							update(move[0], move[1]);
						}
					});
				}
			}
		}
	}
}

function get_board() {
	var board="$$$$$$$$$$"
	for (var i = 0; i < 8; i++) {
		board += "$";
		for (var j = 0; j < 8; j++) {
			board += gameboard[7-i][j];
		}
		board += "$";
	}
	board += "$$$$$$$$$$ ";
	board += currentplayer;
	return board;
}

function get_move(move) {
	return [7 - Math.floor((move-11)/10), (move-11)%10];
}

/*
  Change the pieces in certain directions between target point and end point.
  The @current_piece is the current color the target point, or assumed color of it during idnetifying whether the point will a valid move.
  The @change is a boolean. True if it is a actual move, false if it is an assumed move.
*/
function change_inside(target_x, target_y, end_x, end_y, current_piece, change) {
	var i = Number(target_x);
	var j = Number(target_y);
	var listx = new Array();
	var listy = new Array();
	var num = Number(0);
	var found = Boolean(false);

	while (!found && (i != end_x || j != end_y)) {
		if (end_x - i != 0) {
			i = i + (end_x - i) / Math.abs(end_x - i);
		}
		if (end_y - j != 0) {
			j = j + (end_y - j) / Math.abs(end_y - j);
		}

		if (gameboard[i][j] == ".") {
			return false;
		} else if (gameboard[i][j] == current_piece) {
			found = true;
			break;
		}

		listx[num] = i;
		listy[num] = j;
		num++;
	}

	if (num == 0 || !found) {
		return false;
	} else if (change == true) {
		for (var n = 0; n < num; n++) {
			gameboard[listx[n]][listy[n]] = current_piece;
		}
	}
	return true;
}

/*
  Expand from the target point in 8 directions.
  The @current_piece is the current color the target point, or assumed color of it during idnetifying whether the point will a valid move.
  The @change is a boolean. True if it is a actual move, false if it is an assumed move.
*/
function expand(target_x, target_y, current_piece, change) {
	var enable = Boolean(false);
	var up = Number(Math.min(target_x, target_y));
	var down = Number(Math.min(7 - target_x, 7 - target_y));
	var left = Number(Math.min(target_x, 7 - target_y));
	var right = Number(Math.min(7 - target_x, target_y));

	if (change_inside(target_x, target_y, 0, target_y, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, 7, target_y, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, target_x, 0, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, target_x, 7, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, target_x - up, target_y - up, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, target_x - left, target_y + left, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, target_x + down, target_y + down, current_piece, change))
		enable = true;
	if (change_inside(target_x, target_y, target_x + right, target_y - right, current_piece, change))
		enable = true;

	if (enable == true) {
		return true;
	} else {
		return false;
	}

}

/*
  mark the valid possible moves on the xboard and oboard;
*/
function validateAndCount() {
	stones[0] = Number(0);
	stones[1] = Number(0);
	validmoves[0] = Number(0);
	validmoves[1] = Number(0);
	for (var i = 0; i < 8; i++) {
		for (var j = 0; j < 8; j++) {
			for (var k = 0; k < 2; k++) {
				validboard[k][i][j] = ".";
				if (gameboard[i][j] == ".") {
					if (expand(i, j, pieces[k], false)) {
						validboard[k][i][j] = pieces[k];
						validmoves[k]++;
					}
				} else if (gameboard[i][j] == pieces[k]) {
					stones[k]++;
				}
			}
		}
	}
}

function update(x, y) {
	gameboard[x][y] = currentplayer;
	//update the gameboard
	expand(x, y, currentplayer, true);
	// console.log((currentplayer == "x" ? 1 : 0) + " " + y + " " + (7-x) + " \r\n");
	record += (currentplayer == "x" ? 1 : 0) + " " + y + " " + (7-x) + " \r\n";

	//update the xboard, oboard, xmove and omove;
	validateAndCount();

	if (currentplayer == pieces[0]) {
		if (validmoves[1] != 0) {
			currentplayer = pieces[1];
		}
	} else if (currentplayer == pieces[1]) {
		if (validmoves[0] != 0) {
			currentplayer = pieces[0];
		}
	}

	display();
	handleEvent();

	checkWin();
}

function checkWin() {
	if (stones[0] == 0 || stones[1] == 0 || stones[0] + stones[1] == 64 || (validmoves[0] == 0 && validmoves[1] == 0)) {
		// TODO: add congratulations for the winner
		// Example:
		if (stones[0] > stones[1]) {
			setTimeout('alert("Black Wins!");',200);
		} else if (stones[0] < stones[1]) {
			setTimeout('alert("White Wins!");',200);
		} else {
			setTimeout('alert("Draw!");',200);
		}

		var d = new Date();
		dateStr = d.toISOString().substring(0,19).replace(/-|:/g, "");
		$('<a role="button" class="btn btn-success" id="downloadRecord" download="record_' + dateStr + '.txt" href="data:text/plain;charset=utf-8,' + encodeURIComponent(record) + '">Download Record</a>').insertAfter("#restart");
	}
}


$(document).ready(function() {

	user_is_black = true;

	gameboard = new Array(); // gameboard

	pieces = new Array("x", "o"); //pieces color: black="x" white="o" 黑子是叉，白子是圈
	currentplayer = pieces[0];
	stones = new Array(Number(0), Number(0)); //stone number for each player
	validmoves = new Array(Number(0), Number(0)); // possible moves for each player
	validboard = new Array(new Array(), new Array()); // the possible moves's board for each player

	elementName = new Array("black", "white");
	photoScource = new Array("./img/black.png", "./img/white.png", "./img/black2.png", "./img/white2.png");

	record = ""; // record string

	for (var i = 0; i < 8; i++) {
		gameboard[i] = new Array();
		validboard[0][i] = new Array();
		validboard[1][i] = new Array();

		for (var j = 0; j < 8; j++) {
			gameboard[i][j] = ".";
			validboard[0][i][j] = ".";
			validboard[1][i][j] = ".";
		}
	}

	oldboard = new Array();
	for (var i = 0; i < 8; i++) {
		oldboard[i] = new Array();
	}

	restart();
	$("#restart").attr('onclick', 'restart()');

});

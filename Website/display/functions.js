/*
  prepare the new board for the new game
*/
function restart()
{
  currentplayer = pieces[0];
  for (var i=0;i<8;i++){
    for (var j=0; j<8; j++){
      gameboard[i][j] = "_";
    }
  }

  update_old();

  gameboard[3][3] = pieces[1];
  gameboard[3][4] = pieces[0];
  gameboard[4][3] = pieces[0];
  gameboard[4][4] = pieces[1];

  validateAndCount();
  display();
  handleEvent();
}

/*
  let the oldboard updated with the gameboard
*/
function update_old()
{
  for (var i=0;i<8;i++){
    for (var j=0; j<8; j++){
      oldboard[i][j]=gameboard[i][j];
    }
  }
}

/*
  clean the old element
*/
function cleanboard()
{
  for (var i=0;i<8;i++)
  {
    for (var j=0; j<8; j++)
    {
      for (var k=0; k<2; k++)
      {
        var s = document.getElementById(elementName[k]+i+j);
        if (s!=null)
        {
          s.parentNode.removeChild(s);
        }
      }
    }
  }
}


/*
  display all the pieces and let the valid possible moves to be seen when hovered on
*/
function display()
{
  var up = 0;
  var left = 0;
  var board = document.getElementById("board");
  board.style.cssText = "top:"+up+"px;position:absolute;left:"+left+"px;";

  cleanboard();
  update_old();

  for (var i=0;i<8;i++)
  {
    for (var j=0; j<8; j++)
    {
      for (var k=0; k<2; k++)
      {
        if (gameboard[i][j] == pieces[k])
        {
          var xcoor = left+41+j*65;
          var ycoor = up+41+i*65;
          var container = document.createElement("div");
          container.id = elementName[k]+i+j;
          container.style.cssText = "width:65px;height:65px;top:"+ycoor+"px;position:absolute;left:"+xcoor+"px;";
          var img = document.createElement("img");
          img.src = photoScource[k];
          container.appendChild(img);
          document.body.appendChild(container);
        }

        // here we want to add the possible moves to be elements
        if (validboard[k][i][j] == currentplayer)
        {
          var xcoor = left+41+j*65;
          var ycoor = up+41+i*65;
          var container = document.createElement("div");
          container.id = elementName[k]+i+j;
          container.style.cssText = "width:65px;height:65px;top:"+ycoor+"px;position:absolute;left:"+xcoor+"px;";
          container.className = "hover"+k;
          var img = document.createElement("img");
          img.src = photoScource[k+2];
          container.appendChild(img);
          document.body.appendChild(container);
        }
      }
    }
  }
  // TODO: show the stones count for each player
  // Example:
  $("div#blackstones").text("black stones = " + stones[0]);
  $("div#whitestones").text("white stones = " + stones[1]);
}

function handleEvent()
{
  for (var k=0; k<2; k++)
  {
    $("div.hover"+k).children("img").hide();
    if (currentplayer == pieces[k])
    {
      $("div.hover"+k).mouseenter(function(){
          $(this).children("img").show();
      });
      $("div.hover"+k).mouseleave(function(){
          $(this).children("img").hide();
      });
      $("div.hover"+k).click(function(){
          var name = $(this).get(0).id;
          update(Number(name[5]),Number(name[6]));
      });
    }
  }
}

/*
  Change the pieces in certain directions between target point and end point.
  The @current_piece is the current color the target point, or assumed color of it during idnetifying whether the point will a valid move.
  The @change is a boolean. True if it is a actual move, false if it is an assumed move.
*/
function change_inside(target_x, target_y, end_x, end_y, current_piece, change)
{
  var i = Number(target_x);
  var j = Number(target_y);
  var listx = new Array(); var listy = new Array(); var num = Number(0);
  var found = Boolean(false);

  while (!found && (i != end_x || j != end_y))
  {
    if (end_x - i != 0)
    {
      i = i + (end_x - i)/Math.abs(end_x - i);
    }
    if (end_y - j != 0)
    {
      j = j + (end_y - j)/Math.abs(end_y - j);
    }

    if (gameboard[i][j] == "_")
    {
      return false;
    }
    else if (gameboard[i][j] == current_piece)
    {
      found = true;
      break;
    }

    listx[num] = i;
    listy[num] = j;
    num++;
  }

  if (num == 0 || !found)
  {
    return false;
  }
  else if (change == true)
  {
    for (var n=0; n<num; n++)
    {
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
function expand(target_x, target_y, current_piece, change)
{
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
  if (change_inside(target_x, target_y, target_x-up, target_y-up, current_piece, change))
    enable = true;
  if (change_inside(target_x, target_y, target_x-left, target_y+left, current_piece, change))
    enable = true;
  if (change_inside(target_x, target_y, target_x+down, target_y+down, current_piece, change))
    enable = true;
  if (change_inside(target_x, target_y, target_x+right, target_y-right, current_piece, change))
    enable = true;

  if (enable == true)
  {
    return true;
  }
  else
  {
    return false;
  }

}

/*
  mark the valid possible moves on the xboard and oboard;
*/
function validateAndCount()
{
  stones[0] = Number(0);
  stones[1] = Number(0);
  validmoves[0] = Number(0);
  validmoves[1] = Number(0);
  for ( var i = 0; i<8; i++)
  {
    for (var j = 0; j<8; j++)
    {
      for (var k = 0; k<2 ;k++)
      {
        validboard[k][i][j] = "_";
        if (gameboard[i][j] == "_")
        {
          if (expand(i, j, pieces[k], false))
          {
            validboard[k][i][j] = pieces[k];
            validmoves[k]++;
          }
        }
        else if (gameboard[i][j] == pieces[k])
        {
          stones[k]++;
        }
      }
    }
  }
}

function update(x, y)
{
  gameboard[x][y] = currentplayer;
  //update the gameboard
  expand(x, y, currentplayer, true)

  //update the xboard, oboard, xmove and omove;
  validateAndCount();

  if (currentplayer == pieces[0])
  {
    if (validmoves[1] != 0)
    {
      currentplayer = pieces[1];
    }
  }
  else if (currentplayer == pieces[1])
  {
    if (validmoves[0] != 0)
    {
      currentplayer = pieces[0];
    }
  }

  display();
  handleEvent();

  if(stones[0] == 0 || stones[1] == 0 || stones[0]+stones[1] == 64 || (validmoves[0]== 0 && validmoves[1] == 0))
  {
    // TODO: add congratulations for the winner
    // Example:
    if (stones[0] > stones[1])
    {
      alert("Black Wins!");
    }
    else if (stones[0] < stones[1])
    {
      alert("White Wins!");
    }
    else {
      alert("Draw!");
    }
  }
}

$(document).ready(function(){

//黑子是叉，白子是圈
gameboard = new Array();  // gameboard

pieces = new Array("x", "o"); //pieces color
currentplayer = pieces[0];
stones = new Array(Number(0), Number(0)); //stone number for each player
validmoves = new Array(Number(0), Number(0)); // possible moves for each player
validboard = new Array(new Array(), new Array()); // the possible moves's board for each player

elementName = new Array("black", "white");
photoScource = new Array("black.png", "white.png", "black2.png", "white2.png");

for (var i=0;i<8;i++)
{
  gameboard[i] = new Array();
  validboard[0][i] = new Array();
  validboard[1][i] = new Array();
  for (var j=0; j<8; j++)
  {
    gameboard[i][j] = "_";
    validboard[0][i][j] = "_";
    validboard[1][i][j] = "_";
  }
}


oldboard = new Array();
for (var i=0;i<8;i++)
{
  oldboard[i] = new Array();
}

restart();
$("button").attr('onclick','restart()');

});

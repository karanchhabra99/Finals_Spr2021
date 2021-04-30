# IS597DS - Finals_Spr2021
## Crazy Chess
Team Member:
- Karan Chhabra (karanc2)

Previous Work relating to this game was done in the below repository:
https://github.com/karanchhabra99/Chess.git

<h4> Assumptions</h4>
The various assumption which are being made are:
- No Castling
- No Check, checkmate or Stalemate. The game ends when either of the kings is captured.
- AI will always trun the pawn into Queen (during piece progression)

<BR>
<h4>Variation</h4>
Additional modification which are being done are:
- Knight could jump longer (3 steps ahead and then right or left instead of 2 steps ahead and then right or left).
- Bishop can jump accross his own teams pawns.
- Rook can crush his own teams pawns.


<h4>Targeted Algorithm Analysis</h4>


The heuristic function of the game is board_score. The time taken by that algorithm varies depending upon the size of the board, number of pawns, bishop, knight, rook, and king. Majority of the time taken by the heuristic function by calling np.where function to go through the whole board, and calculating the score based on number of pieces.
In term of the Big-O complexity, the function np.where seems to take the most time, but it is written in C, so I assume np.where goes through whole array once. And np.where is used check where is the piece on the board, so the time complexity of np.where for the board array is,

<b>Heigh of the board * Width of the board</b>

The heuristic function calls the np.where 11 times (5 times of white, 5 times for black, and 1 time to check if both the kings are alive) in most of the cases. So the time complexity of np.where in that case would be,

<b>11 * (Heigh of the board * Width of the board) </b>

Also, the program goes through each piece that is on the board to calculate the score, and so the Big-O calculation also varies based on number of pieces on the board. So, the total time complexity in terms of Big-O for the heuristic function is:

<b>Big-O(11*  (Heigh of the board * Width of the board) + Number of pieces left on the board)</b>

Removing the constant terms:

<b>Big-O((Heigh of the board * Width of the board) + Number of pieces left on the board)</b>

And the lower bound of the heuristic function (big-Theta) is when either of the kings is captured. In that case, the np.where function is called twice, so the time complexity, in that case, would be,

<b>Big-Theta(2 * (Heigh of the board * Width of the board))</b>

Removing the constant terms:

<b>Big-Theta(Heigh of the board * Width of the board)</b>


<h4>Reference:</h4>
- ChessMain.py creates GUI for the games of chess. And also provide some idea about  how the board should be set-up.\
ChessMain.py file and the images are taken taken from the below links (Only minor changes has been done to it): https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc
https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
<br><br>
- The ChessEngine.py copies the methods __init__ and makeMove from class GameState(), although both the methods have been modified significantly, there is a possibility there might some resemble to original code, which is taken from the below links: <br>1. https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc <br> 2. https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
<br><br>
- Minimax Algorithm
https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague

- Idea of board Heuristic functions is taken from:
https://github.com/devinalvaro/yachess


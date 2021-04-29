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

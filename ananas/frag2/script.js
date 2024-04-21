import { Chess } from "./chess.js";

async function run() {
  var engine = new Worker("denis-worker.js", { type: "module"});

  var board = null;
  var game = new Chess();

  function onDragStart(source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (game.isGameOver()) return false;

    // only pick up pieces for White
    if (piece.search(/^b/) !== -1) return false;
  }

  engine.onmessage = (move) => {
    game.move(move.data);
    board.position(game.fen())
  }

  function onDrop(source, target) {
    // see if the move is legal
    try {
      var move = game.move({
        from: source,
        to: target,
        promotion: "q", // NOTE: always promote to a queen for example simplicity
      });

      engine.postMessage(`${source}${target}`);
    } catch(e) {
      return "snapback"
    }
  }

  // update the board position after the piece snap
  // for castling, en passant, pawn promotion
  function onSnapEnd() {
    board.position(game.fen());
  }

  var config = {
    draggable: true,
    position: "start",
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
  };
  board = Chessboard("board1", config);
}

run();

import { Chess, PAWN } from "./chess.js";

const swears = ["Va te crosser.", "Maudit niaiseux !", "Mangeux de marde", "Câlice de chien sale", "Tu fais dur.", "M'a te dérencher la face.", "Grosse plotte sale", "T'es rien qu'une trace de brake.", "Gros colon"]

const insult = () => {
  document.getElementById("clippy-dialog").innerHTML = swears[Math.floor(Math.random()*swears.length)]
}

insult()

async function run() {
  var engine = new Worker("denis-worker.js", { type: "module"});

  var board = null;
  var game = new Chess();

  const loose = () => {
    document.getElementById("clippy").setAttribute("src", "./clippy-think.gif");
    document.getElementById("clippy-dialog").innerHTML = `
        <div id="clippy-loss">
          <p>Ţ̵̨͓̳͓̮͓̣̳͔͍͕̒̌̈́̍̍͑̇̌̌͘͝͝Ŗ̸͚̌͂Ọ̸̹̹͚̣̪̬̠͍̝̝͚̹̀̓͝ͅP̵̨̡̭̘͕̗̪̬̗̯̣̲̗̝̆͆̍̐̌͐̋̆̍ ̸̝͎͍̮̗͈̘̫̝̳̄͒N̸̢̡͙̜̭̳͓͙̒U̴̝̖̘͌̍͊̋̌̅̋̐̂́̇͊͑̄L̴̯̱̠͖̬̼̳͖̪͖͗̆̒̿́͜͝ ̶̢̛͎̟̱̲͔̖͉̥̓̌̒͑̚T̴̢͖̤̥̭͎͓̜̮̞͈̠̿̆́̄̏̈̍̓͆͘̕͝͠͝R̷̮͊̃͑ͅŐ̶͇̇̒͜P̵̨̟̹̮̎͋̋̀͋̂́̋̿̆ ̶̜͇͈͊̈́̑̐̎̾͑̋̀̈́̚̕͝͝N̸͙̈́̿̇̅͆̈́̎͒́͘̕͠Ų̶̪͓̫͉͍̦̞̦̠̼̠̝̑̎̒̐́̽̅͂́͜͠L̴̨̢͖̟̿̍͌͗̓̂͛͘ ̴̼̜̙̝̲̾̆̌͒̃̄̂̎̽͑̑́̚T̸̛͔̥͉̖̠̫̊̀̍̆̑͌̄́͑͠R̶̦̠̀͗̊̔̆̌̕͝Ơ̴̫̗̋̀̀̇̈́̎͆͝P̵̖͋̚͠ ̴̛͙͚͙̰̱̝̭̪̝̬͙̎̏̇͝N̶̨̧̛̟͉̫͛̋̓͑Ṵ̷̡̦̳̖̝̲͇̰͖̳̲͍̋̇̋̽́̿͠ͅL̵̻̣̀̊̔̓̓̽̈́̈͆̄͛̅̿̐͠</p>
          <section
            class="field-row"
            style="justify-content: flex-end"
            onclick="location.reload()"
          >
            <button>Réessayer</button>
          </section>
        </div>
    `
  }

  const win = (frag) => {
    document.getElementById("clippy").setAttribute("src", "./clippy-think.gif");
    document.getElementById("clippy-dialog").innerHTML = `
        <div id="clippy-win">
          <p>@!~&^&*^$&#</p>
          <p>Fragment: ${frag}</p>
          <section
            class="field-row"
            style="justify-content: flex-end"
            onclick="location.reload()"
          >
            <button>Suite</button>
          </section>
        </div>
    `
  }

  function onDragStart(source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (game.isGameOver()) {
      loose();
      return false;
    }

    // only pick up pieces for White
    if (piece.search(/^b/) !== -1) return false;
  }

  engine.onmessage = (move) => {
    if (move.data[0] == "f") {
      game = new Chess(move.data.slice(1))
      board.position(game.fen())
      return
    }

    let data = move.data.split(" ");

    if (data.length == 1) {
      game.move(data[0]);
    } else {
      if (data[0] === "white-win") {
        win(data[1]);
      } else {
        game.move(data[1]);
        loose()
      }
    }

    board.position(game.fen())
  }

  function onDrop(source, target) {
    // see if the move is legal
    let promotion = null;

    if (game.get(source).type == PAWN && (target[1] === "8" || target[1] === "1")) {
      promotion = "q";
    }

    try {
      game.move({
        from: source,
        to: target,
        promotion, // NOTE: always promote to a queen for example simplicity
      });

      insult()

      console.log(`${source}${target}${promotion ?? ""}`);

      engine.postMessage(`${source}${target}${promotion ?? ""}`);
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

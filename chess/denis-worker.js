import init, { Engine } from "./pkg/pablo.js";
await init();

// And afterwards we can use all the functionality defined in wasm.
let engine = Engine.new();

postMessage("v" + engine.pos())

onmessage = (move) => {
    postMessage(engine.play_move(move.data));
}
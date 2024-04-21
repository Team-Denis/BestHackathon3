mod com;
mod eval;
mod search;
mod transposition;

use crate::search::Search;
use chess::{Board, BoardStatus, ChessMove};
use std::str::FromStr;
use rand::seq::SliceRandom;
use wasm_bindgen::prelude::*;

const START_POS: [&str; 5] = ["rnbqkb1r/pp2pp1p/3p1np1/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6", "rnbqkb1r/pp3ppp/3p1n2/2pP4/8/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 6", "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4", "rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6", "r1bqkb1r/4nppp/p1np4/1p1Np3/4P3/N7/PPP2PPP/R1BQKB1R w KQkq - 2 9"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum GameState {
    Playing,
    WhiteWon,
    BlackWon,
    Draw,
}

#[wasm_bindgen]
pub struct Engine {
    board: Board,
    state: GameState,
}

#[wasm_bindgen]
impl Engine {
    #[wasm_bindgen]
    pub fn new() -> Engine {
        let mut rng = rand::thread_rng();

        Engine {
            board: Board::from_str(START_POS.choose(&mut rng).unwrap()).unwrap(),
            state: GameState::Playing,
        }
    }

    #[wasm_bindgen]
    pub fn pos(&self) -> String {
        self.board.to_string()
    }

    #[wasm_bindgen]
    pub fn play_move(&mut self, move_input: &str) -> String {
        if self.state == GameState::Playing {
            let mv = match ChessMove::from_str(&move_input.trim()) {
                Ok(mv) => match self.board.legal(mv) {
                    true => mv,
                    false => {
                        return "illegal".to_string();
                    }
                },
                Err(_) => {
                    println!("Invalid move!");
                    return "illegal".to_string();
                }
            };

            self.board = self.board.make_move_new(mv);

            match self.board.status() {
                BoardStatus::Checkmate => {
                    self.state = GameState::WhiteWon;
                    return format!("white-win {}", 0xCAFEBABE);
                }
                BoardStatus::Stalemate => {
                    self.state = GameState::Draw;
                    return "draw".to_string();
                }
                _ => (),
            }

            let mut search = Search::new();

            let reply = search
                .iterative_search(&self.board, 4)
                .expect("Search error!");

            self.board = self.board.make_move_new(reply);

            match self.board.status() {
                BoardStatus::Checkmate => {
                    self.state = GameState::BlackWon;
                    format!("black-win {reply}")
                }
                BoardStatus::Stalemate => {
                    self.state = GameState::Draw;
                    format!("draw {reply}")
                }
                _ => reply.to_string(),
            }
        } else {
            "not-playing".to_string()
        }
    }
}
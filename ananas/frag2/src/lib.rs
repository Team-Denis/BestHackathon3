mod com;
mod eval;
mod search;
mod transposition;

use crate::search::Search;
use chess::{Board, BoardStatus, ChessMove};
use std::{cell::RefCell, rc::Rc, str::FromStr};
use wasm_bindgen::prelude::*;

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
        Engine {
            board: Board::default(),
            state: GameState::Playing,
        }
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
                    return "white-win".to_string();
                }
                BoardStatus::Stalemate => {
                    self.state = GameState::Draw;
                    return "draw".to_string();
                }
                _ => (),
            }

            // let mut tt = TranspositionTable::new();
            // tt.set_size(0x4000000);
            let mut search = Search::new();

            let reply = search
                .iterative_search(&self.board, 5)
                .expect("Search error!");

            self.board = self.board.make_move_new(reply);

            match self.board.status() {
                BoardStatus::Checkmate => {
                    self.state = GameState::BlackWon;
                    return "black-win".to_string();
                }
                BoardStatus::Stalemate => {
                    self.state = GameState::Draw;
                    return "draw".to_string();
                }
                _ => return reply.to_string(),
            }
        } else {
            "not-playing".to_string()
        }
    }
}
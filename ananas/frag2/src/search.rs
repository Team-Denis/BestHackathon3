use std::time::{Duration, Instant};

use chess::{Board, MoveGen, ChessMove};
use crate::transposition::{TranspositionTable};
use crate::eval::eval;

// Setting max to 100 pawns should be enough
const INF: i32 = 10000;

pub struct Search {
    // tt: &'a mut TranspositionTable,
    // search_end: Option<Instant>,
}


impl Search {
    pub fn new() -> Self {
        Search { }
    }

    pub fn iterative_search(&mut self, board: &Board, depth: u8) -> Option<ChessMove> {
        // let mut main_move = self.search_root(board, 8, -INF, INF);
        // println!("Depth: {}, Best Move: {}", 1, main_move.expect(""));

        // for ply in 1..4 {
        //     main_move = self.search_root(board, ply, -INF, INF);
        //     println!("Depth: {}, Best Move: {}", ply, main_move.expect(""));
        // };

        self.search_root(board, depth, -INF, INF)
    }

    pub fn search_root(&mut self, board: &Board, depth: u8, alpha: i32, beta: i32) -> Option<ChessMove> {
        let mut max = -INF;
        let mut best_move = None;

        for candi in MoveGen::new_legal(board).into_iter() {
            let new_board = board.make_move_new(candi);
            let score = -self.alpha_beta(&new_board, depth-1, alpha, beta);

            dbg!(score);
            dbg!(max);

            if score >= max {
                best_move = Some(candi);
                max = score;
            }
        }

        //self.tt.insert(board, depth, Node::Exact(alpha));

        best_move
    }

    fn quiesce(&self, board: &Board, alpha: i32, beta: i32) -> i32 {
        // board.get_hash();
        let mut alpha = alpha;

        let stand_pat = eval(board);
        if stand_pat >= beta {
            return beta;
        }
        if alpha < stand_pat {
            return stand_pat
        }

        let mut moves = MoveGen::new_legal(board);
        let targets = board.color_combined(!board.side_to_move());
        moves.set_iterator_mask(*targets);

        for capture in moves.into_iter() {
            let new_board = board.make_move_new(capture);
            let score = -self.quiesce(&new_board, -beta, -alpha);

            if score >= beta {
                return beta;
            }
            if score > alpha {
                alpha = score;
            }
        }

        alpha
    }

    fn alpha_beta(&mut self, board: &Board, depth: u8, alpha: i32, beta: i32) -> i32 {
        let mut alpha = alpha;

        if depth == 0 {
            return self.quiesce(board, alpha, beta);
        }

        // if let Some(val) = self.tt.get(board, depth, alpha, beta) {
        //     if val > alpha && val < beta {
        //         return val
        //     }
        // }

        for mv in MoveGen::new_legal(board).into_iter() {
            let new_board = board.make_move_new(mv);
            let score = -self.alpha_beta(&new_board, depth-1, -beta, -alpha);

            if score >= beta {
                return beta;
            }
            if score > alpha {
                alpha = score;

            }
        }

        alpha
    }
}

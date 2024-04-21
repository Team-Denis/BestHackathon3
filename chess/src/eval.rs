use chess::{Board, BoardStatus, Color, MoveGen, Piece};

pub fn eval(board: &Board) -> i32 {
    let turn = match board.side_to_move() {
        Color::White => 1,
        Color::Black => -1,
    };

    match board.status() {
        BoardStatus::Checkmate => return -turn * 10000,
        BoardStatus::Stalemate => return 0,
        _ => (),
    }
    (material_score(board) + mobility_score(board)) * turn
}

fn piece_diff(board: &Board, piece: Piece) -> i32 {
    let white_pieces = board.color_combined(Color::White);
    let black_pieces = board.color_combined(Color::Black);
    let piece_squares = board.pieces(piece);

    (white_pieces & piece_squares).popcnt() as i32 - (black_pieces & piece_squares).popcnt() as i32
}

fn material_score(board: &Board) -> i32 {
    900 * piece_diff(board, Piece::Queen)
        + 500 * piece_diff(board, Piece::Rook)
        + 300 * (piece_diff(board, Piece::Knight) + piece_diff(board, Piece::Bishop))
        + 100 * piece_diff(board, Piece::Pawn)
}

fn mobility_score(board: &Board) -> i32 {
    let turn: i32 = match board.side_to_move() {
        Color::White => 1,
        Color::Black => -1,
    };

    let mobility = turn * MoveGen::new_legal(board).len() as i32;

    let opposite_board = match board.null_move() {
        Some(board) => board,
        None => return 0,
    };

    let opposite_mobility = -turn * MoveGen::new_legal(&opposite_board).len() as i32;

    10 * (mobility + opposite_mobility)
}

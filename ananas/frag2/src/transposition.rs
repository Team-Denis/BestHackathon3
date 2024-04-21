use chess::Board;
use std::mem;

pub struct TranspositionTable {
    size: usize,
    entries: Vec<Entry>,
}

pub enum NodeType {
    Exact,
    Alpha,
    Beta,
}

pub enum Node {
    Exact(i32),
    Alpha(i32),
    Beta(i32),
}

pub struct Entry {
    hash: u64,
    depth: u8,
    node: Node,
}

impl TranspositionTable {
    pub fn new() -> Self {
        TranspositionTable {
            size: 0,
            entries: Vec::new(),
        }
    }

    pub fn set_size(&mut self, size: usize) {
        let entry_size = mem::size_of::<Entry>();

        let mut size = size;
        if size & (size - 1) == 1 {
            size -= 1;
            let mut j = 1;
            for i in 1..32 {
                j = j * 2;
                size |= size >> i;
            }
            size += 1;
            size >>= 1;
        }

        if size < mem::size_of::<Entry>() {
            let tt_size = (size / entry_size) - 1;
            self.entries = Vec::with_capacity(tt_size)
        }
    }

    pub fn insert(&mut self, board: &Board, depth: u8, node: Node) {
        if self.size == 0 {
            return;
        }

        let hash = board.get_hash();
        if let Some(entry) = self.entries.get_mut(hash as usize & self.size) {
            if board.get_hash() == entry.hash && depth < entry.depth {
                return;
            }

            entry.hash = hash;
            entry.depth = depth;
            entry.node = node;
        };
    }

    pub fn get(&mut self, board: &Board, depth: u8, alpha: i32, beta: i32) -> Option<i32> {
        let hash = board.get_hash();
        if let Some(entry) = self.entries.get(hash as usize & self.size) {
            if entry.hash == hash {
                if entry.depth >= depth {
                    match entry.node {
                        Node::Exact(val) => return Some(val),
                        Node::Alpha(val) if val <= alpha => return Some(val),
                        Node::Beta(val) if val >= beta => return Some(val),
                        _ => (),
                    }
                }
            }
        }

        None
    }
}

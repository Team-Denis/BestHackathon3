use std::sync::{Arc, Mutex};
use std::io::{self, Write};

pub struct MockupState {
    ready: bool,
}

pub enum UciCommand {
    Uci,
    Go,
    Stop,
    Position(),
}

fn get_args(cmd: &str) {}

pub fn run() -> io::Result<()> {
    loop {
        let mut buffer = String::new();
        io::stdin().read_line(&mut buffer)?;
        let cmd = buffer.trim_end();
        let res = uci(cmd);
        println!("{res}");
    }
}

pub fn uci(command: &str) -> String {
    match command {
        "uci" => "uciok",
        "isready" => "readyok",
        _ => "",
    }.into()
}

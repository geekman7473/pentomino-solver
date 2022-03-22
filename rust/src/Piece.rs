use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::path::Path;
use std::collections::HashMap;
use std::fmt;


pub struct Config {
    rows: usize,
    cols: usize,
    arr: Vec<Vec<u32>>,
    arr_bool: Vec<Vec<bool>>
}
impl Config {
    pub fn new(_arr: Vec<Vec<u32>>, _rows: usize, _cols: usize) -> Config {
        let mut config = Config {
            rows : _rows,
            cols : _cols,
            arr : _arr,
            arr_bool : vec![vec![false; _rows]; _cols]
        };
        //TODO update arr_bool on creation

        config
    }
}

pub struct Piece {
    configs : Vec<Config>,
    id : u64
}

impl Piece {
    pub fn new(base: Config, _id: u64) -> Piece {
        let mut piece = Piece {
            configs : Vec::new(),
            id : _id
        };

        piece.configs.push(base);

        piece
    }
}

pub struct Bag {
    pieces: Vec<Piece>
}

impl Bag {
    pub fn new() -> Bag {
        Bag {
            pieces : Vec::new()
        }
    }

    pub fn load_pieces_from_file(&mut self, piece_file_path: &str) -> io::Result<()> {
        let file = File::open(piece_file_path)?;
        let reader = BufReader::new(file);

        let mut count = 0u8;
        let mut pieces_raw: HashMap<u8,Vec<String>> = HashMap::new();
        for result in reader.lines() {
            let line = result?;
            if line.eq("\n") || line.is_empty() {
                count += 1;
            } else {
                if !pieces_raw.contains_key(&count) {
                    pieces_raw.insert(count, Vec::new());
                }

                pieces_raw.get_mut(&count).unwrap().push(line.clone());
            }
        }

        for i in 0..count {
            let rows: usize = pieces_raw.get_mut(&i).unwrap().len();
            let cols: usize = pieces_raw.get_mut(&i).unwrap().iter().map(|v| v.chars().count()).max().unwrap();

            let mut piece = vec![vec![0u32; rows]; cols];

            for r in 0..rows {
                for c in 0..cols {
                    piece[r][c] = pieces_raw[&i][r].chars().nth(c).unwrap().to_digit(10).unwrap();
                }
            }

            &self.pieces.push(Piece::new(Config::new(piece, rows, cols), i.into()));
        }
            
        Ok(())
    }
}

impl fmt::Display for Bag {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        Ok(for piece in self.pieces.iter() {
            write!(f, "{}", piece);
            write!(f,"\n");
        })
    }
}

impl fmt::Display for Piece {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        Ok(for config in self.configs.iter() {
            write!(f, "{}", config);
            write!(f,"\n");
        })
    }
}

impl fmt::Display for Config {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f,"FOOBAR\n")
    }
}
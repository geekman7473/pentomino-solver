use std::fmt;
use piece::Piece;
use piece::Config;

pub struct Board {
    rows: usize,
    cols: usize,
    arr: Vec<Vec<u32>>,
    arr_bool: Vec<Vec<bool>>
}

impl Board {
    pub fn new(_rows: usize, _cols: usize) -> Board {
        Board {
            rows : _rows,
            cols : _cols,

            arr : vec![vec![0u32; _rows]; _cols],
            arr_bool : vec![vec![false; _rows]; _cols]
        }
    }

    pub fn is_valid(&self) -> bool {
        true
    }

    pub fn attempt_piece_placement(&self, piece: Piece) -> (bool, Option<Board>) {
        (true, None)
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        Ok(for row in self.arr.iter() {
            for elem in row.iter() {
                write!(f, "{}", elem);
            }
            write!(f,"\n");
        })
    }
}
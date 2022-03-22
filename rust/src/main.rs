mod piece;
mod board;

fn main() {
    // Statements here are executed when the compiled binary is called

    // Print text to the console
    println!("Hello World!");

    let board = board::Board::new(10, 6);
    print!("{}", board);

    let mut bag = piece::Bag::new();
    bag.load_pieces_from_file("..\\pieces.txt");
    print!("{}", bag);
}
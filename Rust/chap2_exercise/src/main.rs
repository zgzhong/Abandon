use std::io;

fn main() {

    // practice of convert between Fahrenheit and Celsius
    println!("Please input the Fahrenheit");

    let mut input_f = String::new();
    io::stdin().read_line(&mut input_f)
        .expect("Can not read line");
    
    let input_f: f64 = input_f.trim().parse()
        .expect("please type a number");

    let c = convert_f_to_c(input_f);
    println!("The Celsius of {}F° is {}C° ", input_f, c);

    println!("Please input the Celsius");
    
    let mut input_c = String::new();
    io::stdin().read_line(&mut input_c)
        .expect("Can not read line");
    let input_c: f64 = input_c.trim().parse()
        .expect("Please type a number");
    
    let f = convert_c_to_f(input_c);

    println!("The Fahrenheit of {}C° is {}F°", input_c, f);

    // pracitce of generate the nth Fibonacci number
    for idx in 1..10{
        println!("The {}st fibonacci number is {}", idx, compute_nth_fabonacci_number(idx));
    }
}

// convert Fahrenheit to Celsius.
fn convert_f_to_c (f:f64) -> f64 {
    5.0 / 9.0 * (f - 32.0)
}

// convert Celsius to Fahrenheit
fn convert_c_to_f (c:f64) -> f64 {
     9.0 / 5.0 * c + 32.0
}

// calculate the nth fabonacci number
fn compute_nth_fabonacci_number (n: u32) -> u64 {
    let mut a:u64 = 0;
    let mut b:u64 = 1;
    
    for _ in 1..n{
        let c = b;
        b = a + b;
        a = c;
    }
    b
}
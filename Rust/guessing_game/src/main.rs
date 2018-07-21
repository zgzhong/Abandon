extern crate rand;

use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    println!("Guessing the number");

    // 生成随机数
    let secret_number = rand::thread_rng().gen_range(1, 101);

    loop{
        println!("Please input your guess");

        // 创建一个String可变变量
        let mut guess = String::new();
        // 获取用户的输入
        io::stdin().read_line(&mut guess)
            .expect("Failed to read line");
        // 将字符串转为数字
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
        
        match guess.cmp(&secret_number){
            Ordering::Less => println!("Too Small"),
            Ordering::Greater => println!("Too Large"),
            Ordering::Equal => {
                println!("You win");
                break;
            }
        };
    }
}

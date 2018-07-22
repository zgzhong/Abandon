fn main(){
    let mut s1 = String::from("hello");
    let len = calculate_len(&s1);
    println!("The length of '{}' is {}.", s1, len);
    change(&mut s1);
    println!("{}", s1);

    // ---------------------------- //
    {
        let s_mut = &mut s1;
        s_mut.push_str(" Are you okay?");
        println!("{}", s_mut);
    }
    
    let hello = &mut s1[0..5];

    println!("{}", hello);


    let arr = [1,2,3,4,5,6,7,8,9,10];
    let slice = &arr[2..5];

}

fn calculate_len(s: &String) -> usize{
    s.len()
}


fn change(s: &mut String){
    s.push_str(", world!");
}
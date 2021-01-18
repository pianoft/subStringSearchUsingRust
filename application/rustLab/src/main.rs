fn say(words: &str) {
    std::process::Command::new("python3")
        .arg("saySMTH.py")
        .arg(words)
        .status()
        .expect("err@Bash commands");
}

fn say2(words: &str) {
    std::process::Command::new("spd-say") //spd-say -w -r 50 -i 100
        .arg("-w")
        .arg("-r")
        .arg("50")
        .arg("-i")
        .arg("100")
        .status()
        .expect("err@Bash commands");
}

fn main() {
    std::process::Command::new("rm")
        .arg("../../result.txt")
        .status()
        .expect("err@Bash commands");
    let args: Vec<String> = std::env::args().collect();
    let desired_string = &args[1].to_string();

    let file_name = String::from("../../listOfFiles.txt");

    let mut contents_of_text_file = std::fs::read_to_string(file_name).expect("err@Reading file");

    let mut sub_string = contents_of_text_file;

    let mut index_alpha = sub_string.find("\n").unwrap();

    let mut lineOfLines;

    let mut vec: Vec<String> = Vec::new();

    loop {
        index_alpha = sub_string.find("\n").unwrap();
        lineOfLines = sub_string[0..index_alpha].to_string();

        sub_string = sub_string[index_alpha + 1..].to_string();
        vec.push(lineOfLines);
        if sub_string.contains("\n") == false {
            break;
        }
    }

    use std::io::Write;
    let mut file_of_write = std::fs::File::create("../../result.txt").unwrap();

    let mut idx = 1;

    for mut title_of_text_file in vec {
        if idx % 100 == 0 {
            let asdf = idx.to_string();
            say(&asdf);
        }
        idx += 1;

        let mut file_name = String::from(title_of_text_file);

        let mut parental_directory: String = "../../rawTextsOfFiles/".to_owned();
        let file_name2: &str = &file_name;
        parental_directory.push_str(file_name2);

        let mut s3: String = file_name.to_owned();

        let line_break_icon: &str = &"\n";

        s3.push_str(line_break_icon);

        contents_of_text_file =
            std::fs::read_to_string(parental_directory).expect("err@Reading file");
        sub_string = contents_of_text_file;

        loop {
            index_alpha = sub_string.find("\n").unwrap();
            lineOfLines = sub_string[0..index_alpha].to_string();
            if lineOfLines.contains(desired_string) {
                file_of_write.write(s3.as_bytes()).unwrap();
            }

            sub_string = sub_string[index_alpha + 1..].to_string();

            if sub_string.contains("\n") == false {
                break;
            }
        }
    }
    std::process::exit(0);
}

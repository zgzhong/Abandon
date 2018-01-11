import argparse


class Tutorial(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        pass
    
    def no_option(self):
        """This snippet do noting, just output
        
        python xxx.py --help
        usage: turorial.py [-h]

        optional arguments:
          -h, --help  show this help message and exit
        """
        self.parser.parse_args()

    def positional_arg(self):
        """the echo fucntion"""
        self.parser.add_argument("echo", help="echo the string you enter here")
        args = self.parser.parse_args()
        print(args.echo)

    def specify_input_type(self):
        self.parser.add_argument("square", help="display the square of given number", type=int)
        args = self.parser.parse_args()
        print(args.square**2)

    def optional_arg(self):
        self.parser.add_argument(
                "--verbose", 
                help="increase output verbosity", 
                action="store_true"
            )
        args = self.parser.parse_args()
        if args.verbose:
            print("verbosity turn on")

    def short_option(self):
        self.parser.add_argument(
                "-v", "--verbose", 
                help="increase output verbosity", 
                action="store_true"
            )
        args = self.parser.parse_args()
        if args.verbose:
            print("verbosity turn on")

    def multi_verbosity_value(self):
        self.parser.add_argument("square", help="display the square of given number", type=int)
        self.parser.add_argument(
                "-v", "--verbose", 
                help="increase output verbosity", 
                type=int, choices={0, 1, 2}
            )
        args = self.parser.parse_args()
        answer = args.square**2

        if args.verbose == 2:
            print("The square of {} is {}".format(args.square, answer))
        elif args.verbose == 1:
            print("{}^2 == {}".format(args.square, answer))
        else:
            print(answer)

    def run(self):
        # self.positional_arg()
        # self.specify_input_type()
        # self.optional_arg()
        # self.short_option()
        self.multi_verbosity_value()


if __name__ == "__main__":
    Tutorial().run()

#include <iostream>		// std::cout
#include <ios>			// std::ios_base::failure
#include <fstream>		// std::ifstream
#include <sstream>		// std::ostringstream
#include <regex>		// std::regex
#include <string>		// std::string, std::stoi
#include <numeric>		// std::accumulate


class MemoryParser{

	public:

		std::string memory;

		bool conditionals = false;

		MemoryParser();
		MemoryParser(
			std::string memory,
			bool conditionals = false
		) :
			memory(memory),
			conditionals(conditionals) {
		}

		int scan(){

			std::sregex_iterator operands_start{
				memory.cbegin(),
				memory.cend(),
				pattern
			};
			std::sregex_iterator operands_end;		// Default constructs to end

			auto sum_operand_products = [this](
				const int& total,
				const std::smatch& operands
			){
				int increment = 0;
				switch(operands.length(1)){
					case 2:								// do
						this->accumulating = true;
						break;
					case 5:								// don't
						this->accumulating =
							this->conditionals
							? false
							: true
						;
						break;
					default:							// mul(X,Y)
						increment =
							this->accumulating
							? (std::stoi(operands[2]) * std::stoi(operands[3]))
							: 0
						;
				}
				return total + increment;
			};

			return std::accumulate(
				operands_start,
				operands_end,
				0,
				sum_operand_products
			);

		}

	private:

		bool accumulating = true;

		std::regex pattern{
			"(do|don't)\\(\\)"							// Sub-match 1
			"|mul\\(([0-9]{1,3}),([0-9]{1,3})\\)"		// Sub-matches 2,3
		};


};

int scan_memory(char* path, bool conditionals){

	std::ifstream file{path, std::ios::in};
	if(!file)
		throw std::ios_base::failure{"Error opening file"};
	std::ostringstream string_stream;
	string_stream << file.rdbuf();

	std::string memory{string_stream.str()};
	MemoryParser memory_parser{memory, conditionals};
	return memory_parser.scan();

}

int part_one(char* path){
	return scan_memory(path, false);
}

int part_two(char* path){
	return scan_memory(path, true);
}

int main(int argc, char* argv[]){
	std::cout << part_one(argv[1]) << std::endl;
	std::cout << part_two(argv[1]) << std::endl;
	return 0;
}

#include <iostream>		// std::cout
#include <ios>			// std::ios_base::failure
#include <fstream>		// std::ifstream
#include <string>		// std::string
#include <sstream>		// std::istringstream
#include <vector>		// std::vector
#include <cmath>		// std::abs
#include <numeric>		// std::adjacent_difference, std::accumulate

class Report{

	public:

		Report();
		Report(std::string& line){
			init_levels(line);
		}

		bool safe(bool problem_dampener){
			
			// Safe
			if( (increasing() || decreasing()) && gradual() )
				return true;

			// Unsafe && no problem damper — unsafe
			if(!problem_dampener)
				return false;

			// Unsafe && problem damper
			for(
				unsigned int bad_level_index = 0;
				bad_level_index < levels.size();
				bad_level_index++
			){
				int bad_level_value = levels.at(bad_level_index);
				levels.erase(levels.cbegin() + bad_level_index);
				if( (increasing() || decreasing()) && gradual() )
					return true;
				levels.insert(
					levels.cbegin() + bad_level_index,
					bad_level_value
				);
			}
			return false;

		}

	private:

		std::vector<int> levels;

		std::vector<int> differences;

		static bool gt0(const bool& a, const int& b){
			return a && (b > 0);
		}

		static bool lt0(const bool& a, const int& b){
			return a && (b < 0);
		}

		static bool abs_gt0_lte4(const bool& a, const int& b){
			return a && (std::abs(b) > 0) && (std::abs(b) < 4) ;
		}

		void init_levels(std::string& line){
			std::istringstream line_stream{line};
			for(int level; line_stream >> level;)
				levels.push_back(level);
		}

		void init_differences(){
			differences.resize(levels.size());
			std::adjacent_difference(
				levels.cbegin(),
				levels.cend(),
				differences.begin()
			);
			differences.erase(differences.cbegin());
		}

		bool increasing(){
			init_differences();
			return std::accumulate(
				differences.cbegin(),
				differences.cend(),
				true,
				Report::gt0
			);
		}

		bool decreasing(){
			init_differences();
			return std::accumulate(
				differences.cbegin(),
				differences.cend(),
				true,
				Report::lt0
			);
		}

		bool gradual(){
			init_differences();
			return std::accumulate(
				differences.cbegin(),
				differences.cend(),
				true,
				Report::abs_gt0_lte4
			);
		}

};

unsigned int count_safe_reports(
	char* path,
	bool problem_dampener
){

	// Open file
	std::ifstream file{path, std::ios::in};
	if(!file)
		throw std::ios_base::failure{"Error opening file"};

	// Process reports
	std::string line;
	unsigned int safe_reports = 0;
	while(file){
		std::getline(file, line, '\n');
		if(file.good()){
			Report report{line};
			safe_reports += (unsigned int)(report.safe(problem_dampener));
		}
		else{
			file.close();
			if(file.eof())
				break;
			else
				throw std::ios_base::failure{"Error reading line from file"};
		}
	}
	return safe_reports;
}

unsigned int part_one(char* path){
	bool problem_dampener = false;
	return count_safe_reports(path, problem_dampener);
}

unsigned int part_two(char* path){
	bool problem_dampener = true;
	return count_safe_reports(path, problem_dampener);
}

int main(int argc, char* argv[]){
	std::cout << part_one(argv[1]) << std::endl;
	std::cout << part_two(argv[1]) << std::endl;
	return 0;
}

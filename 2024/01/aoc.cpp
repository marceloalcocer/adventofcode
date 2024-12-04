#include <iostream>		// std::cout
#include <ios>			// std::ios_base::failure
#include <fstream>		// std::ifstream
#include <vector>		// std::vector
#include <algorithm>	// std::sort
#include <cmath>		// std::abs
#include <numeric>		// std::accumulate
#include <map>			// std::map

unsigned int abs_diff(const int& a, const int& b){
	return (unsigned int)(std::abs(a - b));
}

unsigned int part_one(char* path){

	// Read input
	std::ifstream file{path, std::ios::in};
	if(!file)
		throw std::ios_base::failure{"Error opening file"};
	std::vector<unsigned int> left, right;
	for(unsigned int i_left, i_right; file >> i_left >> i_right; ){
		left.push_back(i_left);
		right.push_back(i_right);
	}

	// Sort (in-place)
	std::sort(left.begin(), left.end());
	std::sort(right.begin(), right.end());

	// Compute absolute difference (in-place)
	std::transform(
		left.cbegin(), left.cend(),
		right.cbegin(),
		left.begin(),
		abs_diff
	);

	// Compute sum
	return std::accumulate(
		left.cbegin(),
		left.cend(),
		0
	);

}

unsigned int part_two(char* path){

	// Read input
	std::ifstream file{path, std::ios::in};
	if(!file)
		throw std::ios_base::failure{"Error opening file"};
	std::map<unsigned int, unsigned int> left, right;
	for(unsigned int i_left, i_right; file >> i_left >> i_right; ){

		// Frequency maps
		left[i_left] += 1;
		right[i_right] += 1;

	}

	// Compute cumulative product
	unsigned int sum = 0;
	for(const auto& it_left : left)
		sum += it_left.first * it_left.second * right[it_left.first];

	return sum;

}

int main(int argc, char* argv[]){
	std::cout << part_one(argv[1]) << std::endl;
	std::cout << part_two(argv[1]) << std::endl;
	return 0;
}

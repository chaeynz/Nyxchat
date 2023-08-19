#pragma once

#include <cstdint>
#include <map>

class Hexchar
{	
private:
	uint8_t hexadecimal_character;
	std::map<char, uint8_t> conversion_set;

public:
	Hexchar(uint8_t);

	static Hexchar convert_number(uint8_t);
	static Hexchar convert_number(uint16_t);
	static Hexchar convert_number(short);
	static Hexchar convert_number(int);
	static Hexchar convert_number(long);
	static Hexchar convert_number(long long);
	static Hexchar convert_number(unsigned short);
	static Hexchar convert_number(unsigned int);
	static Hexchar convert_number(unsigned long);
	static Hexchar convert_number(unsigned long long);

};


// User.hpp

#pragma once

#include <string>

class User {
private:
	char userId[128];
	std::string nodeAddress;

public:
	const char* getUserId() const;
	std::string getNodeAddress() const;
};
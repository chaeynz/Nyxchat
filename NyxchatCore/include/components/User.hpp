// User.hpp

#pragma once

#include <string>

class User {
private:
	char userId[128];

public:
	const char* getUserId() const;
};
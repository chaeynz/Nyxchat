// User.hpp

#pragma once

#include <string>

class User {
private:
	char userId[128];

public:
	unsigned long long getUserId();
};
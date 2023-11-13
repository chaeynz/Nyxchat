// User.cpp

#include <components/User.hpp>

const char* User::getUserId() const {
	return userId;
}

std::string User::getNodeAddress() const {
	return nodeAddress;
}
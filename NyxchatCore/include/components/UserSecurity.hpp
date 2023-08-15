// UserSecurity.hpp
#pragma once
#include <iostream>

#include <boost/date_time/posix_time/posix_time.hpp>

class UserSecurity
{
	unsigned long long int userID;
	std::string passwdHash;
	std::string passwdSalt;
	boost::posix_time::ptime time;
};
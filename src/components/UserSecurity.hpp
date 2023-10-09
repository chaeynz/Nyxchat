// UserSecurity.hpp
#pragma once
#include <iostream>

#include <boost/date_time/posix_time/posix_time.hpp>

class UserSecurity
{
	char userID[128];
	char userPrivateKey[6336]; //Kyber1024
	boost::posix_time::ptime time;
};
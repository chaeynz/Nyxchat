// Message.hpp
#pragma once

#include <string>
#include <boost/date_time/posix_time/posix_time.hpp>

#include "../components/User.hpp"

class Message 
{
private:
	unsigned long long messageId;
	boost::posix_time::ptime messageTimestamp;
	std::string messageContent;
	User* messageAuthor;

public:
	unsigned long long getMessageId();
	boost::posix_time::ptime getMessageTimestamp();
	std::string getMessageContent();
	User* getMessageAuthor();


	Message();
	~Message();
};
#pragma once

#include <string>
#include <chrono>

#include "../../lib/boost/date_time/posix_time/posix_time.hpp"

#include "User.hpp"

class Message 
{
	unsigned int messageId;

	User messageAuthor;
	std::string messageContent;
	boost::posix_time::ptime messageTimestamp;

	Message(std::string messageContent, User messageAuthor);
	~Message();

public:
	bool operator==(const Message& other) const;
};

extern unsigned int lastAssignedMessageId;


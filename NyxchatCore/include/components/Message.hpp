// Message.hpp
#pragma once

#include <string>
#include <memory>
#include <boost/date_time/posix_time/posix_time.hpp>

#include "../components/User.hpp"

class Message 
{
private:
	unsigned long long messageId;
	boost::posix_time::ptime messageTimestamp;
	std::string messageContent;
	std::shared_ptr<User> messageAuthor;

public:
	unsigned long long getMessageId();
	boost::posix_time::ptime getMessageTimestamp();
	std::string getMessageContent();
	std::shared_ptr<User> getMessageAuthor();


	Message(unsigned long long, std::string, std::string, std::string);
	~Message();
};
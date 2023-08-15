#include "Message.hpp"


Message::Message(std::string messageContent, User messageAuthor) 
{
	this->messageAuthor = messageAuthor;
	this->messageContent = messageContent;
	this->messageTimestamp = boost::posix_time::microsec_clock::universal_time();
	this->messageId = lastAssignedMessageId;
	++lastAssignedMessageId;
}

Message::~Message() 
{

}


unsigned int lastAssignedMessageId = 0;


bool Message::operator==(const Message& other) const
{
	if (this->messageContent == other.messageContent) {
		return true;
	}
	else {
		return false;
	}
}

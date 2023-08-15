// Message.cpp

#include "include/components/Message.hpp"

unsigned long long Message::getMessageId() {
	return messageId;
}

boost::posix_time::ptime Message::getMessageTimestamp() {
	return messageTimestamp;
}

std::string Message::getMessageContent() {
	return messageContent;
}

User* Message::getMessageAuthor() {
	return messageAuthor;
}

Message::Message() {

}
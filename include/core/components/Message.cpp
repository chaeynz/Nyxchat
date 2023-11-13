// Message.cpp

#include <components/Message.hpp>

unsigned long long Message::getMessageId() {
	return messageId;
}

boost::posix_time::ptime Message::getMessageTimestamp() {
	return messageTimestamp;
}

std::string Message::getMessageContent() {
	return messageContent;
}

std::shared_ptr<User> Message::getMessageAuthor() {
	return this->messageAuthor;
}

Message::Message(unsigned long long messageID, std::string messageAuthorID, std::string messageIsoExtendedTimestamp, std::string messageContent) {
	this->messageTimestamp = boost::posix_time::from_iso_extended_string(messageIsoExtendedTimestamp);
	this->messageAuthor = User(messageAuthorID);
}
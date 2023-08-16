// ChatEngine.cpp

#include "ChatEngine.hpp"

void ChatEngine::chatOutMessage(std::string message) {
	NetworkEngine::transmitMessage(message, "127.0.0.1");
}


void ChatEngine::chatOutMessage(Message* message, User* receiverUser) {
	NetworkEngine::transmitMessage(message->getMessageId(), boost::posix_time::to_iso_extended_string(message->getMessageTimestamp()), message->getMessageContent(), message->getMessageAuthor()->getUserId(), receiverUser->getUserId());
}
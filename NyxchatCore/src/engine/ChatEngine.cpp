// ChatEngine.cpp

#include "include/engine/ChatEngine.hpp"

void ChatEngine::chatOutMessage(Message* message, User* receiverUser) {
	NetworkEngine::transmitMessage(message->getMessageId, boost::posix_time::to_iso_extended_string(message->getMessageTimestamp()), message->getMessageContent(), message->getMessageAuthor()->getUserId())
}
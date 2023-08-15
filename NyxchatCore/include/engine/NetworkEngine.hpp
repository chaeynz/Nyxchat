#pragma once

#include <string>

class NetworkEngine
{
public:
	static void transmitMessage(unsigned long long messageId, std::string messageTimestamp, std::string messageContent, unsigned long long messageAuthorId, unsigned long long messageReceiverId);
	static void onMessageReceived();
};


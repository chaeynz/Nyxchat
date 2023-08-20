// NetworkEngine.hpp

#pragma once

#include <string>
#include <boost/asio.hpp>

#include "include/engine/ConnectionHandler.hpp"
#include "include/engine/Serializer.hpp"

class NetworkEngine
{
public:
	static void transmitMessage(std::string messageContent, std::string targetIP); // This is for testing purposes
	static void transmitMessage(unsigned long long messageId, std::string messageTimestamp, std::string messageContent, unsigned long long messageAuthorId, unsigned long long messageReceiverId);
	static void onNetworkIncomingDatastream(boost::asio::mutable_buffer);
	static void startListener();

	static bool checkFullNodeStatus(std::string);
	static bool checkFullNodeStatus(boost::asio::ip::address_v4);
};
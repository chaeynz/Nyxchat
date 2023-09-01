// NetworkEngine.hpp

#pragma once

#include <string>
#include <future>
#include <boost/asio.hpp>


#include "ConnectionHandler.hpp"
#include "DHTHandler.hpp"
#include "UserHandler.hpp"
#include "Serializer.hpp"


class NetworkEngine
{
public:
	static std::promise<User> userPromise;
	static std::future<User> userFuture;

	static void registerEventhandlers();

	static void transmitMessage(std::string messageContent, std::string targetIP); // This is for testing purposes
	static void transmitMessage(unsigned long long messageId, std::string messageTimestamp, std::string messageContent, unsigned long long messageAuthorId, unsigned long long messageReceiverId);
	static void onNetworkIncomingDatastream(boost::asio::mutable_buffer);
	static void startListener();

	static void requestUserFromFullNode(std::string);

	static bool checkFullNodeStatus(std::string);
	static bool checkFullNodeStatus(boost::asio::ip::address_v4);
};
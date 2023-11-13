// ErrorHandler.hpp

#pragma once

#include <engine/ConnectionHandler.hpp>

class ErrorHandler {
public:
	static void handleNetworkError();
	static void handleNoEventSubscriberFoundError();
	static void handleSocketForEndpointNotFoundError(boost::asio::ip::address_v4, uint16_t);
};
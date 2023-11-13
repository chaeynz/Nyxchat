// ErrorHandler.cpp

#include <engine/ErrorHandler.hpp>

void ErrorHandler::handleNetworkError() {

}

void ErrorHandler::handleNoEventSubscriberFoundError() {

}

void ErrorHandler::handleSocketForEndpointNotFoundError(boost::asio::ip::address_v4 ip, uint16_t port) {
	boost::asio::ip::tcp::endpoint();
	ConnectionHandler::addConnection(ip, port);
}
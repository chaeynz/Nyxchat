// ConnectionHandler.cpp

#include "include/engine/ConnectionHandler.hpp"

std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> ConnectionHandler::activeConnections;
boost::asio::io_context ConnectionHandler::ioContext;
boost::asio::ip::tcp::resolver ConnectionHandler::resolver(ConnectionHandler::ioContext);

std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> ConnectionHandler::getActiveConnections() {
	return activeConnections;
}

std::shared_ptr<boost::asio::ip::tcp::socket> ConnectionHandler::findSocket(const std::string& ip, uint16_t port) {
	boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::address::from_string(ip), port);
	auto it = activeConnections.find(endpoint);

	if (it != activeConnections.end()) {
		return it->second;
	}

	throw std::runtime_error("Socket for the given endpoint not found!");
}


void ConnectionHandler::addConnection(std::string& targetIP, uint16_t targetPort) {
	boost::asio::ip::tcp::resolver::results_type endpoints = resolver.resolve(targetIP, std::to_string(targetPort));

	try
	{
		std::shared_ptr<boost::asio::ip::tcp::socket> socket = std::make_shared<boost::asio::ip::tcp::socket>(ioContext);
		boost::asio::connect(*socket, endpoints);

		boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::address::from_string(targetIP), targetPort);
		activeConnections[endpoint] = std::move(socket);
	}
	catch (const boost::system::system_error& e)
	{
		ErrorHandler::handleNetworkError();
	}
}

void ConnectionHandler::addConnection(boost::asio::ip::tcp::endpoint targetEndpoint) {
	/*
	try
	{
		std::shared_ptr<boost::asio::ip::tcp::socket> socket = std::make_shared<boost::asio::ip::tcp::socket>(ioContext);

		boost::asio::connect(*socket, targetEndpoint);

		activeConnections[targetEndpoint] = std::move(socket);
	}
	catch (const boost::system::system_error& e)
	{
		ErrorHandler::handleNetworkError();
	}
	*/
}

void ConnectionHandler::sendData(boost::asio::ip::tcp::socket socket, boost::asio::const_buffer data) {
	boost::asio::write(socket, data);
}
void ConnectionHandler::sendData(std::shared_ptr<boost::asio::ip::tcp::socket> socket, boost::asio::const_buffer data) {
	boost::asio::write(*socket, data);
}

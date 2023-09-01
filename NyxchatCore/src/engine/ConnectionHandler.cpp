// ConnectionHandler.cpp

#include "include/engine/ConnectionHandler.hpp"

uint16_t ConnectionHandler::fullNodePort = 2468;

std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> ConnectionHandler::activeConnections;
boost::asio::io_context ConnectionHandler::ioContext;
boost::asio::ip::tcp::resolver ConnectionHandler::resolver(ConnectionHandler::ioContext);

inline std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> ConnectionHandler::getActiveConnections() {
	return activeConnections;
}

inline std::shared_ptr<boost::asio::ip::tcp::socket> ConnectionHandler::findSocket(const std::string& ip, uint16_t port) {
	boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::address::from_string(ip), port);
	auto it = activeConnections.find(endpoint);

	if (it != activeConnections.end()) {
		return it->second;
	}

	ErrorHandler::handleSocketForEndpointNotFoundError(boost::asio::ip::address_v4::from_string(ip), port);
}
inline std::shared_ptr<boost::asio::ip::tcp::socket> ConnectionHandler::findSocket(const boost::asio::ip::address_v4& ip, uint16_t port) {
	boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::address::from_string(ip), port);
	auto it = activeConnections.find(endpoint);

	if (it != activeConnections.end()) {
		return it->second;
	}

	ErrorHandler::handleSocketForEndpointNotFoundError(ip, port);
}


inline void ConnectionHandler::addConnection(std::string& targetIP, uint16_t targetPort) {
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

inline void ConnectionHandler::addConnection(boost::asio::ip::address_v4 targetIP, uint16_t targetPort) {

	boost::asio::ip::tcp::resolver::results_type endpoints = resolver.resolve(targetIP.to_string(), std::to_string(targetPort));
	try
	{
		std::shared_ptr<boost::asio::ip::tcp::socket> socket = std::make_shared<boost::asio::ip::tcp::socket>(ioContext);
		boost::asio::connect(*socket, endpoints);

		boost::asio::ip::tcp::endpoint endpoint(targetIP, targetPort);
		activeConnections[endpoint] = std::move(socket);
	}
	catch (const boost::system::system_error& e)
	{
		ErrorHandler::handleNetworkError();
	}
}

inline void ConnectionHandler::addConnection(boost::asio::ip::tcp::endpoint targetEndpoint) {
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



inline void ConnectionHandler::removeConnection(std::string& targetIP, uint16_t targetPort)
{
	boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::make_address(targetIP), targetPort);

	if (activeConnections.find(endpoint) != activeConnections.end()) {

		activeConnections[endpoint]->close();
		activeConnections.erase(endpoint);
	}
	else {
		// handle Error connection not found
	}
}

inline void ConnectionHandler::sendData(boost::asio::ip::tcp::socket socket, boost::asio::const_buffer data)
{
	boost::asio::write(socket, data);
}
inline void ConnectionHandler::sendData(std::shared_ptr<boost::asio::ip::tcp::socket> socket, boost::asio::const_buffer data) {
	boost::asio::write(*socket, data);
}


void ConnectionHandler::listenForData(uint16_t port, std::function<void(boost::asio::mutable_buffer)> callback)
{
	
	boost::asio::ip::tcp::acceptor acceptor(ConnectionHandler::ioContext, boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), port));
		for(;;)
	{
		acceptor.accept(activeListener);

		
	}


}

void ConnectionHandler::handleListenedData(boost::asio::ip::tcp::socket socket, std::function<void(boost::asio::mutable_buffer)> callback) {
	char data[4096];
	boost::asio::mutable_buffer buffer(data, sizeof(data));

	for (;;) {
		boost::system::error_code error;
		size_t length = activeListener.read_some(buffer, error);

		if (error == boost::asio::error::eof)
			break;  // Connection closed by the peer.
		else if (error)
			throw boost::system::system_error(error);  // Any other errors.

		// If data is received, execute the callback
		if (length > 0) {
			callback(buffer);
		}
	}

}
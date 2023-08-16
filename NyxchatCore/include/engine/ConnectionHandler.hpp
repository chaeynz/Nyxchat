// ConnectionHandler.hpp

#pragma once

#include <memory>
#include <map>

#include <boost/asio.hpp>

#include "include/engine/ErrorHandler.hpp"

struct EndpointComparator {
    bool operator()(const boost::asio::ip::tcp::endpoint& lhs, const boost::asio::ip::tcp::endpoint& rhs) const {
        if (lhs.address() != rhs.address()) {
            return lhs.address() < rhs.address();
        }
        return lhs.port() < rhs.port();
    }
};

class ConnectionHandler
{
public:
	static std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> activeConnections;
	static boost::asio::ip::tcp::socket activeListener;

	static boost::asio::io_context ioContext;
	static boost::asio::ip::tcp::resolver resolver;

    static std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> getActiveConnections();
    static std::shared_ptr<boost::asio::ip::tcp::socket> findSocket(const std::string& ip, uint16_t port);

	static void addConnection(std::string& targetIP, uint16_t targetPort);
    static void addConnection(boost::asio::ip::tcp::endpoint targetEndpoint);
    static void addConnection(boost::asio::ip::tcp::endpoint targetEndpoint, boost::asio::ip::tcp::socket targetSocket);
    static void removeConnection(std::string& targetIP, uint16_t targetPort);

    static void sendData(boost::asio::ip::tcp::socket socket, boost::asio::const_buffer data);
    static void sendData(std::shared_ptr<boost::asio::ip::tcp::socket> socket, boost::asio::const_buffer data);

};


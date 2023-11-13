// ConnectionHandler.hpp

#pragma once

#include <memory>
#include <map>
#include <functional>

#include <boost/asio.hpp>

#include <engine/ErrorHandler.hpp>
#include <engine/EventHandler.hpp>

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
    static uint16_t fullNodePort;

	static std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> activeConnections;
	static boost::asio::ip::tcp::socket activeListener;

	static boost::asio::io_context ioContext;
	static boost::asio::ip::tcp::resolver resolver;

    static std::map<boost::asio::ip::tcp::endpoint, std::shared_ptr<boost::asio::ip::tcp::socket>, EndpointComparator> getActiveConnections();
    static std::shared_ptr<boost::asio::ip::tcp::socket> findSocket(const std::string& ip, uint16_t port);
    static std::shared_ptr<boost::asio::ip::tcp::socket> findSocket(const boost::asio::ip::address_v4&, uint16_t port);

	static void addConnection(std::string&, uint16_t);
    static void addConnection(boost::asio::ip::address_v4, uint16_t);
    static void addConnection(boost::asio::ip::tcp::endpoint targetEndpoint);
    static void addConnection(boost::asio::ip::tcp::endpoint targetEndpoint, boost::asio::ip::tcp::socket targetSocket);
    static void removeConnection(std::string& targetIP, uint16_t targetPort);

    static void sendData(boost::asio::ip::tcp::socket socket, boost::asio::const_buffer data);
    static void sendData(std::shared_ptr<boost::asio::ip::tcp::socket> socket, boost::asio::const_buffer data);

    static void listenForData(uint16_t, std::function<void(boost::asio::mutable_buffer)>);
private:
    static void handleListenedData(boost::asio::ip::tcp::socket socket, std::function<void(boost::asio::mutable_buffer)> callback);


};


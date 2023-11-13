// DHTHandler.hpp

#pragma once

#include <map>
#include <string>
#include <random>
#include <boost/asio.hpp>

#include <engine/NetworkEngine.hpp>
#include <engine/ErrorHandler.hpp>

class DHTHandler
{
public:
	static std::map<std::string, boost::asio::ip::address_v4> clientNodeDHT;
	static std::map<std::string, boost::asio::ip::address_v4> fullNodeDHT;
	static boost::asio::ip::address_v4 backupNode;

	static boost::asio::ip::address_v4 findFullNode();
	static void storeInDHT(std::string, boost::asio::ip::address_v4);
	static void storeInDHT(std::string, std::string);
	static void storeInDHT(boost::asio::ip::address_v4);
	static void storeInDHT(std::string);
	static void registerNewNodeOnNetwork(boost::asio::ip::address_v4);
	static void registerNewNodeOnNetwork(std::string);

};


// DHTHandler.cpp

#include "include/engine/DHTHandler.hpp"

boost::asio::ip::address_v4 backupNode = boost::asio::ip::address_v4::from_string("127.0.0.1");

inline boost::asio::ip::address_v4 DHTHandler::findFullNode() {
	if (!fullNodeDHT.empty()) {
		std::random_device rd;
		std::mt19937_64 gen(rd());
		std::uniform_int_distribution<> dist(1, fullNodeDHT.size());
		short random = dist(gen);

		std::map<std::string, boost::asio::ip::address_v4>::const_iterator fullNodeDHTIterator = fullNodeDHT.begin();
		std::advance(fullNodeDHTIterator, random);

		return fullNodeDHTIterator->second;
	}
	else {
		return backupNode;
	}
}

inline void DHTHandler::storeInDHT(std::string hashToStore, boost::asio::ip::address_v4 ipToStore) {
	if (NetworkEngine::checkFullNodeStatus(ipToStore) == true) {
		fullNodeDHT.insert(std::make_pair(hashToStore, ipToStore));
	}
	else {
		clientNodeDHT.insert(std::make_pair(hashToStore, ipToStore));
	}
}

inline void DHTHandler::storeInDHT(std::string hashToStore, std::string ipToStore) {
	if (NetworkEngine::checkFullNodeStatus(ipToStore) == true) {
		fullNodeDHT.insert(std::make_pair(hashToStore, boost::asio::ip::address_v4::from_string(ipToStore)));
	}
	else {
		clientNodeDHT.insert(std::make_pair(hashToStore, boost::asio::ip::address_v4::from_string(ipToStore)));
	}
}
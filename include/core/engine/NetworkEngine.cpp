// NetworkEngine.cpp

#include <engine/NetworkEngine.hpp>

auto NetworkEngine::userFuture = userPromise.get_future();

void NetworkEngine::registerEventhandlers() {
	EventHandler::registerCallback(EventHandler::onUserNotFoundLocally, NetworkEngine::requestUserFromFullNode)
}


void NetworkEngine::transmitMessage(std::string messageContent, std::string targetIP) // THis overloaded function is for testing!
{
	if (ConnectionHandler::findSocket(targetIP, 4444) != 0) {
		ConnectionHandler::sendData(ConnectionHandler::findSocket(targetIP, 4444), Serializer::serializeMessageContent(messageContent));
	}
	else {
		ConnectionHandler::addConnection(targetIP, 4444);
		ConnectionHandler::sendData(ConnectionHandler::findSocket(targetIP, 4444), Serializer::serializeMessageContent(messageContent));
	}
}

void NetworkEngine::transmitMessage(unsigned long long messageId, std::string messageTimestamp, std::string messageContent, unsigned long long messageAuthorId, unsigned long long messageReceiverId)
{
	
}

void NetworkEngine::onNetworkIncomingDatastream(boost::asio::mutable_buffer data) {
	Serializer::deserializeNetworkStream(data);
}

void NetworkEngine::onNetworkIncomingResponseUser(std::string userID, std::string userName, std::string userID) {

}

void NetworkEngine::startListener() {
	ConnectionHandler::listenForData(2468, onNetworkIncomingDatastream);
}

void NetworkEngine::requestUserFromFullNode(std::string userID) {
	ConnectionHandler::sendData(ConnectionHandler::findSocket(DHTHandler::findFullNode(), ConnectionHandler::fullNodePort), Serializer::serializeRequestUser(userID));
	User user = userFuture.get();
	UserHandler::addUser(user);
}

bool NetworkEngine::checkFullNodeStatus(std::string) {

}
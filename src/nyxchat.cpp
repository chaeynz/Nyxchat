#include <iostream>

#include <node/engine/ChatEngine.hpp>
#include <node/engine/IOHandler.hpp>

#include <core/engine/EventHandler.hpp>

int main() {
	EventHandler::subscribe(EventHandler::onNetworkInputReceived, ChatEngine::on);
}
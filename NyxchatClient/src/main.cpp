#include <iostream>

#include "engine/ChatEngine.hpp"
#include "engine/IOHandler.hpp"

#include "include/engine/EventHandler.hpp"

int main() {
	EventHandler::subscribe(EventHandler::onNetworkInputReceived, ChatEngine::on);
}
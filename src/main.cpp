// main.cpp

#include <iostream>

#include "engine/IOEngine.hpp"

int main()
{
	std::string targetIP = "127.0.0.1";
	uint16_t targetPort = 4444;

	IOEngine ioEngine;;

	std::cout << "Options:\n";
	std::cout << "\t1. Send message\n";
	std::cout << "\t2 Listen for message\n";
	std::cout << "Choice: ";

	int userInputChoice;
	std::cin >> userInputChoice;
	std::string userInputMessage;

	switch (userInputChoice) {
	case 1:
		while (true) {
			std::cout << "\nType message: ";
			std::cin >> userInputMessage;
			ioEngine.sendMessage(userInputMessage, targetIP, targetPort);
		}
	case 2:
		while (true) {
			std::cout << "\nWaiting for message...\n";
			ioEngine.listenForMessages(targetPort);
		}
	}
}



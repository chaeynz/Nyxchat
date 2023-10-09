// ChatEngine.hpp


#include <core/engine/NetworkEngine.hpp>
#include <core/components/Message.hpp>
#include <core/components/User.hpp>

class ChatEngine {
	static void chatOutMessage(std::string message);
	static void chatOutMessage(Message* sendMessage, User* receiverUser);
	static void chatInMessage();
};
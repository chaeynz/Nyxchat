// ChatEngine.hpp

#include "include/engine/NetworkEngine.hpp"

#include "include/components/Message.hpp"
#include "include/components/User.hpp"

class ChatEngine {
	static void chatOutMessage(Message* sendMessage, User* receiverUser);
	static void chatInMessage();
};
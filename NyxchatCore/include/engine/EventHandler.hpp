#pragma once

#include <map>
#include <vector>
#include <functional>
#include <memory>

#include "include/engine/ErrorHandler.hpp"


class EventHandler {
public:
	using Event = std::function<void()>;
	using Callback = std::function<void()>;

	static std::map <Event, std::vector<Callback>> eventSubscribers;
	            //  <onNetworkInputRecv>,    notify  <correspondingReceiver>;

	static void registerCallback(const Event&, const Callback&);
	static void unregisterCallback(const Event&, const Callback&);
	static void notify(const Event&);

	static void onNetworkInputReceived();
	static void onUserNotFoundLocally();
	

	static std::shared_ptr<Event> onNetworkInputReceivedPtr;
};
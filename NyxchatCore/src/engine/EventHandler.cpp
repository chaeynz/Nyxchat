#include "include/engine/EventHandler.hpp"

inline void EventHandler::registerCallback(const Event& onEvent, const Callback& eventCallback) {
	

	if (eventSubscribers.find(onEvent) != eventSubscribers.end()) {
		auto& eventCallbacks = eventSubscribers[onEvent];
		if (std::find(eventCallbacks.begin(), eventCallbacks.end(), eventCallback) == eventCallbacks.end()) {
			eventCallbacks.push_back(eventCallback);
		}
		else {
			ErrorHandler::handleNoEventSubscriberFoundError();
		}
	}

	
}

inline void EventHandler::notify(const Event& onEvent) {
	std::shared_ptr<Event> p_onEvent= std::make_shared<Event>(onEvent);
	auto eventsIterator = eventSubscribers.find(p_onEvent);
	if (eventsIterator != eventSubscribers.end()) {
		for (const std::shared_ptr<Callback> p_callback : eventSubscribers[p_onEvent]) {
			(*p_callback)();
		}
	}
}

inline void EventHandler::onNetworkInputReceived() {
	notify(onNetworkInputReceived);
}

std::shared_ptr<Event> EventHandler::onNetworkInputReceivedPtr = std::make_shared<Event>(onNetworkInputReceived);
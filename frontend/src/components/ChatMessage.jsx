import VoiceListener from "./VoiceListener"

function ChatMessage({ message, isUser }) {
  return (
    <div className={`chat-message ${isUser ? "user-message" : "bot-message"}`}>
      <div className={`message-bubble ${isUser ? "user-bubble" : "bot-bubble"}`}>
        {isUser ? (
          <p className="mb-0">{message}</p>
        ) : (
          <div className="bot-response">
            <p className="mb-0">{message}</p>
            <VoiceListener text={message} isActive={!isUser} />
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatMessage

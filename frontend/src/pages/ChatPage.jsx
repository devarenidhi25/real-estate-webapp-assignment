"use client"

import React from "react"
import ChatInput from "../components/ChatInput"
import ChatMessage from "../components/ChatMessage"
import ResponseSummary from "../components/ResponseSummary"
import TrendChart from "../components/TrendChart"
import DataTable from "../components/DataTable"
import useChatQuery from "../hooks/useChatQuery"
import { useQueryContext } from "../context/QueryContext"
import "../styles/chatpage.css"

function ChatPage() {
  const { messages, currentResponse } = useQueryContext()
  const { sendQuery, isLoading } = useChatQuery()
  const messagesEndRef = React.useRef(null)

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="chat-page-container">
      {/* Header */}
      <header className="chat-header">
        <div className="header-content">
          <div className="header-title">
            <i className="bi bi-building me-3"></i>
            <div>
              <h1>Real Estate Analysis</h1>
              <p className="header-subtitle">Query and analyze real estate data</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <div className="chat-main-container">
        {/* Messages Area */}
        <div className="chat-messages-area">
          <div className="messages-container">
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg.text} isUser={msg.isUser} />
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Response Data Display */}
          {currentResponse && (
            <div className="response-data-section">
              <ResponseSummary summary={currentResponse.summary} />
              {currentResponse.chart && (
                <TrendChart data={currentResponse.chart.data} title={currentResponse.chart.title} />
              )}
              {currentResponse.table && <DataTable data={currentResponse.table} title="Detailed Analysis" />}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <ChatInput onSendQuery={sendQuery} isLoading={isLoading} />
        </div>
      </div>
    </div>
  )
}

export default ChatPage

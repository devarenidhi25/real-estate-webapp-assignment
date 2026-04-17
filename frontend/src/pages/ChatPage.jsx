import React from "react"
import ChatInput from "../components/ChatInput"
import ChatMessage from "../components/ChatMessage"
import ResponseSummary from "../components/ResponseSummary"
import TrendChart from "../components/TrendChart"
import DataTable from "../components/DataTable"
import TopGrowingAreas from "../components/TopGrowingAreas"
import useChatQuery from "../hooks/useChatQuery"
import { useQueryContext } from "../context/QueryContext"
import apiClient from "../api/apiClient"
import "../styles/chatpage.css"

function ChatPage() {
  const { messages, currentResponse, addMessage } = useQueryContext()
  const { sendQuery, isLoading } = useChatQuery()
  const messagesEndRef = React.useRef(null)
  const [initialized, setInitialized] = React.useState(false)
  const [topGrowingAreas, setTopGrowingAreas] = React.useState(null)
  const [loadingGrowth, setLoadingGrowth] = React.useState(false)

  // Show initial greeting when page loads
  React.useEffect(() => {
    if (!initialized && messages.length === 0) {
      const greeting = "Hi! I am your Real Estate Chatbot. How can I help you today? 🏠"
      addMessage(greeting, false)
      setInitialized(true)
    }
  }, [initialized, messages.length, addMessage])

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleShowTopGrowingAreas = async () => {
    setLoadingGrowth(true)
    try {
      const result = await apiClient.getTopGrowingAreas()
      setTopGrowingAreas(result)
      addMessage("Fetched the top 3 growing areas by price growth! 📈", false)
    } catch (error) {
      addMessage("Error fetching top growing areas. Please try again.", false)
      console.error(error)
    } finally {
      setLoadingGrowth(false)
    }
  }

  return (
    <div className="chat-page-container">
      {/* Header */}
      <header className="chat-header">
        <div className="header-content">
          <div className="header-title">
            <img src="/images/logo.png" alt="Logo" className="header-logo" />
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
          {currentResponse && currentResponse.action !== 'greeting' && currentResponse.action !== 'farewell' && (
            <div className="response-data-section">
              <ResponseSummary summary={currentResponse.summary} />
              {currentResponse.chart && (
                <TrendChart 
                  data={currentResponse.chart.data} 
                  title={currentResponse.chart.title}
                  datasets={currentResponse.chart.datasets}
                />
              )}
              {currentResponse.table && currentResponse.table.length > 0 && (
                <DataTable data={currentResponse.table} title="Detailed Analysis" />
              )}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <ChatInput onSendQuery={sendQuery} isLoading={isLoading} />
          <button 
            className="btn btn-info btn-sm ms-2"
            onClick={handleShowTopGrowingAreas}
            disabled={loadingGrowth || isLoading}
            title="Show top 3 growing areas by price growth"
          >
            {loadingGrowth ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Loading...
              </>
            ) : (
              <>
                <i className="bi bi-graph-up me-1"></i>
                Show Top Growing Areas
              </>
            )}
          </button>
        </div>

        {/* Top Growing Areas Display */}
        {topGrowingAreas && topGrowingAreas.top_areas && topGrowingAreas.top_areas.length > 0 && (
          <div className="response-data-section">
            <TopGrowingAreas areas={topGrowingAreas.top_areas} />
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatPage

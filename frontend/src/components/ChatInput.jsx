"use client"

import { useState } from "react"

function ChatInput({ onSendQuery, isLoading }) {
  const [inputValue, setInputValue] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim() && !isLoading) {
      onSendQuery(inputValue)
      setInputValue("")
    }
  }

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <div className="input-group input-group-lg">
        <input
          type="text"
          className="form-control chat-input"
          placeholder="Ask about real estate... e.g., 'Analyze Wakad' or 'Compare Ambegaon demand trends'"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={isLoading}
          autoFocus
        />
        <button className="btn btn-primary btn-send" type="submit" disabled={isLoading || !inputValue.trim()}>
          {isLoading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Analyzing...
            </>
          ) : (
            <>
              <i className="bi bi-send"></i> Send
            </>
          )}
        </button>
      </div>
    </form>
  )
}

export default ChatInput

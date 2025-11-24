"use client"

import { useState, useRef, useEffect } from "react"

function ChatInput({ onSendQuery, isLoading }) {
  const [inputValue, setInputValue] = useState("")
  const [isListening, setIsListening] = useState(false)
  const recognitionRef = useRef(null)

  // Initialize speech recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = "en-US"

      recognitionRef.current.onstart = () => {
        setIsListening(true)
      }

      recognitionRef.current.onresult = (event) => {
        let transcript = ""
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript
        }
        setInputValue(transcript)
      }

      recognitionRef.current.onerror = (event) => {
        console.error("Speech recognition error:", event.error)
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }
  }, [])

  const handleMicClick = () => {
    if (!recognitionRef.current) {
      alert("Speech recognition not supported in your browser")
      return
    }

    if (isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    } else {
      setInputValue("")
      recognitionRef.current.start()
    }
  }

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
        <button
          type="button"
          className={`btn btn-outline-secondary mic-button ${isListening ? 'listening' : ''}`}
          onClick={handleMicClick}
          disabled={isLoading}
          title={isListening ? "Stop listening" : "Start listening"}
        >
          <i className="fa-solid fa-microphone"></i>
        </button>
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

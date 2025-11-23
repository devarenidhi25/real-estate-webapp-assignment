import React, { createContext, useState, useCallback } from "react"

export const QueryContext = createContext()

export function QueryProvider({ children }) {
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      text: 'Welcome to Real Estate Analysis Chatbot! Ask me about any locality, compare areas, or analyze trends. Try queries like "Analyze Wakad" or "Compare demand in Aundh".',
      isUser: false,
    },
  ])
  const [currentResponse, setCurrentResponse] = useState(null)

  const addMessage = useCallback((text, isUser) => {
    const message = {
      id: Date.now(),
      text,
      isUser,
    }
    setMessages((prev) => [...prev, message])
    return message
  }, [])

  const clearCurrentResponse = useCallback(() => {
    setCurrentResponse(null)
  }, [])

  const setResponse = useCallback((response) => {
    setCurrentResponse(response)
  }, [])

  return (
    <QueryContext.Provider
      value={{
        messages,
        addMessage,
        currentResponse,
        setResponse,
        clearCurrentResponse,
      }}
    >
      {children}
    </QueryContext.Provider>
  )
}

export function useQueryContext() {
  return React.useContext(QueryContext)
}

export { QueryProvider as default }

import { useState, useCallback } from "react"
import { useQueryContext } from "../context/QueryContext"
import apiClient from "../api/apiClient"

function useChatQuery() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const { addMessage, setResponse } = useQueryContext()

  const sendQuery = useCallback(
    async (queryText) => {
      setIsLoading(true)
      setError(null)

      // Add user message to chat
      addMessage(queryText, true)

      try {
        // Call real API
        const response = await apiClient.query(queryText)

        // Check for API errors
        if (response.error) {
          throw new Error(response.error)
        }

        // Transform backend response to frontend format
        const transformedResponse = {
          summary: response.summary || "Analysis complete.",
          action: response.action || "unknown",
          areas: response.areas || [],
          chart: response.chart || { labels: [], datasets: [] },
          table: response.table || [],
          summaryData: response.summaryData || {},
        }

        setResponse(transformedResponse)
        addMessage(transformedResponse.summary, false)
      } catch (err) {
        const errorMessage = err.message || "Sorry, there was an error processing your query. Please try again."
        setError(err.message)
        addMessage(errorMessage, false)
        console.error("Query Error:", err)
      } finally {
        setIsLoading(false)
      }
    },
    [addMessage, setResponse],
  )

  return {
    sendQuery,
    isLoading,
    error,
  }
}

export default useChatQuery

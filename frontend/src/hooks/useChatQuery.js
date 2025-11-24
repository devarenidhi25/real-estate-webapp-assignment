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

      // Check for greeting/farewell messages
      const lowerQuery = queryText.toLowerCase().trim()
      
      // Greetings
      if (['hi', 'hello', 'hey', 'okay', 'ok'].includes(lowerQuery)) {
        const greetingResponse = "Please put your query. I can help you with:\n• Price growth analysis\n• Area comparisons\n• Demand trends\n\nExample: 'Compare Aundh Wakad Ambegaon' or 'Show price growth in Wakad'"
        addMessage(greetingResponse, false)
        setResponse({ summary: greetingResponse, action: "greeting", areas: [], chart: { data: [], datasets: [] }, table: [] })
        setIsLoading(false)
        return
      }
      
      // Farewells
      if (['bye', 'goodbye', 'thanks', 'thank you', 'exit', 'quit'].includes(lowerQuery)) {
        const farewellResponse = "Thank you for using Real Estate Analysis Chatbot! Feel free to reach out anytime you need real estate insights. Goodbye!"
        addMessage(farewellResponse, false)
        setResponse({ summary: farewellResponse, action: "farewell", areas: [], chart: { data: [], datasets: [] }, table: [] })
        setIsLoading(false)
        return
      }

      try {
        // Call real API
        const response = await apiClient.query(queryText)

        // Check for API errors
        if (response.error) {
          throw new Error(response.error)
        }

        // Transform backend response to frontend format
        const chartData = transformChartData(response.chart || { labels: [], datasets: [] })
        
        const transformedResponse = {
          summary: response.summary || "Analysis complete.",
          action: response.action || "unknown",
          areas: response.areas || [],
          chart: chartData,
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

// Transform backend chart format {labels, datasets} to frontend format
// Handles both single and multi-dataset charts
function transformChartData(backendChart) {
  const { labels = [], datasets = [] } = backendChart

  if (!labels || labels.length === 0 || !datasets || datasets.length === 0) {
    return {
      data: [],
      title: "Chart",
      datasets: []
    }
  }

  // For multi-dataset comparisons, return datasets structure
  if (datasets.length > 1) {
    return {
      data: [],
      title: "Area Comparison",
      datasets: datasets.map(dataset => ({
        label: dataset.label || "Data",
        data: labels.map((label, index) => ({
          label: label.toString(),
          value: parseFloat(dataset.data[index]) || 0
        }))
      }))
    }
  }

  // For single dataset, return simple format
  const firstDataset = datasets[0] || {}
  const title = firstDataset.label || "Price Trend"
  const values = firstDataset.data || []

  // Transform to TrendChart format: [{label, value}, {label, value}]
  const transformedData = labels.map((label, index) => ({
    label: label.toString(),
    value: parseFloat(values[index]) || 0
  }))

  return {
    data: transformedData,
    title: title
  }
}

export default useChatQuery

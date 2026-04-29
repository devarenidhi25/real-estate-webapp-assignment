class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error("API Error:", error)
      throw error
    }
  }

  async query(queryText) {
    return this.request("/api/query/", {
      method: "POST",
      body: JSON.stringify({ message: queryText }),
    })
  }

  async getTopGrowingAreas() {
    return this.request("/api/top-growth/", {
      method: "GET",
    })
  }
}

export default new APIClient()

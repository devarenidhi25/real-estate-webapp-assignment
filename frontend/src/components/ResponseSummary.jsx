function ResponseSummary({ summary }) {
  if (!summary) return null

  return (
    <div className="response-summary">
      <div className="summary-card">
        <h5 className="summary-title">
          <i className="bi bi-chat-left-quote me-2"></i>Analysis Summary
        </h5>
        <p className="summary-text">{summary}</p>
      </div>
    </div>
  )
}

export default ResponseSummary

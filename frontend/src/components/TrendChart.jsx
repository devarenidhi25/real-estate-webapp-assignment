import React from "react"

function TrendChart({ data, title, datasets }) {
  const canvasRef = React.useRef(null)

  // Colors for different area lines
  const colors = ["#0d6efd", "#198754", "#dc3545", "#fd7e14", "#6f42c1"]

  React.useEffect(() => {
    if (!canvasRef.current) return

    // Check if we have multi-dataset data (comparison mode)
    if (datasets && datasets.length > 1) {
      drawMultiDatasetChart()
    } else if (data && data.length > 0) {
      drawSingleDatasetChart()
    }

    function drawSingleDatasetChart() {
      const canvas = canvasRef.current
      const ctx = canvas.getContext("2d")
      const width = canvas.width
      const height = canvas.height
      const padding = 40

      // Clear canvas
      ctx.fillStyle = "#f8f9fa"
      ctx.fillRect(0, 0, width, height)

      // Draw axes
      ctx.strokeStyle = "#dee2e6"
      ctx.lineWidth = 2
      ctx.beginPath()
      ctx.moveTo(padding, height - padding)
      ctx.lineTo(width - padding, height - padding)
      ctx.moveTo(padding, height - padding)
      ctx.lineTo(padding, padding)
      ctx.stroke()

      // Find max value for scaling
      const values = data.map((d) => d.value)
      const maxValue = Math.max(...values)
      const barWidth = (width - padding * 2) / data.length

      // Draw bars
      data.forEach((d, index) => {
        const barHeight = (d.value / maxValue) * (height - padding * 2)
        const x = padding + index * barWidth + barWidth / 4
        const y = height - padding - barHeight

        ctx.fillStyle = "#0d6efd"
        ctx.fillRect(x, y, barWidth / 2, barHeight)

        // Label
        ctx.fillStyle = "#495057"
        ctx.font = "12px sans-serif"
        ctx.textAlign = "center"
        ctx.fillText(d.label, x + barWidth / 4, height - padding + 20)
      })

      // Title
      ctx.fillStyle = "#212529"
      ctx.font = "bold 14px sans-serif"
      ctx.textAlign = "center"
      ctx.fillText(title, width / 2, 25)
    }

    function drawMultiDatasetChart() {
      const canvas = canvasRef.current
      const ctx = canvas.getContext("2d")
      const width = canvas.width
      const height = canvas.height
      const padding = 50

      // Clear canvas
      ctx.fillStyle = "#f8f9fa"
      ctx.fillRect(0, 0, width, height)

      // Get all labels from first dataset
      const labels = datasets[0]?.data?.map((d) => d.label) || []
      if (labels.length === 0) return

      // Find max value for scaling
      let maxValue = 0
      datasets.forEach((dataset) => {
        dataset.data.forEach((d) => {
          maxValue = Math.max(maxValue, d.value || 0)
        })
      })
      if (maxValue === 0) maxValue = 100

      // Draw axes
      ctx.strokeStyle = "#dee2e6"
      ctx.lineWidth = 2
      ctx.beginPath()
      ctx.moveTo(padding, height - padding)
      ctx.lineTo(width - padding, height - padding)
      ctx.moveTo(padding, height - padding)
      ctx.lineTo(padding, padding)
      ctx.stroke()

      // Calculate bar dimensions
      const groupWidth = (width - padding * 2) / labels.length
      const barWidth = groupWidth / (datasets.length + 1)

      // Draw bars for each dataset
      datasets.forEach((dataset, datasetIndex) => {
        dataset.data.forEach((d, index) => {
          const barHeight = (d.value / maxValue) * (height - padding * 2)
          const x = padding + index * groupWidth + (datasetIndex + 1) * barWidth
          const y = height - padding - barHeight

          ctx.fillStyle = colors[datasetIndex % colors.length]
          ctx.fillRect(x, y, barWidth, barHeight)
        })
      })

      // Draw x-axis labels
      ctx.fillStyle = "#495057"
      ctx.font = "12px sans-serif"
      ctx.textAlign = "center"
      labels.forEach((label, index) => {
        const x = padding + index * groupWidth + groupWidth / 2
        ctx.fillText(label, x, height - padding + 20)
      })

      // Draw legend
      ctx.font = "12px sans-serif"
      ctx.textAlign = "left"
      datasets.forEach((dataset, index) => {
        const legendX = width - 200
        const legendY = 40 + index * 20
        ctx.fillStyle = colors[index % colors.length]
        ctx.fillRect(legendX, legendY, 12, 12)
        ctx.fillStyle = "#212529"
        ctx.fillText(dataset.label, legendX + 18, legendY + 11)
      })

      // Title
      ctx.fillStyle = "#212529"
      ctx.font = "bold 14px sans-serif"
      ctx.textAlign = "center"
      ctx.fillText(title, width / 2, 25)
    }
  }, [data, title, datasets])

  if ((!data || data.length === 0) && (!datasets || datasets.length === 0)) {
    return null
  }

  return (
    <div className="trend-chart-container">
      <canvas ref={canvasRef} width={800} height={400} className="trend-chart"></canvas>
    </div>
  )
}

export default TrendChart

import React from "react"

function TrendChart({ data, title }) {
  const canvasRef = React.useRef(null)

  React.useEffect(() => {
    if (!canvasRef.current || !data || data.length === 0) return

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
  }, [data, title])

  if (!data || data.length === 0) return null

  return (
    <div className="trend-chart-container">
      <canvas ref={canvasRef} width={600} height={300} className="trend-chart"></canvas>
    </div>
  )
}

export default TrendChart

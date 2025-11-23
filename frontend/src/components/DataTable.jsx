"use client"

import { useState, useMemo } from "react"

function DataTable({ data, title }) {
  const [sortConfig, setSortConfig] = useState(null)

  const columns = useMemo(() => (data.length > 0 ? Object.keys(data[0]) : []), [data])

  const sortedData = useMemo(() => {
    const sortableData = [...data]
    if (sortConfig) {
      sortableData.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? -1 : 1
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? 1 : -1
        }
        return 0
      })
    }
    return sortableData
  }, [data, sortConfig])

  const handleSort = (key) => {
    let direction = "asc"
    if (sortConfig && sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc"
    }
    setSortConfig({ key, direction })
  }

  if (!data || data.length === 0) return null

  return (
    <div className="data-table-container">
      <h5 className="table-title">
        <i className="bi bi-table me-2"></i>
        {title}
      </h5>
      <div className="table-responsive">
        <table className="table table-hover data-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col} onClick={() => handleSort(col)} style={{ cursor: "pointer" }} className="table-header">
                  {col}
                  {sortConfig?.key === col && (
                    <i className={`bi bi-arrow-${sortConfig.direction === "asc" ? "up" : "down"} ms-1`}></i>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedData.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={`${idx}-${col}`}>{row[col]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default DataTable

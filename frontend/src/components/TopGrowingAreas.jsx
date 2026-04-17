import React from "react"

// S3 Image mapping for areas
const AREA_IMAGE_MAP = {
  "Aundh": "https://real-estate-fa1-bucket.s3.eu-north-1.amazonaws.com/aundh.jpg",
  "Wakad": "https://real-estate-fa1-bucket.s3.eu-north-1.amazonaws.com/Wakad.jpg",
  "Kharadi": "https://real-estate-fa1-bucket.s3.eu-north-1.amazonaws.com/kharadi.jpg",
  "Magarpatta": "https://real-estate-fa1-bucket.s3.eu-north-1.amazonaws.com/magarpatta.jpg",
  "Ambegaon": "https://real-estate-fa1-bucket.s3.eu-north-1.amazonaws.com/ambegaon.jpg",
  "Akurdi": "https://real-estate-fa1-bucket.s3.eu-north-1.amazonaws.com/akurdi.jpg",
}

function TopGrowingAreas({ areas }) {
  if (!areas || areas.length === 0) return null

  return (
    <div className="top-growing-areas">
      <div className="growth-card">
        <h5 className="growth-title">
          <i className="bi bi-graph-up-arrow me-2"></i>Top Growing Areas
        </h5>
        <div className="areas-grid">
          {areas.map((item, index) => (
            <div key={index} className="area-item">
              <div className="area-rank">#{index + 1}</div>
              <img
                src={AREA_IMAGE_MAP[item.area] || AREA_IMAGE_MAP["Aundh"]}
                alt={item.area}
                className="area-image"
              />
              <div className="area-info">
                <h6 className="area-name">{item.area}</h6>
                <div className="growth-stats">
                  <p className="growth-percent">
                    <strong>Growth:</strong> <span className="growth-value">{item.growth}%</span>
                  </p>
                  <p className="price-range">
                    <strong>Range:</strong> ₹{item.min_price?.toLocaleString()} - ₹{item.max_price?.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default TopGrowingAreas

import { useState, useRef, useEffect } from "react"

function VoiceListener({ text, isActive }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [isSpeechSupported, setIsSpeechSupported] = useState(false)
  const utteranceRef = useRef(null)

  useEffect(() => {
    // Check if speech synthesis is supported
    const speechSynthesis = window.speechSynthesis
    setIsSpeechSupported(!!speechSynthesis)
  }, [])

  const handleSpeak = () => {
    if (!text || !isSpeechSupported) return

    const speechSynthesis = window.speechSynthesis

    if (isPlaying) {
      speechSynthesis.cancel()
      setIsPlaying(false)
      return
    }

    // Cancel any ongoing speech
    speechSynthesis.cancel()

    // Create utterance
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 1
    utterance.pitch = 1
    utterance.volume = 1

    utterance.onstart = () => {
      setIsPlaying(true)
    }

    utterance.onend = () => {
      setIsPlaying(false)
    }

    utterance.onerror = () => {
      setIsPlaying(false)
    }

    utteranceRef.current = utterance
    speechSynthesis.speak(utterance)
  }

  if (!text || !isSpeechSupported || !isActive) {
    return null
  }

  return (
    <button
      type="button"
      className={`btn btn-outline-info voice-button ${isPlaying ? 'playing' : ''}`}
      onClick={handleSpeak}
      title={isPlaying ? "Stop speaking" : "Listen"}
    >
      <i className="fa-solid fa-volume-high"></i>
    </button>
  )
}

export default VoiceListener

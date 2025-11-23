import ChatPage from "./pages/ChatPage"
import { QueryProvider } from "./context/QueryContext"
import "./styles/global.css"
import "./styles/chatpage.css"

function App() {
  return (
    <QueryProvider>
      <ChatPage />
    </QueryProvider>
  )
}

export default App

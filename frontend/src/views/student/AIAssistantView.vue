<template>
  <div class="assistant-page py-8 bg-slate-50 min-h-screen">
    <div class="container max-w-4xl">
      <!-- Assistant Card -->
      <div class="chat-card card shadow-lg flex flex-col h-[75vh]">
        <!-- Chat Header -->
        <div class="chat-header p-4 border-b border-slate-200 flex items-center justify-between bg-white rounded-t-2xl">
          <div class="flex items-center gap-3">
            <div class="ai-avatar">✨</div>
            <div>
              <h2 class="text-base font-bold text-slate-900">AI Career & Resume Coach</h2>
              <span class="text-xs text-emerald-600 font-medium flex items-center gap-1">
                <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
                Grounded in your actual resume and skill profile
              </span>
            </div>
          </div>
          <button class="btn btn-secondary btn-sm text-xs" @click="clearChat">
            Clear Chat
          </button>
        </div>

        <!-- Chat Messages Scroll Area -->
        <div ref="messagesContainer" class="chat-messages p-6 flex-1 overflow-y-auto flex flex-col gap-4 bg-slate-50/50">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message-wrapper flex"
            :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'"
          >
            <!-- AI Avatar -->
            <div v-if="msg.sender === 'ai'" class="ai-avatar-sm mr-2 flex-shrink-0">
              ✨
            </div>

            <!-- Message Bubble -->
            <div
              class="message-bubble max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed"
              :class="msg.sender === 'user' ? 'bg-indigo-600 text-white rounded-br-none' : 'bg-white text-slate-800 border border-slate-200 shadow-sm rounded-bl-none'"
            >
              <div class="bubble-content whitespace-pre-line" v-html="formatMessage(msg.text)"></div>
              <span class="text-[10px] opacity-70 block mt-1 text-right">{{ msg.time }}</span>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="typing" class="flex items-center gap-2 text-slate-500 text-xs pl-8">
            <span class="animate-bounce">●</span>
            <span class="animate-bounce" style="animation-delay: 0.2s">●</span>
            <span class="animate-bounce" style="animation-delay: 0.4s">●</span>
            <span>AI Coach is analyzing...</span>
          </div>
        </div>

        <!-- Quick Prompts Row -->
        <div class="quick-prompts-row p-3 bg-white border-t border-slate-100 flex flex-wrap gap-2">
          <span class="text-xs font-bold text-slate-500 self-center mr-1">Suggested:</span>
          <button
            v-for="prompt in suggestedPrompts"
            :key="prompt"
            class="prompt-pill"
            @click="sendPrompt(prompt)"
          >
            {{ prompt }}
          </button>
        </div>

        <!-- Input Area -->
        <div class="chat-input-row p-4 bg-white border-t border-slate-200 rounded-b-2xl">
          <form class="flex gap-2" @submit.prevent="handleSendMessage">
            <input
              v-model="userInput"
              type="text"
              class="form-input flex-1"
              placeholder="Ask anything about your resume, missing skills, or job matches..."
              :disabled="typing"
            />
            <button type="submit" class="btn btn-primary" :disabled="typing || !userInput.trim()">
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { aiApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const messagesContainer = ref(null)
const userInput = ref('')
const typing = ref(false)
const targetJobId = ref(route.query.job_id || null)

const suggestedPrompts = [
  'What jobs match my skills?',
  'What skills am I missing?',
  'How can I improve my resume score?',
  'Explain my match percentage'
]

const messages = ref([
  {
    sender: 'ai',
    text: `Hello ${authStore.userName}! 👋 I am your AI Career Coach.\n\nI have access to your resume analysis, extracted technical skills, and current job listings. Ask me any question to optimize your career path!`,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
])

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatMessage = (text) => {
  if (!text) return ''
  // Bold formatting **text** -> <strong>text</strong>
  let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  // Italic formatting *text* -> <em>$1</em>
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>')
  return formatted
}

const sendPrompt = (promptText) => {
  userInput.value = promptText
  handleSendMessage()
}

const handleSendMessage = async () => {
  const text = userInput.value.trim()
  if (!text || typing.value) return

  const userTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  messages.value.push({ sender: 'user', text, time: userTime })
  userInput.value = ''
  typing.value = true
  scrollToBottom()

  try {
    const res = await aiApi.sendChatMessage(text, targetJobId.value)
    const replyText = res.data?.reply || 'I am ready to help you with your resume and job search!'
    const aiTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    messages.value.push({ sender: 'ai', text: replyText, time: aiTime })
  } catch (err) {
    messages.value.push({
      sender: 'ai',
      text: 'I encountered an issue connecting to the AI engine. Please ensure your backend is running and try again.',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })
  } finally {
    typing.value = false
    scrollToBottom()
  }
}

const clearChat = () => {
  messages.value = [
    {
      sender: 'ai',
      text: 'Chat reset. How can I assist you with your career search today?',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]
}

onMounted(() => {
  if (targetJobId.value) {
    userInput.value = `Why did I receive this match score for job #${targetJobId.value}?`
    handleSendMessage()
  }
})
</script>

<style scoped>
.chat-card {
  border-radius: 20px;
  height: 75vh;
  display: flex;
  flex-direction: column;
}

.ai-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.ai-avatar-sm {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  margin-top: 4px;
}

.prompt-pill {
  font-size: 0.775rem;
  font-weight: 600;
  color: #4f46e5;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
  padding: 4px 10px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.prompt-pill:hover {
  background: #e0e7ff;
  transform: translateY(-1px);
}
</style>

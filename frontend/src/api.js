const API_URL = import.meta.env.VITE_API_URL || ''

export async function analyzeSubmission(submission) {
  if (API_URL) {
    const response = await fetch(`${API_URL}/api/analyze`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(submission) })
    if (!response.ok) throw new Error('Analysis request failed')
    return response.json()
  }
  return mockAnalysis(submission)
}

function mockAnalysis({ type, content }) {
  const value = content.toLowerCase()
  const indicators = []
  if (/urgent|immediately|now|24 hours|today/.test(value)) indicators.push({ label: 'Urgency language', detail: 'Creates pressure to act before you can verify the request.', points: 15 })
  if (/pin|password|otp|cvv|login|banking details/.test(value)) indicators.push({ label: 'Credential request', detail: 'Legitimate organisations will not ask for private security details over chat.', points: 25 })
  if (/pay|payment|eft|transfer|money|r\d+/.test(value)) indicators.push({ label: 'Financial pressure', detail: 'The message introduces a payment or money transfer request.', points: 20 })
  if (/http|www\.|\.com|\.co\.za/.test(value) || type === 'url') indicators.push({ label: 'Suspicious link', detail: 'Links can lead to lookalike pages designed to capture your details.', points: 25 })
  if (/bank|sars|delivery|family|boss|police/.test(value)) indicators.push({ label: 'Impersonation signal', detail: 'The sender may be using a trusted organisation or relationship to gain access.', points: 20 })
  const score = Math.min(indicators.reduce((total, item) => total + item.points, 0), 100)
  const classification = score >= 60 ? 'CRITICAL THREAT' : score >= 25 ? 'SUSPICIOUS' : 'SAFE'
  const action = classification === 'SAFE' ? 'No obvious fraud signals found. Still, only respond through a trusted channel.' : classification === 'SUSPICIOUS' ? 'Do not click or reply yet. Verify the sender through an official number or website.' : 'Do not click, pay or share information. Block the sender and report the message.'
  return { score, classification, indicators, action, input_type: type, mock: true }
}
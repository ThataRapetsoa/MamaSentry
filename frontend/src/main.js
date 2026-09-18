import './style.css'
import { analyzeSubmission } from './api.js'
import { renderInputForm } from './components/InputForm.js'
import { renderRiskResult } from './components/RiskResult.js'
import { renderThreatReasons } from './components/ThreatReasons.js'

const demoMessage = {
  type: 'message',
  content: 'SARS: Your 2026 tax refund of R4,280 is ready. Claim it immediately by confirming your banking details: https://sars-refund.co.za/claim',
}

const scenarios = [
  { tone: 'safe', label: 'Safe', title: 'The plan is clear', message: 'Hi Thandi, your appointment at Groote Schuur Hospital is confirmed for Thursday at 10:30. Reply YES to confirm.', flags: 'No pressure. No payment. No link.', score: '08 / 100' },
  { tone: 'suspicious', label: 'Suspicious', title: 'A link adds pressure', message: 'Your Takealot delivery could not be completed. Confirm your address today: https://takealot-delivery.co.za', flags: '“today” +15 · link +25', score: '40 / 100' },
  { tone: 'critical', label: 'Critical threat', title: 'The request wants access', message: 'Hi Mom, it’s me. My phone broke. Please send R2,000 urgently and don’t call, I’m in a meeting.', flags: '“urgently” +15 · money +20 · impersonation +20', score: '65 / 100' },
]

const app = document.querySelector('#app')

app.innerHTML = `
  <div class="site-shell">
    <header class="site-header">
      <a class="wordmark" href="/" aria-label="MamaSentry home"><span class="wordmark-seal">M</span><span>MamaSentry</span></a>
      <p class="header-note">A check before you act</p>
      <a class="header-link" href="#checker">Check a message</a>
    </header>
    <main>
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-copy"><p class="kicker">The ten seconds before you click or pay</p><h1 id="hero-title">You do not have a cybersecurity expert next to you.<br><em>Bring the message here.</em></h1><p class="hero-argument">MamaSentry is that person for a moment. We show you what feels wrong in a fake SARS refund, a payment confirmation, or a message from “your child” asking for help.</p></div>
        <div class="demo-grid" aria-label="Example fraud analysis">
          <div class="demo-message"><div class="message-top"><span>WhatsApp message</span><time>09:41</time></div><p>SARS: Your 2026 tax refund of <mark class="mark-amber">R4,280</mark> is ready. <mark class="mark-red">Claim it immediately</mark> by confirming your <mark class="mark-red">banking details</mark>:</p><a class="fake-link" href="#checker" aria-label="Suspicious SARS refund link">sars-refund.co.za/claim</a><span class="message-source">+27 72 184 9031</span></div>
          <div class="demo-explanation"><div class="analysis-heading"><span class="signal-pip"></span><span>Here is why we paused</span></div><div class="demo-score"><strong>80</strong><span>/ 100<br><b>CRITICAL THREAT</b></span></div><ul class="demo-flags"><li><mark class="mark-red">Claim it immediately</mark><span>Urgency language</span><b>+15</b></li><li><mark class="mark-red">banking details</mark><span>Credential request</span><b>+25</b></li><li><mark class="mark-amber">sars-refund.co.za</mark><span>Domain mismatch</span><b>+30</b></li></ul><p class="friend-warning">Do not click or share details. Open <strong>sars.gov.za</strong> yourself to check for a refund.</p></div>
        </div>
      </section>
      <section class="checker-section" id="checker" aria-labelledby="checker-title"><div class="section-intro"><span class="section-number">01</span><div><h2 id="checker-title">Put your message under the light</h2><p>Paste the text, link, or screenshot that made you hesitate.</p></div></div><div class="checker-layout"><div id="input-form"></div><div class="live-result"><div class="section-label">Your answer</div><div id="risk-result"></div><div id="threat-reasons"></div></div></div></section>
      <section class="flow-section" aria-labelledby="flow-title"><div class="section-intro"><span class="section-number">02</span><div><h2 id="flow-title">A pause with a purpose</h2><p>Three things happen before you decide what to do.</p></div></div><ol class="flow-list"><li><span>1</span><div><h3>Detect</h3><p>We look for pressure, money requests, credential requests, impersonation, and links that do not belong.</p></div></li><li><span>2</span><div><h3>Explain</h3><p>Each signal gets a name and a score. You can see the phrase that made the risk go up.</p></div></li><li><span>3</span><div><h3>Protect</h3><p>You get one plain next step: verify, stop, report, or safely continue.</p></div></li></ol></section>
      <section class="scenarios-section" aria-labelledby="scenarios-title"><div class="section-intro"><span class="section-number">03</span><div><h2 id="scenarios-title">What changes the answer?</h2><p>These messages can all arrive in an ordinary day. The details matter.</p></div></div><div class="scenario-table">${scenarios.map((scenario) => `<article class="scenario scenario-${scenario.tone}"><header><span>${scenario.label}</span><strong>${scenario.score}</strong></header><h3>${scenario.title}</h3><p class="scenario-message">${scenario.message}</p><p class="scenario-flags">${scenario.flags}</p></article>`).join('')}</div></section>
      <section class="signals-section" aria-labelledby="signals-title"><div class="signals-copy"><p class="kicker">The check is transparent</p><h2 id="signals-title">No mystery score.<br><em>Just the reasons.</em></h2><p>Our prototype adds points for the things scammers use to rush or persuade you. The score is a guide, not a probability of fraud.</p><div class="thresholds"><div><strong>0–24</strong><span>Safe</span></div><div><strong>25–59</strong><span>Suspicious</span></div><div><strong>60+</strong><span>Critical threat</span></div></div></div><ul class="signal-list"><li><span>+15</span><div><strong>Urgency language</strong><p>“Immediately”, “today”, or a deadline designed to stop you checking.</p></div></li><li><span>+20</span><div><strong>Financial pressure</strong><p>A request to pay, transfer, send an EFT, or “confirm” money.</p></div></li><li><span>+25</span><div><strong>Credential request</strong><p>A PIN, OTP, password, CVV, or banking details.</p></div></li><li><span>+25</span><div><strong>Suspicious URL</strong><p>A link that could lead to a lookalike page.</p></div></li><li><span>+30</span><div><strong>Domain mismatch</strong><p>The visible organisation and the real website do not match.</p></div></li></ul></section>
    </main>
    <footer><span class="wordmark-seal">M</span><span>MamaSentry</span><p>Before you click. Before you pay.</p></footer>
  </div>
`

const resultElement = document.querySelector('#risk-result')
const reasonsElement = document.querySelector('#threat-reasons')

function runAnalysis(submission) {
  renderRiskResult(resultElement, { loading: true })
  reasonsElement.innerHTML = ''
  window.setTimeout(async () => {
    const response = await analyzeSubmission(submission)
    renderRiskResult(resultElement, response)
    renderThreatReasons(reasonsElement, response)
  }, 450)
}

renderInputForm(document.querySelector('#input-form'), runAnalysis)
renderRiskResult(resultElement, { empty: true })
document.querySelector('.demo-message').addEventListener('click', () => { document.querySelector('#checker').scrollIntoView({ behavior: 'smooth' }); runAnalysis(demoMessage) })

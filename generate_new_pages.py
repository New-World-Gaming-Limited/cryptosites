#!/usr/bin/env python3
"""
Cryptosites.com — Strategic Pages Generator
Generates: How We Rate, Enhanced Comparison Tables, Educational Guides,
Buyer's Guides, and Warnings/Blacklist page.
Also updates navigation, footers, sitemap across ALL existing pages.
"""

import os, re, json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.now().strftime("%B %Y")

# ============================================================
# SHARED TEMPLATES
# ============================================================

PPLX_HEAD = """<!--
   ______                            __
  / ____/___  ____ ___  ____  __  __/ /____  _____
 / /   / __ \\/ __ `__ \\/ __ \\/ / / / __/ _ \\/ ___/
/ /___/ /_/ / / / / / / /_/ / /_/ / /_/  __/ /
\\____/\\____/_/ /_/ /_/ .___/\\__,_/\\__/\\___/_/
                    /_/
        Created with Perplexity Computer
        https://www.perplexity.ai/computer
-->

<!-- Perplexity Computer Attribution — SEO Meta Tags -->
<meta name="generator" content="Perplexity Computer">
<meta name="author" content="Perplexity Computer">
<meta property="og:see_also" content="https://www.perplexity.ai/computer">
<link rel="author" href="https://www.perplexity.ai/computer">"""

NAV_LINKS = """<a href="./index.html" class="{home_active}">Home</a>
<a href="./crypto-casinos.html" class="{casinos_active}">Casinos</a>
<a href="./crypto-sports-betting.html" class="{sports_active}">Sports Betting</a>
<a href="./crypto-poker.html" class="{poker_active}">Poker</a>
<a href="./crypto-exchanges.html" class="{exchanges_active}">Exchanges</a>
<a href="./crypto-lottery.html" class="{lottery_active}">Lottery</a>
<a href="./crypto-wallets.html" class="{wallets_active}">Wallets</a>
<a href="./how-we-rate.html" class="{rate_active}">How We Rate</a>"""

def get_nav(active=""):
    keys = ["home","casinos","sports","poker","exchanges","lottery","wallets","rate"]
    vals = {f"{k}_active": "active" if k == active else "" for k in keys}
    return NAV_LINKS.format(**vals)

LOGO_SVG = """<svg viewBox="0 0 32 32" width="32" height="32" fill="none" aria-label="Cryptosites logo">
  <path d="M16 2 L28 9 L28 23 L16 30 L4 23 L4 9 Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" opacity="0.6"/>
  <path d="M20 11 A6 6 0 1 0 20 21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="21" cy="11" r="1.5" fill="var(--secondary)"/>
  <circle cx="21" cy="21" r="1.5" fill="var(--secondary)"/>
</svg>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col footer-brand">
        <a href="./index.html" class="footer-logo" aria-label="Cryptosites home">
          {logo}
          <span class="nav-logo-text">Crypto<span class="logo-accent">sites</span></span>
        </a>
        <p class="footer-tagline">The most trusted source for crypto platform reviews. Independent, transparent, updated {now}.</p>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Top Promos</p>
        <div class="footer-links">
        <a href="./promo-stake-casino.html">Stake Casino</a>
        <a href="./promo-binance.html">Binance</a>
        <a href="./promo-kraken.html">Kraken</a>
        <a href="./promo-bc-game-casino.html">BC.Game</a>
        <a href="./promo-coinbase.html">Coinbase</a>
        <a href="./promo-cloudbet-casino.html">Cloudbet</a>
        <a href="./promo-ledger.html">Ledger</a>
        <a href="./promo-coinpoker.html">CoinPoker</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Categories</p>
        <div class="footer-links">
        <a href="./crypto-casinos.html">Crypto Casinos</a>
        <a href="./crypto-sports-betting.html">Crypto Sports</a>
        <a href="./crypto-poker.html">Crypto Poker</a>
        <a href="./crypto-exchanges.html">Crypto Exchanges</a>
        <a href="./crypto-lottery.html">Crypto Lottery</a>
        <a href="./crypto-wallets.html">Crypto Wallets</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Resources</p>
        <div class="footer-links">
        <a href="./how-we-rate.html">How We Rate</a>
        <a href="./guide-provably-fair.html">Provably Fair Guide</a>
        <a href="./guide-choosing-exchange.html">Choosing an Exchange</a>
        <a href="./guide-crypto-vs-traditional.html">Crypto vs Traditional</a>
        <a href="./guide-gas-fees.html">Understanding Gas Fees</a>
        <a href="./guide-wallet-security.html">Wallet Security</a>
        <a href="./warnings.html">Warnings &amp; Blacklist</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Best Of Guides</p>
        <div class="footer-links">
        <a href="./best-crypto-casino-slots.html">Best for Slots</a>
        <a href="./best-crypto-exchange-beginners.html">Best for Beginners</a>
        <a href="./best-crypto-casino-high-rollers.html">Best for High Rollers</a>
        <a href="./best-crypto-casino-privacy.html">Best for Privacy</a>
        <a href="./best-crypto-exchange-low-fees.html">Best for Low Fees</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Transparency</p>
        <div class="footer-links">
        <a href="./how-we-rate.html">Our Methodology</a>
        <a href="./about.html">Affiliate Disclosure</a>
        <a href="./about.html">Editorial Policy</a>
        <a href="./warnings.html">Platform Warnings</a>
        </div>
      </div>
    </div>
    <div class="rg-notice">
      <p class="footer-heading">18+ RESPONSIBLE GAMBLING</p>
      <p>Gambling and trading crypto involves risk. You must be 18+ to participate. Never invest or gamble more than you can afford to lose. If gambling is becoming a problem, seek help: <strong>National Council on Problem Gambling: 1-800-522-4700</strong> (US), <strong>GamCare: 0808 8020 133</strong> (UK). Crypto investments can go to zero. DYOR.</p>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Cryptosites. All rights reserved.</p>
      <a href="https://www.perplexity.ai/computer" target="_blank" rel="noopener noreferrer" style="font-size:12px;color:var(--text-muted)">Created with Perplexity Computer</a>
    </div>
    <p class="footer-disclaimer">Disclaimer: Cryptosites is an independent review site. We earn affiliate commissions when you sign up through our links — that is how we keep the lights on. This never influences our rankings or reviews. All bonus offers, rates, and availability are subject to change. Always read the terms and conditions. Crypto trading involves significant risk of loss. Past performance does not guarantee future results.</p>
  </div>
</footer>"""

def page_shell(title, description, url, active_nav, body_content, extra_head="", json_ld=""):
    nav = get_nav(active_nav)
    footer = FOOTER.format(logo=LOGO_SVG, now=NOW)
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
{PPLX_HEAD}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://cryptosites.com/{url}">
  <meta property="og:site_name" content="Cryptosites">
  <link rel="icon" href="./favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://api.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@700,800&f[]=satoshi@300,400,500,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./base.css">
  <link rel="stylesheet" href="./style.css">
{extra_head}{json_ld}
</head>
<body>
<a href="#main-content" class="skip-link">Skip to main content</a>
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="container nav-inner">
    <a href="./index.html" class="nav-logo" aria-label="Cryptosites home">
      {LOGO_SVG}
      <span class="nav-logo-text">Crypto<span class="logo-accent">sites</span></span>
    </a>
    <div class="nav-links">
      {nav}
    </div>
    <div class="nav-actions">
      <button class="theme-toggle" aria-label="Toggle dark/light mode" type="button">
        <span class="icon-sun"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></span>
        <span class="icon-moon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></span>
      </button>
      <button class="search-btn" aria-label="Search" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </button>
      <button class="mobile-menu-btn" aria-label="Toggle menu" aria-expanded="false" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </div>
</nav>

<main id="main-content">
{body_content}
</main>

{footer}
<script src="./app.js" defer></script>
</body>
</html>"""

# ============================================================
# PAGE 1: HOW WE RATE
# ============================================================
def generate_how_we_rate():
    body = """
<section class="content-hero">
  <div class="container container-narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="./index.html">Home</a> <span class="bc-sep">/</span> <span>How We Rate</span>
    </nav>
    <h1>How We Rate Crypto Platforms</h1>
    <p class="content-hero-sub">Our scoring methodology is transparent, repeatable, and designed to protect you. Every platform on Cryptosites goes through the same rigorous evaluation process.</p>
    <div class="content-meta">
      <span class="meta-badge">Methodology</span>
      <span class="meta-date">Last updated: March 2026</span>
      <span class="meta-author">By the Cryptosites Review Team</span>
    </div>
  </div>
</section>

<section class="content-body">
  <div class="container container-narrow">

    <div class="methodology-intro card-elevated">
      <h2>Why This Matters</h2>
      <p>The crypto space is full of affiliate sites that rank platforms based on who pays the highest commission. We take a different approach. Our ratings are based on a <strong>10-category scoring system</strong> that we apply consistently to every platform we review. We test each platform ourselves, verify claims independently, and update reviews quarterly.</p>
      <p>We earn affiliate commissions — that is how we keep the site running. But commissions never influence rankings. A platform that pays us 50% commission will still get a 2.0 rating if the product is poor. We have given negative reviews to platforms with active affiliate deals, and we will continue to do so.</p>
    </div>

    <h2>Our 10-Category Scoring System</h2>
    <p>Each category is scored 1-5 and weighted based on importance. The final rating is a weighted average rounded to one decimal.</p>

    <div class="rating-categories-grid">
      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
          <div class="rc-weight">20%</div>
        </div>
        <h3>Security &amp; Trust</h3>
        <p>Licensing, 2FA, cold storage, insurance, audit history, and past breach record. This is the single most important factor — no platform scores above 3.0 overall with poor security.</p>
        <ul class="rc-checklist">
          <li>Valid gambling/financial licence</li>
          <li>Two-factor authentication available</li>
          <li>Cold storage for majority of funds</li>
          <li>Independent security audits</li>
          <li>No unresolved breach history</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8l-4 4-4-4"/><path d="M12 12v6"/></svg></div>
          <div class="rc-weight">15%</div>
        </div>
        <h3>Fees &amp; Value</h3>
        <p>Trading fees, withdrawal fees, deposit fees, hidden charges, and overall bonus/promotion value. We calculate effective costs based on realistic usage patterns, not theoretical minimums.</p>
        <ul class="rc-checklist">
          <li>Transparent fee schedule</li>
          <li>Competitive rates vs. market average</li>
          <li>No hidden withdrawal charges</li>
          <li>Fair bonus wagering requirements</li>
          <li>No deceptive "free" claims</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
          <div class="rc-weight">10%</div>
        </div>
        <h3>User Experience</h3>
        <p>Interface design, navigation, mobile responsiveness, page load speeds, and overall ease of use. We test on multiple devices and browsers, including mobile-first scenarios.</p>
        <ul class="rc-checklist">
          <li>Intuitive navigation</li>
          <li>Mobile-responsive design</li>
          <li>Fast load times (&lt;3s)</li>
          <li>Clean, uncluttered interface</li>
          <li>Accessible to new users</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></div>
          <div class="rc-weight">10%</div>
        </div>
        <h3>Crypto Support</h3>
        <p>Number of supported cryptocurrencies, blockchain networks, deposit/withdrawal options, and integration with popular wallets. More is better, but quality matters too.</p>
        <ul class="rc-checklist">
          <li>Major cryptos (BTC, ETH, USDT)</li>
          <li>Multiple blockchain networks</li>
          <li>Wallet integrations</li>
          <li>Reasonable confirmation times</li>
          <li>Stablecoin support</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div>
          <div class="rc-weight">10%</div>
        </div>
        <h3>Customer Support</h3>
        <p>Response times, channel availability (live chat, email, phone), knowledge quality, and resolution rates. We submit test tickets and measure actual response quality.</p>
        <ul class="rc-checklist">
          <li>24/7 live chat available</li>
          <li>Response under 5 minutes</li>
          <li>Knowledgeable agents</li>
          <li>Issue resolved on first contact</li>
          <li>Multiple support channels</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
          <div class="rc-weight">10%</div>
        </div>
        <h3>Speed &amp; Reliability</h3>
        <p>Deposit confirmation times, withdrawal processing speed, platform uptime, and performance during high-traffic periods. We track real withdrawal times over weeks.</p>
        <ul class="rc-checklist">
          <li>Withdrawals processed within stated time</li>
          <li>99.9%+ uptime track record</li>
          <li>No degradation during peaks</li>
          <li>Fast deposit confirmations</li>
          <li>Consistent performance</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><circle cx="12" cy="17" r="0.5"/></svg></div>
          <div class="rc-weight">5%</div>
        </div>
        <h3>Transparency</h3>
        <p>Clear terms and conditions, visible fee structures, provably fair mechanisms (for casinos), and honest marketing. Platforms that hide information lose points here.</p>
        <ul class="rc-checklist">
          <li>Clear T&amp;Cs, easy to find</li>
          <li>No misleading advertising</li>
          <li>Provably fair verification (casinos)</li>
          <li>Public audit reports</li>
          <li>Honest about limitations</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
          <div class="rc-weight">5%</div>
        </div>
        <h3>KYC &amp; Privacy</h3>
        <p>Know Your Customer requirements, data handling practices, privacy policy quality, and options for anonymous usage. Balance between regulatory compliance and user privacy.</p>
        <ul class="rc-checklist">
          <li>Clear KYC requirements stated upfront</li>
          <li>Privacy-respecting data practices</li>
          <li>Options for reduced-KYC usage</li>
          <li>GDPR/privacy compliant</li>
          <li>No excessive data collection</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg></div>
          <div class="rc-weight">10%</div>
        </div>
        <h3>Product Range</h3>
        <p>Breadth and depth of offerings — games for casinos, markets for sports, trading pairs for exchanges. Quality over quantity, but range matters for versatility.</p>
        <ul class="rc-checklist">
          <li>Comprehensive offering for the category</li>
          <li>Quality providers/markets</li>
          <li>Regular new additions</li>
          <li>Unique features or exclusives</li>
          <li>Cross-category options (casino + sports)</li>
        </ul>
      </div>

      <div class="rating-category-card">
        <div class="rc-header">
          <div class="rc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></div>
          <div class="rc-weight">5%</div>
        </div>
        <h3>Community &amp; Reputation</h3>
        <p>Online sentiment, social media presence, community engagement, industry awards, and longevity. We aggregate reviews from Reddit, Trustpilot, and industry forums.</p>
        <ul class="rc-checklist">
          <li>Positive community sentiment</li>
          <li>Active social media presence</li>
          <li>Industry recognition/awards</li>
          <li>Years of operation</li>
          <li>Resolved complaints publicly</li>
        </ul>
      </div>
    </div>

    <h2>Our Review Process</h2>
    <div class="process-timeline">
      <div class="process-step">
        <div class="ps-number">1</div>
        <div class="ps-content">
          <h3>Account Creation &amp; First Impressions</h3>
          <p>We create real accounts on every platform we review. We evaluate the signup process, KYC requirements, and initial user experience. If a platform requires KYC, we go through the full verification process and time it.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">2</div>
        <div class="ps-content">
          <h3>Deposit &amp; Fund Testing</h3>
          <p>We deposit real cryptocurrency — typically BTC, ETH, and USDT — and record confirmation times, any fees charged, and the overall process smoothness. We test multiple deposit methods where available.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">3</div>
        <div class="ps-content">
          <h3>Product Testing (2-4 Weeks)</h3>
          <p>We actively use each platform for 2-4 weeks. For casinos, we play a variety of games. For exchanges, we execute trades across market conditions. For sportsbooks, we place bets across multiple sports. This is not a quick look — we live on the platform.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">4</div>
        <div class="ps-content">
          <h3>Withdrawal Testing</h3>
          <p>The true test of any crypto platform. We request withdrawals of varying sizes and track processing times against the platform's stated timeframes. We test multiple withdrawal methods and note any unexpected fees or delays.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">5</div>
        <div class="ps-content">
          <h3>Support Evaluation</h3>
          <p>We contact customer support through every available channel (live chat, email, social media) with pre-defined test scenarios ranging from basic questions to complex issues. We measure response times, agent knowledge, and resolution quality.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">6</div>
        <div class="ps-content">
          <h3>Scoring &amp; Publication</h3>
          <p>Two independent reviewers score the platform using our 10-category system. If scores diverge by more than 0.5 on any category, a third reviewer arbitrates. The final score is published with full category breakdowns.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">7</div>
        <div class="ps-content">
          <h3>Quarterly Re-Evaluation</h3>
          <p>Every reviewed platform is re-tested quarterly. Scores can go up or down based on changes to the platform, new security incidents, fee changes, or shifts in market standards. We note all score changes and the reasons behind them.</p>
        </div>
      </div>
    </div>

    <h2>Score Interpretation</h2>
    <div class="score-guide">
      <div class="sg-row sg-excellent"><div class="sg-score">4.5 - 5.0</div><div class="sg-label">Excellent</div><div class="sg-desc">Best in class. We would personally use and recommend this platform to anyone.</div></div>
      <div class="sg-row sg-good"><div class="sg-score">4.0 - 4.4</div><div class="sg-label">Very Good</div><div class="sg-desc">Strong platform with minor areas for improvement. Recommended with confidence.</div></div>
      <div class="sg-row sg-decent"><div class="sg-score">3.5 - 3.9</div><div class="sg-label">Good</div><div class="sg-desc">Solid option with some notable drawbacks. Suitable for most users with caveats.</div></div>
      <div class="sg-row sg-fair"><div class="sg-score">3.0 - 3.4</div><div class="sg-label">Fair</div><div class="sg-desc">Below average. Specific strengths but significant concerns. Proceed with caution.</div></div>
      <div class="sg-row sg-poor"><div class="sg-score">Below 3.0</div><div class="sg-label">Poor</div><div class="sg-desc">Not recommended. Major issues with security, reliability, or trust. See our <a href="./warnings.html">Warnings page</a>.</div></div>
    </div>

    <h2>What We Will Never Do</h2>
    <div class="commitments-grid">
      <div class="commitment-card">
        <span class="commitment-icon">&#10005;</span>
        <p>Rank a platform higher because they pay a higher affiliate commission</p>
      </div>
      <div class="commitment-card">
        <span class="commitment-icon">&#10005;</span>
        <p>Remove a negative review because a platform asked us to</p>
      </div>
      <div class="commitment-card">
        <span class="commitment-icon">&#10005;</span>
        <p>Publish a review without testing the platform ourselves first</p>
      </div>
      <div class="commitment-card">
        <span class="commitment-icon">&#10005;</span>
        <p>Hide a security incident or negative news about a listed platform</p>
      </div>
      <div class="commitment-card">
        <span class="commitment-icon">&#10005;</span>
        <p>Accept payment for favourable reviews or sponsored rankings</p>
      </div>
      <div class="commitment-card">
        <span class="commitment-icon">&#10005;</span>
        <p>Recommend a platform we would not use ourselves with our own money</p>
      </div>
    </div>

    <div class="cta-box">
      <h3>Questions About Our Methodology?</h3>
      <p>We believe in full transparency. If you have questions about how we scored a specific platform, or if you think we missed something, reach out to our editorial team. We read every message and update reviews when presented with new evidence.</p>
      <a href="./about.html" class="btn btn-accent">Contact Our Team</a>
    </div>

  </div>
</section>"""

    return page_shell(
        "How We Rate Crypto Platforms - Our Methodology | Cryptosites",
        "Learn how Cryptosites rates and reviews crypto casinos, exchanges, and wallets. Our transparent 10-category scoring system explained.",
        "how-we-rate.html",
        "rate",
        body
    )


# ============================================================
# PAGE 2: WARNINGS & BLACKLIST
# ============================================================
def generate_warnings():
    body = """
<section class="content-hero warnings-hero">
  <div class="container container-narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="./index.html">Home</a> <span class="bc-sep">/</span> <span>Warnings &amp; Blacklist</span>
    </nav>
    <h1>Warnings &amp; Blacklist</h1>
    <p class="content-hero-sub">Platforms we recommend you avoid. This page exists to protect you — not every crypto platform operates ethically, and some are outright dangerous.</p>
    <div class="content-meta">
      <span class="meta-badge meta-badge-danger">Safety Advisory</span>
      <span class="meta-date">Last updated: March 2026</span>
    </div>
  </div>
</section>

<section class="content-body">
  <div class="container container-narrow">

    <div class="warning-alert">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="warning-alert-icon"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      <div>
        <strong>This is not a sponsored hit list.</strong> Every platform listed here has documented evidence of harmful practices. We remove platforms from this list if they demonstrably fix the issues.
      </div>
    </div>

    <h2>Red Flags to Watch For</h2>
    <p>Before using any crypto platform, check for these warning signs:</p>

    <div class="red-flags-grid">
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>No Verifiable Licence</h3>
        <p>If a platform claims to be licensed but you cannot verify it through the regulator's website, that is a major red flag. Legitimate licences from Curacao, Malta, Gibraltar, or the UK can always be independently verified.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Delayed or Denied Withdrawals</h3>
        <p>The number one complaint in crypto gambling and trading. If a platform consistently takes longer than stated to process withdrawals, or imposes surprise KYC requirements only when you try to cash out, avoid them.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Fake or Bought Reviews</h3>
        <p>Check Trustpilot and Reddit carefully. If a platform has hundreds of 5-star reviews with similar language but almost no detailed negative reviews, those reviews are likely purchased. Real platforms have mixed reviews.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Unrealistic Promises</h3>
        <p>"Guaranteed 10x returns," "Risk-free trading," or "Guaranteed winning strategies" are lies. No legitimate platform makes guarantees about financial outcomes. This is the hallmark of scams.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>No Contact Information</h3>
        <p>Legitimate platforms provide clear contact details — a registered company name, physical address, and multiple support channels. If the only contact is an anonymous Telegram group, walk away.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Pressure Tactics</h3>
        <p>"Deposit now or lose your bonus forever," or aggressive account managers pushing you to deposit more. Legitimate platforms let you take your time and never pressure you to spend beyond your means.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Clone Sites</h3>
        <p>Scammers create exact copies of legitimate platforms (e.g., "Binannce.com" or "Coinbase-pro.net"). Always check the URL carefully and bookmark official sites. Use official app store links, not links from ads or emails.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Mandatory Minimum Wagering Before Withdrawal</h3>
        <p>Some platforms require you to wager a large multiple of your deposit before allowing any withdrawal — even of your own deposited funds. Read the terms before depositing.</p>
      </div>
    </div>

    <h2>Known Problem Platforms</h2>
    <p>The following platforms have documented issues that we believe make them unsafe for users. Click each for details.</p>

    <div class="blacklist-table">
      <div class="bl-item">
        <div class="bl-header">
          <span class="bl-name">Anonymous "DeFi Casinos" on Telegram</span>
          <span class="bl-status bl-status-scam">Likely Scam</span>
        </div>
        <div class="bl-details">
          <p><strong>Issues:</strong> Dozens of Telegram-based "casinos" have appeared offering impossibly high returns. They have no licence, no verifiable company information, and typically disappear after collecting deposits. Many are rebranded versions of previous scams.</p>
          <p><strong>What to do:</strong> Never deposit crypto into a platform that operates exclusively through Telegram or Discord with no website, no licence, and no verifiable identity.</p>
        </div>
      </div>
      <div class="bl-item">
        <div class="bl-header">
          <span class="bl-name">Yield-Generating Casino Tokens</span>
          <span class="bl-status bl-status-danger">High Risk</span>
        </div>
        <div class="bl-details">
          <p><strong>Issues:</strong> Some platforms sell tokens that promise "passive income from casino profits." These are typically unsustainable Ponzi-like structures where early investors are paid with money from new investors. The tokens inevitably collapse in value.</p>
          <p><strong>What to do:</strong> Treat any token promising guaranteed returns from gambling revenue as extremely high risk. Legitimate casinos do not need to sell tokens to fund operations.</p>
        </div>
      </div>
      <div class="bl-item">
        <div class="bl-header">
          <span class="bl-name">Unlicensed Exchange Clones</span>
          <span class="bl-status bl-status-scam">Scam</span>
        </div>
        <div class="bl-details">
          <p><strong>Issues:</strong> Phishing sites that copy the exact look of Binance, Coinbase, Kraken, and other major exchanges. They capture login credentials and drain wallets. Often promoted through social media ads, phishing emails, or compromised YouTube channels.</p>
          <p><strong>What to do:</strong> Bookmark the official URLs of every exchange you use. Never click exchange links from emails, ads, or social media. Enable 2FA and use hardware wallets for large holdings.</p>
        </div>
      </div>
      <div class="bl-item">
        <div class="bl-header">
          <span class="bl-name">"Recovery Service" Scams</span>
          <span class="bl-status bl-status-scam">Scam</span>
        </div>
        <div class="bl-details">
          <p><strong>Issues:</strong> Services claiming they can recover lost or stolen crypto for an upfront fee. In almost all cases, these are secondary scams targeting people who have already been scammed once. They collect the "recovery fee" and disappear.</p>
          <p><strong>What to do:</strong> If you have been scammed, report to local law enforcement and the platform involved. Do not pay anyone who claims they can recover your crypto.</p>
        </div>
      </div>
    </div>

    <h2>How to Protect Yourself</h2>
    <div class="protection-checklist">
      <div class="pc-item">
        <div class="pc-check">&#10003;</div>
        <div>
          <strong>Verify the licence.</strong> Go to the regulator's website (e.g., Curacao eGaming, MGA, UKGC) and search for the platform's licence number. If it does not appear, the licence is fake.
        </div>
      </div>
      <div class="pc-item">
        <div class="pc-check">&#10003;</div>
        <div>
          <strong>Start small.</strong> Always make a small test deposit and withdrawal before committing larger amounts. If the withdrawal goes smoothly, gradually increase.
        </div>
      </div>
      <div class="pc-item">
        <div class="pc-check">&#10003;</div>
        <div>
          <strong>Use a hardware wallet.</strong> Never leave large amounts of crypto on any platform — exchange, casino, or otherwise. Use a hardware wallet (Ledger, Trezor) for long-term storage.
        </div>
      </div>
      <div class="pc-item">
        <div class="pc-check">&#10003;</div>
        <div>
          <strong>Enable 2FA everywhere.</strong> Use an authenticator app (not SMS) for two-factor authentication on every crypto account you own.
        </div>
      </div>
      <div class="pc-item">
        <div class="pc-check">&#10003;</div>
        <div>
          <strong>Read the terms.</strong> Especially bonus terms, withdrawal limits, and KYC requirements. The 5 minutes it takes to read the T&amp;Cs can save you thousands.
        </div>
      </div>
      <div class="pc-item">
        <div class="pc-check">&#10003;</div>
        <div>
          <strong>Check multiple review sources.</strong> Do not rely on a single review site (including this one). Check Reddit, Trustpilot, and crypto forums for a complete picture.
        </div>
      </div>
    </div>

    <div class="cta-box cta-box-warning">
      <h3>Report a Suspicious Platform</h3>
      <p>If you have evidence of a crypto platform engaging in harmful practices — withdrawal delays, fake games, stolen funds — we want to hear about it. Help us protect the community.</p>
      <a href="./about.html" class="btn btn-accent">Report a Platform</a>
    </div>

  </div>
</section>"""

    return page_shell(
        "Crypto Platform Warnings & Blacklist - Stay Safe | Cryptosites",
        "Crypto platforms to avoid in 2026. Red flags, known scams, and how to protect yourself when using crypto casinos, exchanges, and wallets.",
        "warnings.html",
        "",
        body
    )


# ============================================================
# EDUCATIONAL GUIDES
# ============================================================

GUIDES = [
    {
        "slug": "guide-provably-fair",
        "title": "What is Provably Fair Gambling? Complete Guide",
        "meta_title": "Provably Fair Gambling Explained - How It Works | Cryptosites",
        "description": "Learn how provably fair technology works in crypto casinos. Understand server seeds, client seeds, and how to verify game outcomes yourself.",
        "badge": "Educational Guide",
        "content": """
    <h2>What Does "Provably Fair" Mean?</h2>
    <p>Provably fair is a cryptographic system that allows players to independently verify that a game outcome was not manipulated by the casino. It is one of the most significant innovations in online gambling — something that traditional casinos simply cannot offer.</p>
    <p>In a provably fair system, both the casino (server) and the player (client) contribute random data to generate the game outcome. Because the outcome depends on both inputs, neither party can predict or manipulate the result. After each game round, you can verify the math yourself.</p>

    <h2>How It Works: The Technical Process</h2>
    <div class="process-timeline">
      <div class="process-step">
        <div class="ps-number">1</div>
        <div class="ps-content">
          <h3>Server Seed Generation</h3>
          <p>Before the game round, the casino generates a random "server seed" and creates a hash (encrypted fingerprint) of it. You receive the hash — this proves the seed existed before you played, but you cannot see the actual seed yet.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">2</div>
        <div class="ps-content">
          <h3>Client Seed &amp; Nonce</h3>
          <p>You (the player) provide a "client seed" — this can be any text or number you choose. A nonce (game counter) is also included. Your seed ensures the casino cannot predict the outcome, because they do not control your input.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">3</div>
        <div class="ps-content">
          <h3>Outcome Calculation</h3>
          <p>The game combines the server seed, client seed, and nonce using a cryptographic function (typically HMAC-SHA256) to produce the game outcome. This calculation is deterministic — the same inputs always produce the same output.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">4</div>
        <div class="ps-content">
          <h3>Verification</h3>
          <p>After the round, the casino reveals the original server seed. You can now hash it yourself and confirm it matches the hash you received in Step 1. Then, using the server seed + your client seed + nonce, you can recalculate the outcome and verify it matches what was played.</p>
        </div>
      </div>
    </div>

    <h2>Which Crypto Casinos Are Provably Fair?</h2>
    <p>Not all crypto casinos offer provably fair games. Here are the platforms we have verified:</p>
    <div class="comparison-mini">
      <table class="guide-table">
        <thead><tr><th>Platform</th><th>Provably Fair</th><th>Verification Tool</th><th>Game Types</th></tr></thead>
        <tbody>
          <tr><td><a href="./promo-stake-casino.html">Stake</a></td><td class="td-yes">Yes</td><td>Built-in verifier</td><td>Originals (Dice, Crash, Plinko, Mines)</td></tr>
          <tr><td><a href="./promo-bc-game-casino.html">BC.Game</a></td><td class="td-yes">Yes</td><td>Built-in verifier</td><td>Originals (Classic Dice, Hash Dice, Crash)</td></tr>
          <tr><td><a href="./promo-fortunejack.html">FortuneJack</a></td><td class="td-yes">Yes</td><td>Built-in verifier</td><td>Dice, Crash games</td></tr>
          <tr><td><a href="./promo-bitstarz.html">BitStarz</a></td><td class="td-partial">Partial</td><td>Third-party audit</td><td>Selected games only</td></tr>
          <tr><td><a href="./promo-mbit-casino.html">mBit Casino</a></td><td class="td-no">No</td><td>N/A</td><td>Uses RNG certification instead</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Provably Fair vs. Traditional RNG</h2>
    <div class="vs-table">
      <table class="guide-table">
        <thead><tr><th>Feature</th><th>Provably Fair</th><th>Traditional RNG</th></tr></thead>
        <tbody>
          <tr><td>Verification</td><td class="td-yes">Player can verify each round</td><td class="td-no">Trust the auditor</td></tr>
          <tr><td>Transparency</td><td class="td-yes">Open algorithm, public seeds</td><td class="td-no">Black box</td></tr>
          <tr><td>Manipulation risk</td><td class="td-yes">Mathematically impossible</td><td class="td-partial">Depends on auditor quality</td></tr>
          <tr><td>Game variety</td><td class="td-partial">Mainly originals/simple games</td><td class="td-yes">All game types</td></tr>
          <tr><td>Industry standard</td><td class="td-partial">Crypto casinos only</td><td class="td-yes">All licensed casinos</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Limitations of Provably Fair</h2>
    <p>Provably fair is powerful but not perfect:</p>
    <ul class="content-list">
      <li><strong>Only applies to specific games.</strong> Slot games from providers like Pragmatic Play or NetEnt use their own RNG systems, not provably fair. Provably fair typically applies to "original" games like dice, crash, and mines.</li>
      <li><strong>Does not guarantee fair odds.</strong> A game can be provably fair (not rigged) but still have a high house edge. Always check the stated house edge before playing.</li>
      <li><strong>Requires technical knowledge to verify.</strong> While most platforms provide built-in verification tools, truly independent verification requires understanding of hash functions.</li>
    </ul>

    <div class="cta-box">
      <h3>Ready to Try Provably Fair Gaming?</h3>
      <p>Stake and BC.Game both offer excellent provably fair original games with built-in verification tools.</p>
      <div class="cta-buttons">
        <a href="./promo-stake-casino.html" class="btn btn-accent">Stake Casino Promo</a>
        <a href="./promo-bc-game-casino.html" class="btn btn-outline">BC.Game Promo</a>
      </div>
    </div>"""
    },
    {
        "slug": "guide-crypto-vs-traditional",
        "title": "Crypto Casino vs Traditional Online Casino: Full Comparison",
        "meta_title": "Crypto Casino vs Traditional Casino - Which is Better? | Cryptosites",
        "description": "Compare crypto casinos with traditional online casinos. Speed, privacy, fees, bonuses, game selection, and security compared side by side.",
        "badge": "Comparison Guide",
        "content": """
    <h2>The Core Differences</h2>
    <p>Crypto casinos and traditional online casinos offer fundamentally different experiences. Neither is universally "better" — it depends on what you value most: speed, privacy, bonus size, game selection, or regulatory protection.</p>

    <div class="vs-table">
      <table class="guide-table">
        <thead><tr><th>Factor</th><th>Crypto Casino</th><th>Traditional Casino</th></tr></thead>
        <tbody>
          <tr><td><strong>Deposit Speed</strong></td><td class="td-yes">Minutes (blockchain confirmation)</td><td class="td-partial">Hours to days (bank processing)</td></tr>
          <tr><td><strong>Withdrawal Speed</strong></td><td class="td-yes">Minutes to hours</td><td class="td-no">1-5 business days</td></tr>
          <tr><td><strong>Privacy</strong></td><td class="td-yes">Often anonymous or low-KYC</td><td class="td-no">Full KYC required</td></tr>
          <tr><td><strong>Bonus Size</strong></td><td class="td-yes">Often larger (1-10 BTC)</td><td class="td-partial">Typically capped lower</td></tr>
          <tr><td><strong>Regulatory Protection</strong></td><td class="td-partial">Varies — some well-licensed</td><td class="td-yes">Strong (UKGC, MGA, etc.)</td></tr>
          <tr><td><strong>Game Selection</strong></td><td class="td-partial">Growing, but fewer exclusives</td><td class="td-yes">Widest selection available</td></tr>
          <tr><td><strong>Provably Fair</strong></td><td class="td-yes">Available on original games</td><td class="td-no">Not available</td></tr>
          <tr><td><strong>Fees</strong></td><td class="td-yes">Minimal or zero</td><td class="td-partial">Varies by payment method</td></tr>
          <tr><td><strong>Geographic Access</strong></td><td class="td-yes">Often globally accessible</td><td class="td-no">Country-restricted</td></tr>
          <tr><td><strong>Responsible Gambling Tools</strong></td><td class="td-partial">Basic on most platforms</td><td class="td-yes">Comprehensive (mandated by law)</td></tr>
        </tbody>
      </table>
    </div>

    <h2>When to Choose a Crypto Casino</h2>
    <ul class="content-list">
      <li><strong>You value privacy.</strong> Crypto casinos often require minimal personal information, with some allowing fully anonymous play.</li>
      <li><strong>You want faster payouts.</strong> Crypto withdrawals typically process in minutes, not days. This is the single biggest advantage.</li>
      <li><strong>You already hold cryptocurrency.</strong> If you hold BTC, ETH, or other crypto, gambling directly avoids conversion fees and bank complications.</li>
      <li><strong>You want provably fair games.</strong> Only crypto casinos offer this level of game transparency.</li>
      <li><strong>Traditional casinos are restricted in your country.</strong> Crypto casinos often accept players from regions where traditional online gambling is limited.</li>
    </ul>

    <h2>When to Choose a Traditional Casino</h2>
    <ul class="content-list">
      <li><strong>You want maximum regulatory protection.</strong> UKGC and MGA-licensed casinos must follow strict player protection rules, including deposit limits and self-exclusion.</li>
      <li><strong>You prefer paying in fiat currency.</strong> If you do not hold crypto and do not want to buy any, traditional casinos are simpler.</li>
      <li><strong>Game selection is your priority.</strong> Traditional casinos still have access to some exclusive game providers.</li>
      <li><strong>You need strong responsible gambling tools.</strong> Regulated traditional casinos are legally required to offer comprehensive self-exclusion and limit-setting tools.</li>
    </ul>

    <h2>The Middle Ground: Hybrid Casinos</h2>
    <p>Many platforms now accept both crypto and fiat currencies. <a href="./promo-bitstarz.html">BitStarz</a>, <a href="./promo-cloudbet-casino.html">Cloudbet</a>, and several others bridge both worlds — giving you the speed of crypto deposits with the game selection of traditional platforms.</p>

    <div class="cta-box">
      <h3>Explore Our Top-Rated Crypto Casinos</h3>
      <p>All independently tested and rated using our <a href="./how-we-rate.html">10-category scoring system</a>.</p>
      <a href="./crypto-casinos.html" class="btn btn-accent">View Crypto Casino Rankings</a>
    </div>"""
    },
    {
        "slug": "guide-choosing-exchange",
        "title": "How to Choose a Crypto Exchange: 7 Essential Criteria",
        "meta_title": "How to Choose a Crypto Exchange - Beginner's Guide 2026 | Cryptosites",
        "description": "A complete guide to choosing the right crypto exchange. Security, fees, crypto selection, KYC requirements, and more explained for beginners.",
        "badge": "Beginner Guide",
        "content": """
    <h2>Why Your Choice of Exchange Matters</h2>
    <p>Your crypto exchange is where your money lives, at least temporarily. Choosing poorly can mean losing funds to a hack, paying excessive fees, or getting locked out of your account. The good news: in 2026, there are several excellent options. Here is how to evaluate them.</p>

    <h2>The 7 Essential Criteria</h2>

    <div class="process-timeline">
      <div class="process-step">
        <div class="ps-number">1</div>
        <div class="ps-content">
          <h3>Security Track Record</h3>
          <p>This is non-negotiable. Check whether the exchange has ever been hacked, and if so, how they handled it. Look for: two-factor authentication, cold storage of funds, insurance coverage, and regulatory licences.</p>
          <p><strong>Best in class:</strong> <a href="./promo-kraken.html">Kraken</a> has never been hacked since 2011. <a href="./promo-coinbase.html">Coinbase</a> is publicly traded and SOC 2 certified.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">2</div>
        <div class="ps-content">
          <h3>Fee Structure</h3>
          <p>Fees vary dramatically between exchanges. Look at: trading fees (maker/taker), withdrawal fees, deposit fees, and spread (the difference between buy and sell price). Low advertised trading fees can be offset by high withdrawal fees.</p>
          <div class="comparison-mini">
            <table class="guide-table">
              <thead><tr><th>Exchange</th><th>Maker Fee</th><th>Taker Fee</th><th>BTC Withdrawal</th></tr></thead>
              <tbody>
                <tr><td><a href="./promo-binance.html">Binance</a></td><td>0.10%</td><td>0.10%</td><td>0.0002 BTC</td></tr>
                <tr><td><a href="./promo-kraken.html">Kraken</a></td><td>0.16%</td><td>0.26%</td><td>0.00015 BTC</td></tr>
                <tr><td><a href="./promo-coinbase.html">Coinbase</a></td><td>0.40%</td><td>0.60%</td><td>Dynamic</td></tr>
                <tr><td><a href="./promo-kucoin.html">KuCoin</a></td><td>0.10%</td><td>0.10%</td><td>0.0004 BTC</td></tr>
                <tr><td><a href="./promo-bybit.html">Bybit</a></td><td>0.10%</td><td>0.10%</td><td>0.0002 BTC</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">3</div>
        <div class="ps-content">
          <h3>Available Cryptocurrencies</h3>
          <p>If you only want BTC and ETH, any exchange works. If you want access to altcoins, check the selection carefully. <a href="./promo-kucoin.html">KuCoin</a> leads with 700+ tokens, while <a href="./promo-gemini.html">Gemini</a> is more selective with 100+.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">4</div>
        <div class="ps-content">
          <h3>KYC Requirements</h3>
          <p>Some exchanges require full identity verification before you can trade. Others allow basic trading with just an email. Consider how much personal information you are comfortable sharing. More KYC typically means better regulatory protection but less privacy.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">5</div>
        <div class="ps-content">
          <h3>Geographic Availability</h3>
          <p>Not all exchanges operate in all countries. US users, in particular, have restricted access to some global exchanges like Binance (must use Binance.US) and Bybit. Check availability before creating an account.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">6</div>
        <div class="ps-content">
          <h3>User Experience</h3>
          <p>If you are a beginner, prioritize simplicity. <a href="./promo-coinbase.html">Coinbase</a> and <a href="./promo-crypto-com.html">Crypto.com</a> are the most beginner-friendly. If you are an experienced trader, look at <a href="./promo-binance.html">Binance</a> or <a href="./promo-bybit.html">Bybit</a> for advanced tools.</p>
        </div>
      </div>
      <div class="process-step">
        <div class="ps-number">7</div>
        <div class="ps-content">
          <h3>Customer Support Quality</h3>
          <p>You will likely need support at some point. Test the live chat before depositing significant funds. Check response times and whether agents actually understand the platform.</p>
        </div>
      </div>
    </div>

    <h2>Our Exchange Recommendations by Use Case</h2>
    <div class="comparison-mini">
      <table class="guide-table">
        <thead><tr><th>If you want...</th><th>Best choice</th><th>Why</th></tr></thead>
        <tbody>
          <tr><td>Maximum security</td><td><a href="./promo-kraken.html">Kraken</a></td><td>Never hacked, operating since 2011</td></tr>
          <tr><td>Lowest fees</td><td><a href="./promo-binance.html">Binance</a></td><td>0.10% maker/taker, industry-leading</td></tr>
          <tr><td>Easiest for beginners</td><td><a href="./promo-coinbase.html">Coinbase</a></td><td>Clean UI, publicly traded, insured</td></tr>
          <tr><td>Most altcoins</td><td><a href="./promo-kucoin.html">KuCoin</a></td><td>700+ tokens listed</td></tr>
          <tr><td>Best mobile app</td><td><a href="./promo-crypto-com.html">Crypto.com</a></td><td>Excellent app + Visa card</td></tr>
          <tr><td>Derivatives trading</td><td><a href="./promo-bybit.html">Bybit</a></td><td>Best futures/options platform</td></tr>
        </tbody>
      </table>
    </div>

    <div class="cta-box">
      <h3>Compare All Crypto Exchanges</h3>
      <p>See our full rankings with detailed scores across all 10 rating categories.</p>
      <a href="./crypto-exchanges.html" class="btn btn-accent">View Exchange Rankings</a>
    </div>"""
    },
    {
        "slug": "guide-gas-fees",
        "title": "Understanding Crypto Gas Fees: A Complete Guide",
        "meta_title": "Crypto Gas Fees Explained - What They Are & How to Save | Cryptosites",
        "description": "Learn what gas fees are, why they vary, and how to minimise transaction costs when using crypto casinos, exchanges, and wallets.",
        "badge": "Educational Guide",
        "content": """
    <h2>What Are Gas Fees?</h2>
    <p>Gas fees are the transaction costs you pay to use a blockchain network. Think of them as postage — you pay a fee for the network to process and confirm your transaction. Every time you send crypto, swap tokens, or interact with a smart contract, you pay gas.</p>
    <p>The term "gas" originated from Ethereum, but every blockchain has transaction fees. Bitcoin calls them "miner fees," Solana calls them "transaction fees," but the concept is the same.</p>

    <h2>Why Do Fees Vary So Much?</h2>
    <p>Blockchain fees fluctuate based on network demand. When many people are trying to use the network simultaneously, fees spike — sometimes dramatically. During the 2021 NFT boom, Ethereum gas fees regularly exceeded $100 per transaction. In quiet periods, they can be under $1.</p>

    <div class="comparison-mini">
      <table class="guide-table">
        <thead><tr><th>Network</th><th>Typical Fee</th><th>Speed</th><th>Used By</th></tr></thead>
        <tbody>
          <tr><td>Bitcoin (BTC)</td><td>$1 - $15</td><td>10-60 min</td><td>Most platforms</td></tr>
          <tr><td>Ethereum (ETH)</td><td>$2 - $50</td><td>1-5 min</td><td>DeFi, NFTs, many exchanges</td></tr>
          <tr><td>Tron (TRX)</td><td>$0.01 - $1</td><td>3 seconds</td><td>USDT transfers, some casinos</td></tr>
          <tr><td>Solana (SOL)</td><td>$0.001 - $0.01</td><td>400ms</td><td>Some exchanges, DeFi</td></tr>
          <tr><td>Litecoin (LTC)</td><td>$0.01 - $0.10</td><td>2-5 min</td><td>Many casinos, exchanges</td></tr>
          <tr><td>Polygon (MATIC)</td><td>$0.01 - $0.10</td><td>2 seconds</td><td>Some exchanges, DeFi</td></tr>
        </tbody>
      </table>
    </div>

    <h2>How to Minimise Gas Fees</h2>
    <div class="tips-grid">
      <div class="tip-card">
        <h3>Use Low-Fee Networks</h3>
        <p>When depositing to a casino or exchange, choose TRC-20 (Tron) for USDT transfers instead of ERC-20 (Ethereum). The difference can be $0.50 vs $15+ for the same transaction.</p>
      </div>
      <div class="tip-card">
        <h3>Time Your Transactions</h3>
        <p>Ethereum fees are typically lowest on weekends and during off-peak hours (early morning UTC). Avoid transacting during major market events or NFT drops.</p>
      </div>
      <div class="tip-card">
        <h3>Batch Your Transfers</h3>
        <p>Instead of making five $100 deposits, make one $500 deposit. You pay gas once instead of five times. This applies to both casino deposits and exchange withdrawals.</p>
      </div>
      <div class="tip-card">
        <h3>Use Layer 2 Solutions</h3>
        <p>Networks like Polygon, Arbitrum, and Optimism offer Ethereum-compatible transactions at a fraction of the cost. Some exchanges now support direct L2 withdrawals.</p>
      </div>
      <div class="tip-card">
        <h3>Choose Platforms with Free Withdrawals</h3>
        <p>Some exchanges absorb withdrawal fees. <a href="./promo-kraken.html">Kraken</a> and <a href="./promo-gemini.html">Gemini</a> (10 free per month) offer free or subsidised withdrawals on certain assets.</p>
      </div>
      <div class="tip-card">
        <h3>Use Lightning Network for Bitcoin</h3>
        <p>Bitcoin's Lightning Network enables near-instant, near-free BTC transfers. <a href="./promo-kraken.html">Kraken</a> and some crypto casinos support Lightning deposits and withdrawals.</p>
      </div>
    </div>

    <h2>Gas Fees When Using Crypto Casinos</h2>
    <p>This is where gas fees can catch you off guard:</p>
    <ul class="content-list">
      <li><strong>Deposits:</strong> You pay the blockchain fee to send crypto to the casino. Choose a low-fee network — most casinos accept USDT on Tron (TRC-20) which costs pennies.</li>
      <li><strong>Withdrawals:</strong> Most casinos cover the withdrawal fee, but some pass it on to you. Check before playing. Platforms like <a href="./promo-stake-casino.html">Stake</a> and <a href="./promo-bc-game-casino.html">BC.Game</a> typically cover standard withdrawal fees.</li>
      <li><strong>Minimum withdrawals:</strong> Many casinos set minimum withdrawal amounts that are higher than the gas fee. This is normal but worth checking — you do not want to play below the minimum and get stuck.</li>
    </ul>

    <div class="cta-box">
      <h3>Find Low-Fee Crypto Platforms</h3>
      <p>Our exchange and casino reviews include detailed fee breakdowns for every platform.</p>
      <div class="cta-buttons">
        <a href="./best-crypto-exchange-low-fees.html" class="btn btn-accent">Lowest Fee Exchanges</a>
        <a href="./crypto-casinos.html" class="btn btn-outline">Casino Reviews</a>
      </div>
    </div>"""
    },
    {
        "slug": "guide-wallet-security",
        "title": "Crypto Wallet Security: How to Protect Your Assets",
        "meta_title": "Crypto Wallet Security Guide - Protect Your Assets 2026 | Cryptosites",
        "description": "Essential security practices for crypto wallets. Hardware wallets, seed phrases, 2FA, and common scams to avoid. Protect your Bitcoin and crypto.",
        "badge": "Security Guide",
        "content": """
    <h2>Why Wallet Security Is Critical</h2>
    <p>In crypto, you are your own bank. There is no "forgot password" button, no fraud department to call, and no insurance if you lose access. If someone steals your private keys or seed phrase, your funds are gone permanently. This guide covers everything you need to know to keep your crypto safe.</p>

    <h2>Types of Wallets</h2>
    <div class="comparison-mini">
      <table class="guide-table">
        <thead><tr><th>Type</th><th>Security</th><th>Convenience</th><th>Best For</th></tr></thead>
        <tbody>
          <tr><td><strong>Hardware Wallet</strong></td><td class="td-yes">Highest</td><td class="td-partial">Medium</td><td>Long-term storage of significant holdings</td></tr>
          <tr><td><strong>Software Wallet</strong></td><td class="td-partial">Medium</td><td class="td-yes">High</td><td>Daily transactions, DeFi interaction</td></tr>
          <tr><td><strong>Exchange Wallet</strong></td><td class="td-partial">Medium</td><td class="td-yes">Highest</td><td>Active trading (not long-term storage)</td></tr>
          <tr><td><strong>Paper Wallet</strong></td><td class="td-yes">High (if stored well)</td><td class="td-no">Low</td><td>Cold storage backup</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Essential Security Practices</h2>
    <div class="tips-grid">
      <div class="tip-card">
        <h3>Use a Hardware Wallet</h3>
        <p>For any amount you cannot afford to lose, use a hardware wallet like <a href="./promo-ledger.html">Ledger</a> or <a href="./promo-trezor.html">Trezor</a>. These devices keep your private keys offline, making them immune to remote hacking. Even if your computer is compromised, your crypto stays safe.</p>
      </div>
      <div class="tip-card">
        <h3>Protect Your Seed Phrase</h3>
        <p>Your seed phrase (12 or 24 words) is the master key to your wallet. Write it down on paper or metal — never store it digitally (no photos, no cloud storage, no notes apps). Store it in a fireproof safe or safety deposit box. Make multiple copies stored in different locations.</p>
      </div>
      <div class="tip-card">
        <h3>Enable 2FA Everywhere</h3>
        <p>Use an authenticator app (Google Authenticator, Authy) — never SMS. SMS can be intercepted through SIM swapping. Enable 2FA on every exchange, wallet app, and email account connected to your crypto.</p>
      </div>
      <div class="tip-card">
        <h3>Use Unique, Strong Passwords</h3>
        <p>Every crypto-related account should have a unique password. Use a password manager (1Password, Bitwarden). If one platform is breached, attackers should not be able to access your other accounts.</p>
      </div>
      <div class="tip-card">
        <h3>Verify Transaction Addresses</h3>
        <p>Always double-check wallet addresses before sending. Clipboard malware can replace the address you copied with an attacker's address. Verify at least the first and last 6 characters of any address.</p>
      </div>
      <div class="tip-card">
        <h3>Use a Dedicated Device</h3>
        <p>For significant holdings, consider a dedicated device (old phone or laptop) used only for crypto. No browsing, no app downloads, no email. This dramatically reduces your attack surface.</p>
      </div>
    </div>

    <h2>Common Wallet Scams to Avoid</h2>
    <div class="red-flags-grid">
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Fake Wallet Apps</h3>
        <p>Scammers create convincing copies of popular wallet apps. Only download wallets from official websites or verified app store listings. Check the developer name and review count carefully.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Seed Phrase Phishing</h3>
        <p>No legitimate service will ever ask for your seed phrase. Not support, not "verification," not "wallet sync." Anyone asking for your seed phrase is trying to steal your funds.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>"Approval" Scams</h3>
        <p>DeFi transactions may ask you to "approve" token spending. Malicious contracts can set unlimited approval, allowing them to drain your wallet later. Always check what you are approving and revoke unused approvals regularly.</p>
      </div>
      <div class="red-flag-card">
        <div class="rf-icon">&#9888;</div>
        <h3>Airdrop Scams</h3>
        <p>Unsolicited tokens appearing in your wallet may contain malicious contracts. Do not interact with tokens you did not buy or expect. Ignore them — interacting can trigger wallet drains.</p>
      </div>
    </div>

    <h2>Our Recommended Wallets</h2>
    <div class="comparison-mini">
      <table class="guide-table">
        <thead><tr><th>Wallet</th><th>Type</th><th>Best For</th><th>Rating</th></tr></thead>
        <tbody>
          <tr><td><a href="./promo-ledger.html">Ledger</a></td><td>Hardware</td><td>Best overall security</td><td>4.7/5</td></tr>
          <tr><td><a href="./promo-trezor.html">Trezor</a></td><td>Hardware</td><td>Open-source, beginner-friendly</td><td>4.6/5</td></tr>
          <tr><td><a href="./promo-metamask.html">MetaMask</a></td><td>Software</td><td>DeFi &amp; Ethereum ecosystem</td><td>4.3/5</td></tr>
          <tr><td><a href="./promo-trust-wallet.html">Trust Wallet</a></td><td>Software</td><td>Multi-chain mobile wallet</td><td>4.2/5</td></tr>
          <tr><td><a href="./promo-exodus.html">Exodus</a></td><td>Software</td><td>Beautiful UI, beginner-friendly</td><td>4.1/5</td></tr>
        </tbody>
      </table>
    </div>

    <div class="cta-box">
      <h3>Get a Hardware Wallet</h3>
      <p>The single best thing you can do for your crypto security is using a hardware wallet.</p>
      <div class="cta-buttons">
        <a href="./promo-ledger.html" class="btn btn-accent">Ledger Promo</a>
        <a href="./promo-trezor.html" class="btn btn-outline">Trezor Promo</a>
      </div>
    </div>"""
    },
]

def generate_guide(guide):
    body = f"""
<section class="content-hero">
  <div class="container container-narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="./index.html">Home</a> <span class="bc-sep">/</span> <a href="./how-we-rate.html">Resources</a> <span class="bc-sep">/</span> <span>{guide['title'].split(':')[0] if ':' in guide['title'] else guide['title']}</span>
    </nav>
    <h1>{guide['title']}</h1>
    <div class="content-meta">
      <span class="meta-badge">{guide['badge']}</span>
      <span class="meta-date">Updated: {NOW}</span>
      <span class="meta-author">By the Cryptosites Review Team</span>
    </div>
  </div>
</section>

<section class="content-body">
  <div class="container container-narrow">
{guide['content']}
  </div>
</section>"""

    return page_shell(
        guide['meta_title'],
        guide['description'],
        f"{guide['slug']}.html",
        "",
        body
    )


# ============================================================
# BUYER'S GUIDES
# ============================================================

BUYERS_GUIDES = [
    {
        "slug": "best-crypto-casino-slots",
        "title": "Best Crypto Casinos for Slots in 2026",
        "meta_title": "Best Crypto Casinos for Slots 2026 - Top Bitcoin Slot Sites | Cryptosites",
        "description": "Find the best crypto casinos for playing slots in 2026. Compare game libraries, slot providers, RTP rates, and welcome bonuses.",
        "hero_sub": "If slots are your game, these are the crypto casinos with the biggest libraries, best providers, and most generous slot-specific bonuses.",
        "rankings": [
            {"name": "Stake", "slug": "stake-casino", "rating": 4.9, "reason": "3,000+ slots from 40+ providers. Fast payouts and excellent VIP rewards for slot players.", "highlight": "3,000+ Slots"},
            {"name": "BitStarz", "slug": "bitstarz", "rating": 4.8, "reason": "Award-winning slot selection with exclusive BitStarz titles. 10-minute withdrawal average.", "highlight": "Exclusive Titles"},
            {"name": "BC.Game", "slug": "bc-game-casino", "rating": 4.8, "reason": "2,500+ slots with daily slot tournaments and community jackpots.", "highlight": "Daily Tournaments"},
            {"name": "mBit Casino", "slug": "mbit-casino", "rating": 4.6, "reason": "300 free spins with welcome bonus. Strong Pragmatic Play and NetEnt selection.", "highlight": "300 Free Spins"},
            {"name": "Wild.io", "slug": "wild-io", "rating": 4.4, "reason": "Modern platform with 10 BTC welcome package. Good for high-stakes slot play.", "highlight": "10 BTC Bonus"},
        ],
        "what_to_look_for": [
            ("Game Library Size", "More games means more variety. The best crypto slot casinos offer 2,000+ titles from multiple providers."),
            ("Slot Providers", "Look for casinos with top providers: Pragmatic Play, NetEnt, Play'n GO, Microgaming, and Hacksaw Gaming."),
            ("RTP Transparency", "Return to Player (RTP) should be clearly stated. Look for slots with 96%+ RTP for better long-term value."),
            ("Free Spins Bonuses", "Slot-specific welcome bonuses with free spins are more valuable than generic deposit matches for slot players."),
            ("Jackpot Availability", "Progressive jackpots can offer life-changing wins. Check if the casino offers them from major jackpot networks."),
        ],
    },
    {
        "slug": "best-crypto-exchange-beginners",
        "title": "Best Crypto Exchanges for Beginners in 2026",
        "meta_title": "Best Crypto Exchanges for Beginners 2026 - Easiest Platforms | Cryptosites",
        "description": "The easiest crypto exchanges for beginners in 2026. Simple interfaces, low minimums, educational resources, and strong security.",
        "hero_sub": "New to crypto? These exchanges make buying your first Bitcoin as simple as possible — with strong security to protect you while you learn.",
        "rankings": [
            {"name": "Coinbase", "slug": "coinbase", "rating": 4.7, "reason": "The gold standard for beginners. Clean interface, educational earn program, publicly traded.", "highlight": "Easiest UI"},
            {"name": "Crypto.com", "slug": "crypto-com", "rating": 4.5, "reason": "$1 minimum deposit, excellent app, Visa card for spending crypto. Most accessible entry point.", "highlight": "$1 Minimum"},
            {"name": "Kraken", "slug": "kraken", "rating": 4.8, "reason": "Beginner mode hides complexity. Excellent educational resources and perfect security record.", "highlight": "Best Security"},
            {"name": "Gemini", "slug": "gemini", "rating": 4.4, "reason": "Available in all 50 US states. SOC 2 certified. Clean, unintimidating interface.", "highlight": "All US States"},
            {"name": "Bybit", "slug": "bybit", "rating": 4.6, "reason": "Copy trading lets beginners follow expert traders. Great mobile app with simplified view.", "highlight": "Copy Trading"},
        ],
        "what_to_look_for": [
            ("Simple Interface", "Beginners need a clean, uncluttered interface. Advanced features should be optional, not in your face."),
            ("Low Minimum Deposits", "You should be able to start with $10-50. Exchanges requiring large minimums are not beginner-friendly."),
            ("Educational Resources", "The best exchanges teach you while you trade — with guides, tutorials, and learn-to-earn programs."),
            ("Strong Security", "As a beginner, you are more vulnerable to scams. Choose exchanges with robust 2FA, insurance, and regulatory oversight."),
            ("Fiat On-Ramp", "Being able to buy crypto directly with a debit card or bank transfer is essential for beginners."),
        ],
    },
    {
        "slug": "best-crypto-casino-high-rollers",
        "title": "Best Crypto Casinos for High Rollers in 2026",
        "meta_title": "Best Crypto Casinos for High Rollers 2026 - VIP & High Limits | Cryptosites",
        "description": "Top crypto casinos for high rollers in 2026. Highest deposit limits, best VIP programs, and biggest welcome bonuses for serious players.",
        "hero_sub": "If you play big, you need a platform that can handle it. These crypto casinos offer the highest limits, best VIP programs, and most generous rewards for high-volume players.",
        "rankings": [
            {"name": "Stake", "slug": "stake-casino", "rating": 4.9, "reason": "Industry-leading VIP program with personal account managers, custom bonuses, and $100,000 welcome package.", "highlight": "$100K Welcome"},
            {"name": "Cloudbet", "slug": "cloudbet-casino", "rating": 4.7, "reason": "Highest betting limits in crypto. No traditional wagering — loyalty points system rewards volume.", "highlight": "Highest Limits"},
            {"name": "FortuneJack", "slug": "fortunejack", "rating": 4.5, "reason": "6 BTC welcome bonus with just 30x wagering. Biggest bonus value for high-value first deposits.", "highlight": "6 BTC Bonus"},
            {"name": "Wild.io", "slug": "wild-io", "rating": 4.4, "reason": "10 BTC welcome package. One of the highest bonus ceilings in the industry.", "highlight": "10 BTC Package"},
            {"name": "BC.Game", "slug": "bc-game-casino", "rating": 4.8, "reason": "360% deposit bonus and active VIP program with daily rewards. Good for consistent high-volume play.", "highlight": "360% Bonus"},
        ],
        "what_to_look_for": [
            ("High Deposit/Bet Limits", "The platform should support five and six-figure bets without restrictions."),
            ("VIP Program Quality", "Look for personal account managers, custom bonuses, faster withdrawals, and exclusive events."),
            ("Withdrawal Speed", "When you win big, you need your money fast. Best VIP programs offer priority withdrawal processing."),
            ("Welcome Bonus Ceiling", "A 100% match means nothing if the cap is 0.1 BTC. High rollers need high bonus ceilings."),
            ("Privacy", "Many high rollers prefer anonymous play. Check KYC requirements for large transactions."),
        ],
    },
    {
        "slug": "best-crypto-casino-privacy",
        "title": "Best Anonymous Crypto Casinos for Privacy in 2026",
        "meta_title": "Best Anonymous Crypto Casinos 2026 - No KYC Required | Cryptosites",
        "description": "The best anonymous crypto casinos that require no KYC. Play with Bitcoin and other cryptos privately. Privacy-focused casino reviews.",
        "hero_sub": "For players who value their privacy, these crypto casinos allow anonymous play with minimal or no personal information required.",
        "rankings": [
            {"name": "Stake", "slug": "stake-casino", "rating": 4.9, "reason": "No KYC for crypto deposits under reasonable limits. Play with just an email address.", "highlight": "Email Only"},
            {"name": "BC.Game", "slug": "bc-game-casino", "rating": 4.8, "reason": "Register with just username and password. 150+ crypto options for anonymous deposits.", "highlight": "Username Only"},
            {"name": "FortuneJack", "slug": "fortunejack", "rating": 4.5, "reason": "Accepts privacy coins (Monero, Zcash). One of the few casinos supporting truly private transactions.", "highlight": "Privacy Coins"},
            {"name": "Wild.io", "slug": "wild-io", "rating": 4.4, "reason": "Minimal signup. Focus on crypto-native users who value anonymity.", "highlight": "Minimal KYC"},
            {"name": "mBit Casino", "slug": "mbit-casino", "rating": 4.6, "reason": "Email-only registration. Quick crypto deposits without identity verification.", "highlight": "No Verification"},
        ],
        "what_to_look_for": [
            ("Registration Requirements", "The less information required, the better. Look for email-only or even username-only registration."),
            ("KYC Triggers", "Even 'no-KYC' casinos may require verification for large withdrawals. Understand the thresholds."),
            ("Privacy Coin Support", "Monero (XMR) and Zcash (ZEC) offer transaction-level privacy that Bitcoin cannot match."),
            ("Data Handling", "Check the privacy policy. Does the casino share data with third parties? Do they log IP addresses?"),
            ("VPN Policy", "Some casinos ban VPN usage. Privacy-focused platforms should explicitly allow VPN connections."),
        ],
    },
    {
        "slug": "best-crypto-exchange-low-fees",
        "title": "Lowest Fee Crypto Exchanges in 2026",
        "meta_title": "Lowest Fee Crypto Exchanges 2026 - Cheapest Trading | Cryptosites",
        "description": "Compare the cheapest crypto exchanges for trading in 2026. Trading fees, withdrawal fees, and hidden costs compared side by side.",
        "hero_sub": "Fees eat into your profits. These exchanges offer the lowest trading and withdrawal costs in the crypto industry.",
        "rankings": [
            {"name": "Binance", "slug": "binance", "rating": 4.6, "reason": "0.10% maker/taker — the lowest standard fees in the industry. Even cheaper with BNB payment.", "highlight": "0.10% Fees"},
            {"name": "KuCoin", "slug": "kucoin", "rating": 4.5, "reason": "0.10% base fees with further discounts via KCS token. Best value for altcoin trading.", "highlight": "0.10% + KCS Discount"},
            {"name": "Bybit", "slug": "bybit", "rating": 4.6, "reason": "0.10% spot fees, competitive derivatives fees. Strong fee discounts for volume traders.", "highlight": "Volume Discounts"},
            {"name": "OKX", "slug": "okx", "rating": 4.5, "reason": "0.08% maker / 0.10% taker. Among the cheapest for high-volume trading.", "highlight": "0.08% Maker"},
            {"name": "Kraken", "slug": "kraken", "rating": 4.8, "reason": "0.16% maker / 0.26% taker. Higher than Binance but offset by free withdrawals and superior security.", "highlight": "Free Withdrawals"},
        ],
        "what_to_look_for": [
            ("Trading Fees", "Maker/taker fees are the primary cost. Look for 0.10% or lower. Even small differences compound significantly over time."),
            ("Withdrawal Fees", "Low trading fees can be offset by high withdrawal fees. Always check withdrawal costs for the cryptos you use most."),
            ("Token Discounts", "Many exchanges offer fee discounts when you pay with their native token (BNB, KCS, OKB). This can save 20-25%."),
            ("Volume Tiers", "Higher trading volume usually unlocks lower fees. Check the tier structure if you are an active trader."),
            ("Spread", "The bid-ask spread is a hidden cost. High-liquidity exchanges like Binance have tighter spreads, meaning better prices."),
        ],
    },
]

def generate_buyers_guide(guide):
    rankings_html = ""
    for i, r in enumerate(guide["rankings"], 1):
        rankings_html += f"""
      <div class="bg-rank-card">
        <div class="bg-rank-number">#{i}</div>
        <div class="bg-rank-content">
          <div class="bg-rank-header">
            <h3><a href="./promo-{r['slug']}.html">{r['name']}</a></h3>
            <div class="bg-rank-meta">
              <span class="bg-rating">{r['rating']}/5</span>
              <span class="bg-highlight">{r['highlight']}</span>
            </div>
          </div>
          <p>{r['reason']}</p>
          <a href="./promo-{r['slug']}.html" class="btn btn-sm btn-accent">Get Promo Code &rarr;</a>
        </div>
      </div>"""

    criteria_html = ""
    for title, desc in guide["what_to_look_for"]:
        criteria_html += f"""
      <div class="criteria-item">
        <h3>{title}</h3>
        <p>{desc}</p>
      </div>"""

    body = f"""
<section class="content-hero">
  <div class="container container-narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="./index.html">Home</a> <span class="bc-sep">/</span> <a href="./how-we-rate.html">Resources</a> <span class="bc-sep">/</span> <span>{guide['title'].split(' in ')[0]}</span>
    </nav>
    <h1>{guide['title']}</h1>
    <p class="content-hero-sub">{guide['hero_sub']}</p>
    <div class="content-meta">
      <span class="meta-badge">Buyer's Guide</span>
      <span class="meta-date">Updated: {NOW}</span>
      <span class="meta-author">By the Cryptosites Review Team</span>
    </div>
  </div>
</section>

<section class="content-body">
  <div class="container container-narrow">

    <h2>Our Top Picks</h2>
    <p>Ranked based on our <a href="./how-we-rate.html">10-category scoring system</a>, with extra weight given to factors most relevant to this category.</p>

    <div class="bg-rankings">
{rankings_html}
    </div>

    <h2>What to Look For</h2>
    <div class="criteria-grid">
{criteria_html}
    </div>

    <h2>How We Chose These</h2>
    <p>Every platform on this list has been personally tested by our team for a minimum of 2 weeks. We use real accounts with real deposits. Our scoring is transparent — see our full <a href="./how-we-rate.html">methodology page</a> for the complete breakdown.</p>
    <p>Rankings are updated quarterly based on re-testing. Scores can go up or down based on platform changes, new security incidents, or shifts in market standards.</p>

    <div class="cta-box">
      <h3>View All Reviews</h3>
      <p>See our complete category rankings with detailed scores across all 10 rating categories.</p>
      <a href="./{'crypto-casinos.html' if 'casino' in guide['slug'].lower() else 'crypto-exchanges.html'}" class="btn btn-accent">View Full Rankings</a>
    </div>

  </div>
</section>"""

    return page_shell(
        guide["meta_title"],
        guide["description"],
        f"{guide['slug']}.html",
        "",
        body
    )


# ============================================================
# CSS ADDITIONS
# ============================================================
def get_new_css():
    return """

/* ============================================
   CONTENT PAGES — SHARED STYLES
   ============================================ */

/* Content Hero */
.content-hero {
  padding: var(--space-16) 0 var(--space-12);
  background: var(--hero-gradient);
  position: relative;
}
.content-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--hero-glow);
  pointer-events: none;
}
.content-hero h1 {
  font-size: var(--text-3xl);
  margin-bottom: var(--space-4);
}
.content-hero-sub {
  font-size: var(--text-lg);
  color: var(--text-secondary);
  max-width: 640px;
  line-height: 1.7;
}
.content-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  align-items: center;
  margin-top: var(--space-6);
}
.meta-badge {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: var(--accent-muted);
  color: var(--accent);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 600;
}
.meta-badge-danger {
  background: rgba(255, 87, 87, 0.15);
  color: var(--error);
}
.meta-date,
.meta-author {
  font-size: var(--text-sm);
  color: var(--text-muted);
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
  font-size: var(--text-sm);
}
.breadcrumb a {
  color: var(--text-muted);
}
.breadcrumb a:hover {
  color: var(--accent);
}
.bc-sep {
  color: var(--text-faint);
  font-size: var(--text-xs);
}

/* Content Body */
.content-body {
  padding: var(--space-12) 0 var(--space-16);
}
.content-body h2 {
  font-size: var(--text-2xl);
  margin-top: var(--space-12);
  margin-bottom: var(--space-6);
  padding-top: var(--space-6);
  border-top: 1px solid var(--border);
}
.content-body h2:first-child {
  margin-top: 0;
  border-top: none;
  padding-top: 0;
}
.content-body h3 {
  font-size: var(--text-xl);
  margin-bottom: var(--space-3);
}
.content-body p {
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: var(--space-4);
}
.content-body p:last-child {
  margin-bottom: 0;
}
.content-body strong {
  color: var(--text-primary);
}
.content-list {
  padding-left: var(--space-6);
  margin-bottom: var(--space-6);
}
.content-list li {
  position: relative;
  padding-left: var(--space-2);
  margin-bottom: var(--space-3);
  color: var(--text-secondary);
  line-height: 1.7;
  list-style: disc;
}

/* Card Elevated */
.card-elevated {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  margin-bottom: var(--space-8);
}

/* Methodology Intro */
.methodology-intro {
  border-left: 3px solid var(--accent);
}

/* Rating Categories Grid */
.rating-categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}
.rating-category-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  transition: border-color var(--duration-normal) var(--ease-out);
}
.rating-category-card:hover {
  border-color: var(--border-hover);
}
.rc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}
.rc-icon svg {
  width: 28px;
  height: 28px;
  color: var(--accent);
}
.rc-weight {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 800;
  color: var(--accent);
}
.rc-checklist {
  margin-top: var(--space-4);
  padding-left: 0;
}
.rc-checklist li {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  border-bottom: 1px solid var(--border);
  list-style: none;
}
.rc-checklist li:last-child {
  border-bottom: none;
}
.rc-checklist li::before {
  content: '\\2713';
  color: var(--accent);
  font-weight: 700;
  flex-shrink: 0;
}

/* Process Timeline */
.process-timeline {
  margin: var(--space-6) 0 var(--space-8);
  position: relative;
  padding-left: var(--space-10);
}
.process-timeline::before {
  content: '';
  position: absolute;
  left: 18px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border);
}
.process-step {
  position: relative;
  margin-bottom: var(--space-8);
}
.process-step:last-child {
  margin-bottom: 0;
}
.ps-number {
  position: absolute;
  left: calc(-1 * var(--space-10) + 6px);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent);
  color: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: var(--text-sm);
  z-index: 1;
}
.ps-content h3 {
  margin-bottom: var(--space-2);
}
.ps-content p {
  color: var(--text-secondary);
  line-height: 1.7;
}

/* Score Guide */
.score-guide {
  margin: var(--space-6) 0;
}
.sg-row {
  display: grid;
  grid-template-columns: 100px 100px 1fr;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-2);
  align-items: center;
}
.sg-score {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: var(--text-lg);
}
.sg-label {
  font-weight: 600;
  font-size: var(--text-sm);
}
.sg-desc {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  margin-bottom: 0;
}
.sg-excellent { background: rgba(0, 212, 170, 0.08); }
.sg-excellent .sg-score { color: var(--accent); }
.sg-good { background: rgba(0, 212, 170, 0.05); }
.sg-good .sg-score { color: var(--accent); }
.sg-decent { background: rgba(247, 183, 49, 0.08); }
.sg-decent .sg-score { color: var(--secondary); }
.sg-fair { background: rgba(247, 183, 49, 0.05); }
.sg-fair .sg-score { color: var(--secondary); }
.sg-poor { background: rgba(255, 87, 87, 0.08); }
.sg-poor .sg-score { color: var(--error); }

/* Commitments Grid */
.commitments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
  margin: var(--space-6) 0;
}
.commitment-card {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
}
.commitment-icon {
  color: var(--error);
  font-size: var(--text-xl);
  font-weight: 700;
  flex-shrink: 0;
  line-height: 1;
}
.commitment-card p {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  margin: 0;
  line-height: 1.6;
}

/* CTA Box */
.cta-box {
  background: var(--bg-surface);
  border: 1px solid var(--accent-muted);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  margin-top: var(--space-10);
  text-align: center;
}
.cta-box h3 {
  margin-bottom: var(--space-3);
}
.cta-box p {
  max-width: 500px;
  margin: 0 auto var(--space-6);
  color: var(--text-secondary);
}
.cta-box-warning {
  border-color: rgba(255, 87, 87, 0.2);
}
.cta-buttons {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  flex-wrap: wrap;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: var(--text-sm);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-out);
  cursor: pointer;
}
.btn-accent {
  background: var(--accent);
  color: var(--bg-primary);
}
.btn-accent:hover {
  background: var(--accent-hover);
  color: var(--bg-primary);
}
.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-primary);
}
.btn-outline:hover {
  border-color: var(--accent);
  color: var(--accent);
}
.btn-sm {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-xs);
}

/* ============================================
   WARNINGS PAGE
   ============================================ */
.warning-alert {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
  background: rgba(255, 87, 87, 0.08);
  border: 1px solid rgba(255, 87, 87, 0.2);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
}
.warning-alert-icon {
  width: 24px;
  height: 24px;
  color: var(--error);
  flex-shrink: 0;
  margin-top: 2px;
}
.warning-alert strong {
  color: var(--error);
}

/* Red Flags Grid */
.red-flags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-5);
  margin: var(--space-6) 0 var(--space-8);
}
.red-flag-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  border-top: 3px solid var(--error);
}
.rf-icon {
  font-size: var(--text-2xl);
  margin-bottom: var(--space-3);
  color: var(--error);
}

/* Blacklist */
.blacklist-table {
  margin: var(--space-6) 0;
}
.bl-item {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
  overflow: hidden;
}
.bl-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-5) var(--space-6);
  gap: var(--space-4);
}
.bl-name {
  font-weight: 700;
  font-size: var(--text-base);
}
.bl-status {
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}
.bl-status-scam {
  background: rgba(255, 87, 87, 0.15);
  color: var(--error);
}
.bl-status-danger {
  background: rgba(247, 183, 49, 0.15);
  color: var(--secondary);
}
.bl-details {
  padding: 0 var(--space-6) var(--space-5);
  border-top: 1px solid var(--border);
}
.bl-details p {
  margin-top: var(--space-3);
}

/* Protection Checklist */
.protection-checklist {
  margin: var(--space-6) 0;
}
.pc-item {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
  padding: var(--space-5) 0;
  border-bottom: 1px solid var(--border);
}
.pc-item:last-child {
  border-bottom: none;
}
.pc-check {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent-muted);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: var(--text-sm);
  flex-shrink: 0;
}

/* ============================================
   GUIDE PAGES
   ============================================ */

/* Tables */
.guide-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--space-4) 0 var(--space-6);
  font-size: var(--text-sm);
}
.guide-table thead th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  background: var(--bg-surface-2);
  border-bottom: 2px solid var(--border);
  font-weight: 700;
  color: var(--text-primary);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.guide-table tbody td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--border);
  color: var(--text-secondary);
}
.guide-table tbody tr:hover {
  background: var(--bg-surface);
}
.td-yes {
  color: var(--accent) !important;
  font-weight: 600;
}
.td-no {
  color: var(--error) !important;
  font-weight: 600;
}
.td-partial {
  color: var(--secondary) !important;
  font-weight: 600;
}

.comparison-mini {
  overflow-x: auto;
  margin: var(--space-4) 0 var(--space-6);
  -webkit-overflow-scrolling: touch;
}

/* Tips Grid */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-5);
  margin: var(--space-6) 0 var(--space-8);
}
.tip-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
.tip-card h3 {
  color: var(--accent);
  margin-bottom: var(--space-3);
  font-size: var(--text-base);
}

/* ============================================
   BUYER'S GUIDE PAGES
   ============================================ */
.bg-rankings {
  margin: var(--space-6) 0;
}
.bg-rank-card {
  display: flex;
  gap: var(--space-6);
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-4);
  transition: border-color var(--duration-normal) var(--ease-out);
}
.bg-rank-card:hover {
  border-color: var(--border-hover);
}
.bg-rank-number {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
  flex-shrink: 0;
  min-width: 48px;
}
.bg-rank-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
  flex-wrap: wrap;
  gap: var(--space-3);
}
.bg-rank-header h3 {
  margin-bottom: 0;
}
.bg-rank-meta {
  display: flex;
  gap: var(--space-3);
  align-items: center;
}
.bg-rating {
  font-weight: 700;
  color: var(--secondary);
  font-size: var(--text-sm);
}
.bg-highlight {
  padding: var(--space-1) var(--space-3);
  background: var(--accent-muted);
  color: var(--accent);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
}
.bg-rank-content p {
  margin-bottom: var(--space-4);
}

/* Criteria Grid */
.criteria-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
  margin: var(--space-6) 0;
}
.criteria-item {
  padding: var(--space-5);
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--accent);
}
.criteria-item h3 {
  font-size: var(--text-base);
  margin-bottom: var(--space-2);
}
.criteria-item p {
  margin: 0;
  font-size: var(--text-sm);
}

/* ============================================
   RESPONSIVE — CONTENT PAGES
   ============================================ */
@media (max-width: 768px) {
  .content-hero {
    padding: var(--space-10) 0 var(--space-8);
  }
  .content-hero h1 {
    font-size: var(--text-2xl);
  }
  .rating-categories-grid {
    grid-template-columns: 1fr;
  }
  .sg-row {
    grid-template-columns: 80px 70px 1fr;
    gap: var(--space-2);
    padding: var(--space-3);
  }
  .commitments-grid {
    grid-template-columns: 1fr;
  }
  .red-flags-grid {
    grid-template-columns: 1fr;
  }
  .tips-grid {
    grid-template-columns: 1fr;
  }
  .bg-rank-card {
    flex-direction: column;
    gap: var(--space-3);
  }
  .bg-rank-number {
    font-size: var(--text-2xl);
  }
  .bl-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-2);
  }
  .process-timeline {
    padding-left: var(--space-8);
  }
  .ps-number {
    left: calc(-1 * var(--space-8) + 4px);
    width: 24px;
    height: 24px;
    font-size: var(--text-xs);
  }
  .process-timeline::before {
    left: 14px;
  }
  .guide-table {
    font-size: var(--text-xs);
  }
  .guide-table thead th,
  .guide-table tbody td {
    padding: var(--space-2) var(--space-3);
  }
}
"""


# ============================================================
# UPDATE EXISTING PAGES — Nav + Footer
# ============================================================
def update_existing_pages():
    """Update nav links and footer on ALL existing HTML pages."""
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]

    # Old nav patterns to replace
    old_nav_pattern = re.compile(
        r'<a href="\./index\.html"[^>]*>Home</a>\s*'
        r'<a href="\./crypto-casinos\.html"[^>]*>Casinos</a>\s*'
        r'<a href="\./crypto-sports-betting\.html"[^>]*>Sports Betting</a>\s*'
        r'<a href="\./crypto-poker\.html"[^>]*>Poker</a>\s*'
        r'<a href="\./crypto-exchanges\.html"[^>]*>Exchanges</a>\s*'
        r'<a href="\./crypto-lottery\.html"[^>]*>Lottery</a>\s*'
        r'<a href="\./crypto-wallets\.html"[^>]*>Wallets</a>',
        re.DOTALL
    )

    updated_count = 0
    for fname in html_files:
        fpath = os.path.join(BASE_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Determine active nav based on filename
        active = ""
        if fname == "index.html": active = "home"
        elif "casinos" in fname and not fname.startswith("best-"): active = "casinos"
        elif "sports" in fname and not fname.startswith("best-"): active = "sports"
        elif "poker" in fname: active = "poker"
        elif "exchanges" in fname and not fname.startswith("best-"): active = "exchanges"
        elif "lottery" in fname: active = "lottery"
        elif "wallets" in fname and not fname.startswith("best-"): active = "wallets"
        elif "how-we-rate" in fname: active = "rate"

        nav = get_nav(active)
        content = old_nav_pattern.sub(nav, content)

        # Update footer — replace everything between <footer> and </footer>
        new_footer = FOOTER.format(logo=LOGO_SVG, now=NOW)
        footer_pattern = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)
        if footer_pattern.search(content):
            content = footer_pattern.sub(new_footer, content)

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1

    return updated_count


# ============================================================
# SITEMAP
# ============================================================
def generate_sitemap():
    html_files = sorted([f for f in os.listdir(BASE_DIR) if f.endswith('.html')])
    entries = []
    for f in html_files:
        priority = "1.0" if f == "index.html" else "0.9" if f.startswith("crypto-") else "0.8" if f.startswith("how-we-rate") or f.startswith("warnings") else "0.7" if f.startswith("guide-") or f.startswith("best-") else "0.6"
        entries.append(f'  <url><loc>https://cryptosites.com/{f}</loc><lastmod>2026-03-15</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>')

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>"""


# ============================================================
# MAIN
# ============================================================
def main():
    pages_created = []

    # 1. How We Rate
    html = generate_how_we_rate()
    path = os.path.join(BASE_DIR, "how-we-rate.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    pages_created.append("how-we-rate.html")
    print(f"  Created: how-we-rate.html")

    # 2. Warnings
    html = generate_warnings()
    path = os.path.join(BASE_DIR, "warnings.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    pages_created.append("warnings.html")
    print(f"  Created: warnings.html")

    # 3. Educational Guides
    for guide in GUIDES:
        html = generate_guide(guide)
        fname = f"{guide['slug']}.html"
        path = os.path.join(BASE_DIR, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        pages_created.append(fname)
        print(f"  Created: {fname}")

    # 4. Buyer's Guides
    for guide in BUYERS_GUIDES:
        html = generate_buyers_guide(guide)
        fname = f"{guide['slug']}.html"
        path = os.path.join(BASE_DIR, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        pages_created.append(fname)
        print(f"  Created: {fname}")

    # 5. Append new CSS
    css_path = os.path.join(BASE_DIR, "style.css")
    new_css = get_new_css()
    with open(css_path, 'r', encoding='utf-8') as f:
        existing_css = f.read()

    if "CONTENT PAGES" not in existing_css:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(new_css)
        print(f"  Updated: style.css (+{len(new_css)} chars)")
    else:
        print(f"  Skipped: style.css (content page styles already present)")

    # 6. Update existing pages (nav + footer)
    updated = update_existing_pages()
    print(f"  Updated nav/footer on {updated} existing pages")

    # 7. Regenerate sitemap
    sitemap = generate_sitemap()
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f"  Regenerated: sitemap.xml")

    print(f"\nDone! Created {len(pages_created)} new pages:")
    for p in pages_created:
        print(f"  - {p}")


if __name__ == "__main__":
    main()

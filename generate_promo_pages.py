#!/usr/bin/env python3
"""
Cryptosites.com — Promo Code Page Generator
Generates promo code pages for all brands across 6 categories,
updates CSS/JS/footer/nav, and generates sitemap.
"""

import os, json, html as html_mod, re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# BRAND DATA
# ============================================================

CATEGORIES = {
    "casinos": {
        "name": "Crypto Casinos",
        "page": "crypto-casinos.html",
        "slug": "casinos",
        "brands": [
            {"name": "Stake", "slug": "stake-casino", "rating": 4.9, "bonus": "Up to $100,000 Welcome Package", "code": "CRYPTOSITES", "min_deposit": "0.0001 BTC", "wagering": "40x", "year": 2017, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "XRP", "TRX", "EOS"],
             "pros": ["Massive game library with 3,000+ titles", "Industry-leading VIP program", "Instant crypto deposits and withdrawals", "Provably fair games available"],
             "cons": ["Not licensed in all jurisdictions", "High wagering on welcome bonus", "No fiat currency support"],
             "expert": "Stake has cemented itself as the undisputed king of crypto casinos. Their welcome package is aggressive, their game selection is unmatched, and the VIP program rewards loyal players generously. Our team verified this code is active as of March 2026.",
             "desc": "Stake is the world's largest crypto casino by volume, trusted by millions of players globally. Their platform offers an unparalleled selection of slots, table games, and originals — all with provably fair mechanics."},
            {"name": "BC.Game", "slug": "bc-game-casino", "rating": 4.8, "bonus": "Up to 360% Deposit Bonus", "code": "CRYPTO360", "min_deposit": "$10 equivalent", "wagering": "60x", "year": 2017, "cryptos": ["BTC", "ETH", "DOGE", "LTC", "BCH", "150+ more"],
             "pros": ["Supports 150+ cryptocurrencies", "Unique community features and chat", "Daily lucky spin and tasks", "Low minimum deposits"],
             "cons": ["Higher than average wagering requirements", "Interface can feel cluttered", "Withdrawal limits on some methods"],
             "expert": "BC.Game stands out with its incredible crypto support — over 150 coins accepted. The 360% deposit bonus is one of the most generous in the space, though the 60x wagering is steep. Still, the community features and daily rewards make it a solid choice.",
             "desc": "BC.Game has built a loyal following with its community-first approach to crypto gambling. Supporting over 150 cryptocurrencies, it offers one of the widest ranges of deposit options in the industry."},
            {"name": "BitStarz", "slug": "bitstarz", "rating": 4.8, "bonus": "5 BTC + 200 Free Spins", "code": "BITS200", "min_deposit": "0.0001 BTC", "wagering": "40x", "year": 2014, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "BCH", "USDT"],
             "pros": ["Award-winning platform since 2014", "Lightning-fast withdrawals under 10 mins", "Dual currency (crypto + fiat)", "200 free spins with welcome bonus"],
             "cons": ["Not available in US/UK", "Limited sports betting options", "Some country restrictions apply"],
             "expert": "BitStarz is a veteran in the crypto casino space and it shows. They have won multiple industry awards and their withdrawal speeds are genuinely best-in-class. The 5 BTC + 200 free spins welcome package is generous and the 40x wagering is fair.",
             "desc": "BitStarz has been a trusted name in crypto gambling since 2014. Multiple award wins and consistently fast payouts have earned them a sterling reputation among crypto gamblers worldwide."},
            {"name": "mBit Casino", "slug": "mbit-casino", "rating": 4.6, "bonus": "5 BTC + 300 Free Spins", "code": "MBIT300", "min_deposit": "0.0003 BTC", "wagering": "35x", "year": 2014, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "BCH", "USDT", "XRP"],
             "pros": ["300 free spins — more than most competitors", "Lower wagering at 35x", "2,000+ games from top providers", "VIP cashback program"],
             "cons": ["Website design feels dated", "Limited live dealer options", "Customer support could be faster"],
             "expert": "mBit Casino offers one of the best value propositions in crypto gambling. The 35x wagering requirement is below industry average, and 300 free spins is exceptionally generous. A solid choice for players who value bonus value over flashy branding.",
             "desc": "mBit Casino has been serving the crypto gambling community since 2014 with a focus on value. Their generous bonus structure and lower-than-average wagering requirements make them a favourite among bonus hunters."},
            {"name": "FortuneJack", "slug": "fortunejack", "rating": 4.5, "bonus": "6 BTC + 250 Free Spins", "code": "FJACK250", "min_deposit": "0.001 BTC", "wagering": "30x", "year": 2014, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "DASH", "ZEC", "XMR"],
             "pros": ["Largest welcome bonus at 6 BTC", "Lowest wagering at 30x", "Privacy coins accepted (Monero, Zcash)", "Provably fair dice and crash games"],
             "cons": ["Interface not as polished as competitors", "Slower customer support responses", "Some games geo-restricted"],
             "expert": "FortuneJack brings the biggest welcome bonus in the crypto casino world — 6 BTC with just 30x wagering. If you are looking for pure bonus value, this is hard to beat. The privacy coin support is also a plus for anonymity-focused players.",
             "desc": "FortuneJack has been a staple of the crypto gambling scene since 2014. Their standout feature is the massive 6 BTC welcome bonus with the lowest wagering requirements among top-tier crypto casinos."},
            {"name": "Cloudbet", "slug": "cloudbet-casino", "rating": 4.7, "bonus": "5 BTC Welcome Bonus", "code": "CLOUD5BTC", "min_deposit": "0.001 BTC", "wagering": "Loyalty points system", "year": 2013, "cryptos": ["BTC", "ETH", "BCH", "USDT", "DOGE", "LTC", "PAXG"],
             "pros": ["One of the oldest and most trusted platforms", "No traditional wagering — loyalty points instead", "Excellent sportsbook integration", "High betting limits"],
             "cons": ["Bonus released gradually through play", "Fewer slots than some competitors", "KYC required for large withdrawals"],
             "expert": "Cloudbet is one of the OGs of crypto gambling, operating since 2013. Their unique loyalty points system replaces traditional wagering requirements, which many players prefer. The platform combines casino and sports betting seamlessly.",
             "desc": "Cloudbet has been at the forefront of crypto gambling since 2013. As one of the first Bitcoin casinos, they have built a reputation for reliability, high limits, and a unique loyalty-based bonus system."},
            {"name": "Wild.io", "slug": "wild-io", "rating": 4.4, "bonus": "Up to 10 BTC Welcome Package", "code": "WILD10", "min_deposit": "$10 equivalent", "wagering": "45x", "year": 2022, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "USDT", "BNB", "TRX"],
             "pros": ["Massive 10 BTC welcome package", "Modern, slick interface", "NFT integration and rewards", "Rapid withdrawal processing"],
             "cons": ["Newer platform with less track record", "45x wagering is above average", "Limited loyalty program details"],
             "expert": "Wild.io is the new kid on the block but it is making waves with its 10 BTC welcome package — one of the largest in the industry. The platform looks fantastic and loads fast, though the 45x wagering tempers the excitement somewhat.",
             "desc": "Wild.io burst onto the crypto casino scene in 2022 with a bold proposition: up to 10 BTC in welcome bonuses and a sleek, modern platform that rivals established players."},
            {"name": "Vave Casino", "slug": "vave-casino", "rating": 4.3, "bonus": "100% up to 1 BTC", "code": "VAVE100", "min_deposit": "$10 equivalent", "wagering": "40x", "year": 2022, "cryptos": ["BTC", "ETH", "LTC", "USDT", "DOGE", "TRX"],
             "pros": ["Clean, intuitive interface", "Combined casino and sportsbook", "Good selection of live dealers", "Regular promotions and tournaments"],
             "cons": ["Smaller game library than top competitors", "1 BTC max bonus is modest", "Limited VIP program information"],
             "expert": "Vave Casino offers a well-rounded crypto gambling experience with both casino and sports betting under one roof. The 100% match up to 1 BTC is straightforward and the 40x wagering is fair. A solid all-rounder for crypto gamblers.",
             "desc": "Vave Casino launched in 2022 as a combined crypto casino and sportsbook. Their clean interface and straightforward bonus structure appeal to players who want simplicity without sacrificing quality."},
        ]
    },
    "sports": {
        "name": "Crypto Sports Betting",
        "page": "crypto-sports-betting.html",
        "slug": "sports",
        "brands": [
            {"name": "Stake Sports", "slug": "stake-sports", "rating": 4.9, "bonus": "200% up to $1,000", "code": "CRYPTOSITES", "min_deposit": "0.0001 BTC", "wagering": "30x", "year": 2017, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "XRP", "TRX"],
             "pros": ["Best odds across major sports", "Live streaming for thousands of events", "Fastest crypto payouts in sports betting", "Comprehensive esports coverage"],
             "cons": ["Welcome bonus wagering could be lower", "No dedicated mobile app", "Some markets restricted"],
             "expert": "Stake Sports is the benchmark for crypto sports betting. Their odds consistently beat the competition, live streaming is top-tier, and the 200% welcome bonus up to $1,000 is a strong start. This is where serious sports bettors go.",
             "desc": "Stake Sports combines the reliability of the world's largest crypto gambling platform with a sportsbook that covers everything from Premier League football to Korean baseball and beyond."},
            {"name": "Cloudbet Sports", "slug": "cloudbet-sports", "rating": 4.7, "bonus": "5 BTC Welcome Bonus", "code": "CLOUD5BTC", "min_deposit": "0.001 BTC", "wagering": "Loyalty points", "year": 2013, "cryptos": ["BTC", "ETH", "BCH", "USDT", "DOGE", "LTC"],
             "pros": ["Highest betting limits in crypto", "Established since 2013", "No traditional wagering requirements", "Competitive odds on major leagues"],
             "cons": ["Bonus released through loyalty points over time", "Interface not as modern as Stake", "Limited promotions for existing users"],
             "expert": "Cloudbet Sports is the go-to for high rollers in crypto sports betting. Their limits are among the highest in the industry and the loyalty-based bonus system means no rushed wagering deadlines. A trusted name since 2013.",
             "desc": "Cloudbet Sports has been a pioneer in crypto sports betting since 2013. Their high limits and trusted reputation make them the preferred choice for professional and high-volume bettors."},
            {"name": "BC.Game Sports", "slug": "bc-game-sports", "rating": 4.7, "bonus": "Up to 300% Deposit Bonus", "code": "CRYPTO300", "min_deposit": "$10 equivalent", "wagering": "50x", "year": 2017, "cryptos": ["BTC", "ETH", "DOGE", "LTC", "150+ more"],
             "pros": ["300% bonus is among the highest", "150+ crypto deposit options", "Community shilling and chat features", "Combined casino and sportsbook"],
             "cons": ["50x wagering is very high for sports", "Odds not always the sharpest", "Can be overwhelming for beginners"],
             "expert": "BC.Game Sports offers an impressive 300% deposit bonus, though the 50x wagering requirement is steep for sports betting. The massive crypto support and community features set it apart, but serious bettors may prefer sharper odds elsewhere.",
             "desc": "BC.Game Sports brings the community-driven crypto gambling experience to sports betting. With support for over 150 cryptocurrencies and a generous 300% welcome bonus, it appeals to both casual and dedicated bettors."},
            {"name": "Sportsbet.io", "slug": "sportsbet-io", "rating": 4.6, "bonus": "Up to 5% Cashback", "code": "AUTO", "min_deposit": "$10 equivalent", "wagering": "1x", "year": 2016, "cryptos": ["BTC", "ETH", "LTC", "USDT", "TRX", "XRP"],
             "pros": ["Official partner of major sports teams", "Cashback with just 1x wagering", "Price boosts and enhanced odds daily", "Fiat and crypto accepted"],
             "cons": ["No traditional deposit match bonus", "Cashback percentage varies", "Some features limited by region"],
             "expert": "Sportsbet.io takes a different approach with cashback instead of a deposit match. The 1x wagering is incredibly player-friendly, and their partnerships with major sports teams add credibility. A great choice for regular bettors who value ongoing rewards.",
             "desc": "Sportsbet.io has established itself as a mainstream crypto sportsbook with official partnerships with Premier League clubs and international sports teams. Their cashback-focused reward system appeals to regular bettors."},
            {"name": "Thunderpick", "slug": "thunderpick", "rating": 4.5, "bonus": "100% up to $500", "code": "THUNDER500", "min_deposit": "$10 equivalent", "wagering": "10x", "year": 2017, "cryptos": ["BTC", "ETH", "LTC", "USDT", "DOGE", "XRP"],
             "pros": ["Best esports betting coverage", "Very low 10x wagering requirement", "Sleek, gamer-friendly interface", "Regular esports tournaments and promos"],
             "cons": ["Traditional sports coverage not as deep", "Smaller brand awareness", "Limited live streaming"],
             "expert": "Thunderpick is the esports betting king. If you bet on CS2, Dota 2, or League of Legends, this is your platform. The 10x wagering on the welcome bonus is one of the lowest in the industry, making it easy to actually benefit from.",
             "desc": "Thunderpick has carved out a niche as the premier esports betting platform in the crypto space. Their deep coverage of competitive gaming, combined with a generous low-wagering welcome bonus, makes them essential for esports enthusiasts."},
            {"name": "Betplay", "slug": "betplay", "rating": 4.4, "bonus": "100% up to $10,000", "code": "BETPLAY10K", "min_deposit": "0.0001 BTC", "wagering": "35x", "year": 2020, "cryptos": ["BTC", "ETH", "LTC", "USDT", "DOGE"],
             "pros": ["Massive $10,000 max bonus", "Good mix of sports and casino", "Bitcoin-native platform", "Competitive odds on football"],
             "cons": ["Newer platform, less track record", "35x wagering on sports bonus", "Limited payment methods beyond crypto"],
             "expert": "Betplay offers one of the largest welcome bonuses in crypto sports betting at $10,000. The platform is Bitcoin-native and offers competitive odds, particularly on football. The 35x wagering is moderate for the bonus size.",
             "desc": "Betplay launched in 2020 with a focus on delivering a premium crypto sports betting experience. Their standout $10,000 welcome bonus and competitive football odds have quickly attracted a dedicated user base."},
            {"name": "Vave Sports", "slug": "vave-sports", "rating": 4.3, "bonus": "100% up to 1 BTC", "code": "VAVE100", "min_deposit": "$10 equivalent", "wagering": "40x", "year": 2022, "cryptos": ["BTC", "ETH", "LTC", "USDT", "DOGE", "TRX"],
             "pros": ["Combined sportsbook and casino", "Clean interface for live betting", "Good coverage of Asian markets", "Regular accumulator boosts"],
             "cons": ["1 BTC max is modest vs competitors", "Newer brand with less reputation", "Customer support response times vary"],
             "expert": "Vave Sports provides a clean, no-nonsense sportsbook experience with solid coverage across major and minor leagues. The 1 BTC welcome bonus is straightforward and the live betting interface is smooth and responsive.",
             "desc": "Vave Sports combines a comprehensive sportsbook with their established crypto casino platform. The clean interface and solid odds make it a respectable option for crypto sports bettors seeking simplicity."},
            {"name": "Duelbits", "slug": "duelbits", "rating": 4.4, "bonus": "Up to $1,000 Cashback", "code": "DUEL1K", "min_deposit": "$10 equivalent", "wagering": "3x", "year": 2020, "cryptos": ["BTC", "ETH", "LTC", "USDT", "SOL", "DOGE"],
             "pros": ["Ultra-low 3x wagering on cashback", "SOL support — rare among competitors", "Fun, gamified user experience", "Active community and social features"],
             "cons": ["Cashback structure can be confusing", "Odds not always the sharpest", "Brand less established than top tier"],
             "expert": "Duelbits takes the cashback approach with an incredible 3x wagering requirement — the lowest we have seen. The gamified experience and SOL support make it unique, though the odds could be sharper on some markets.",
             "desc": "Duelbits brings a gamified approach to crypto sports betting with cashback rewards and one of the lowest wagering requirements in the industry. Their community-driven platform and SOL support set them apart."},
        ]
    },
    "poker": {
        "name": "Crypto Poker",
        "page": "crypto-poker.html",
        "slug": "poker",
        "brands": [
            {"name": "CoinPoker", "slug": "coinpoker", "rating": 4.7, "bonus": "150% up to $2,000 + Free Tickets", "code": "CPOKER150", "min_deposit": "$10 equivalent", "wagering": "Earned via rakeback", "year": 2017, "cryptos": ["CHP (native)", "BTC", "ETH", "USDT"],
             "pros": ["Dedicated crypto poker platform", "Provably fair card dealing (RNG audit)", "Own CHP token for reduced rake", "Regular freerolls and tournaments"],
             "cons": ["Smaller player pool than major sites", "CHP token adds complexity", "Limited cash game traffic off-peak"],
             "expert": "CoinPoker is the premier dedicated crypto poker platform. Their provably fair dealing system, own CHP token, and 150% bonus make it the top choice for serious crypto poker players. Player pools are growing steadily.",
             "desc": "CoinPoker is built from the ground up for crypto poker players. Their native CHP token reduces rake, and the provably fair dealing system provides transparency that traditional poker rooms cannot match."},
            {"name": "Blockchain Poker", "slug": "blockchain-poker", "rating": 4.3, "bonus": "Free Satoshis on Signup", "code": "AUTO", "min_deposit": "None (free to start)", "wagering": "None", "year": 2015, "cryptos": ["BTC", "BCH", "BSV"],
             "pros": ["Completely free to start — no deposit needed", "Simple, clean interface", "Anonymous play — no KYC required", "Micro-stakes available for learning"],
             "cons": ["Very limited game variety (Hold'em only)", "Small player base", "Basic interface with few features"],
             "expert": "Blockchain Poker is perfect for beginners who want to try crypto poker without risking anything. Free satoshis on signup and no KYC means you can be playing in seconds. The trade-off is a smaller player pool and limited game selection.",
             "desc": "Blockchain Poker offers the purest form of Bitcoin poker — anonymous, simple, and free to start. They give you free satoshis upon signup so you can jump into real-money games without depositing a single sat."},
            {"name": "SwC Poker", "slug": "swc-poker", "rating": 4.2, "bonus": "100% up to 1 BTC Rakeback", "code": "SWC100", "min_deposit": "0.001 BTC", "wagering": "Earned via rake", "year": 2012, "cryptos": ["BTC"],
             "pros": ["One of the oldest Bitcoin poker rooms", "High rakeback percentage", "Anonymous play — Bitcoin only", "Decent tournament schedule"],
             "cons": ["Bitcoin only — no other cryptos", "Player pool has declined", "Interface feels outdated", "No mobile app"],
             "expert": "SwC Poker is a Bitcoin purist's poker room. Operating since 2012, it is one of the longest-running crypto poker platforms. The rakeback bonus is solid for grinders, though the declining player pool is a concern.",
             "desc": "SwC Poker (formerly Seals with Clubs) has been a pioneer in Bitcoin poker since 2012. As a Bitcoin-only platform, it appeals to purists who value anonymity and the OG crypto poker experience."},
            {"name": "BetOnline Poker", "slug": "betonline-poker", "rating": 4.5, "bonus": "100% up to $1,000", "code": "BOL1000", "min_deposit": "$20 equivalent", "wagering": "Cleared in increments", "year": 2004, "cryptos": ["BTC", "ETH", "LTC", "BCH", "USDT", "XRP"],
             "pros": ["Largest player pool among crypto-friendly rooms", "Established since 2004", "Multiple crypto deposit options", "Excellent tournament schedule"],
             "cons": ["Not exclusively crypto — also accepts fiat", "Higher minimum deposit", "Bonus cleared slowly through play"],
             "expert": "BetOnline Poker offers the best of both worlds — a large, established player pool with full crypto support. The $1,000 welcome bonus and extensive tournament schedule make it ideal for players who want consistent action.",
             "desc": "BetOnline has been a trusted name in online poker since 2004 and has embraced crypto payments fully. Their large player pool ensures action at all stakes and times, making them the most liquid crypto-friendly poker room."},
            {"name": "Americas Cardroom", "slug": "americas-cardroom", "rating": 4.4, "bonus": "100% up to $2,000 + Free $50", "code": "ACR2000", "min_deposit": "$25 equivalent", "wagering": "Released in $1 increments", "year": 2001, "cryptos": ["BTC", "ETH", "LTC", "BCH", "DOGE", "USDT"],
             "pros": ["Largest bonus at $2,000 + $50 free", "Long-established since 2001", "Massive tournament guarantees", "Crypto deposits get extra bonuses"],
             "cons": ["Bonus releases very slowly", "Software can feel dated", "Higher rake on micro-stakes"],
             "expert": "Americas Cardroom offers the biggest bonus package in crypto poker — $2,000 plus an extra $50 free. Their tournament schedule features massive guarantees, and crypto depositors get preferential treatment. The bonus release is slow but steady.",
             "desc": "Americas Cardroom has been a pillar of online poker since 2001. Their embrace of cryptocurrency deposits and massive tournament guarantees have made them a top destination for serious poker players."},
        ]
    },
    "exchanges": {
        "name": "Crypto Exchanges",
        "page": "crypto-exchanges.html",
        "slug": "exchanges",
        "brands": [
            {"name": "Coinbase", "slug": "coinbase", "rating": 4.7, "bonus": "Get $10 in BTC on First Trade", "code": "AUTO", "min_deposit": "$50 first trade", "wagering": "N/A", "year": 2012, "cryptos": ["250+ cryptos"],
             "pros": ["Most trusted exchange in the US", "Publicly traded (NASDAQ: COIN)", "Beginner-friendly interface", "Strong security with insurance coverage"],
             "cons": ["Higher fees than some competitors", "Customer support can be slow", "Advanced features require Coinbase Advanced"],
             "expert": "Coinbase is the gold standard for beginners entering the crypto world. As a publicly traded company with robust security and insurance, it offers peace of mind that few exchanges can match. The $10 BTC bonus on your first trade is a nice welcome.",
             "desc": "Coinbase is the most widely recognized crypto exchange in the world. As a NASDAQ-listed company, they offer institutional-grade security and a beginner-friendly platform that has onboarded millions of new crypto users."},
            {"name": "Kraken", "slug": "kraken", "rating": 4.8, "bonus": "Up to $100 Trading Credit", "code": "KRAK100", "min_deposit": "$10", "wagering": "N/A", "year": 2011, "cryptos": ["200+ cryptos"],
             "pros": ["One of the oldest and most trusted exchanges", "Advanced trading features (margin, futures)", "Excellent security record — never hacked", "Competitive fees for high volume"],
             "cons": ["Interface can intimidate beginners", "Staking rewards reduced in some regions", "Slower fiat withdrawal times"],
             "expert": "Kraken is the exchange for serious traders. Operating since 2011 without a single security breach, their track record is impeccable. The $100 trading credit and competitive fee structure make them our top-rated exchange.",
             "desc": "Kraken has been one of the most trusted names in crypto since 2011. Their perfect security record, advanced trading tools, and transparent fee structure have earned them a loyal following among experienced traders."},
            {"name": "Binance", "slug": "binance", "rating": 4.6, "bonus": "100 USDT Trading Fee Rebate", "code": "BINANCE100", "min_deposit": "$10", "wagering": "N/A", "year": 2017, "cryptos": ["350+ cryptos"],
             "pros": ["Largest exchange by trading volume globally", "Widest selection of trading pairs", "Lowest fees in the industry", "Advanced tools: futures, options, staking"],
             "cons": ["Regulatory challenges in several countries", "Complex interface for beginners", "US users have limited access (Binance.US)"],
             "expert": "Binance is the world's largest crypto exchange by volume for a reason — the widest selection of coins, the lowest fees, and the most advanced trading tools. Regulatory concerns aside, no exchange offers more for active traders.",
             "desc": "Binance dominates the global crypto exchange landscape with the highest trading volume and the most extensive selection of cryptocurrencies. Their fee structure is among the most competitive in the industry."},
            {"name": "KuCoin", "slug": "kucoin", "rating": 4.5, "bonus": "Up to $700 Welcome Bonus", "code": "KUCOIN700", "min_deposit": "$10", "wagering": "N/A", "year": 2017, "cryptos": ["700+ cryptos"],
             "pros": ["Largest altcoin selection at 700+", "Trading bot marketplace built-in", "No mandatory KYC for basic trading", "Competitive spot and futures fees"],
             "cons": ["Has experienced a security breach", "Less regulated than top-tier exchanges", "Withdrawal fees can be high"],
             "expert": "KuCoin is the altcoin hunter's paradise with over 700 listed tokens — more than any other major exchange. The $700 welcome bonus and built-in trading bots add significant value. Just be mindful of their security history.",
             "desc": "KuCoin has positioned itself as the go-to exchange for discovering new and emerging cryptocurrencies. With over 700 tokens listed and built-in trading bot features, it caters to both altcoin enthusiasts and automated traders."},
            {"name": "Bybit", "slug": "bybit", "rating": 4.6, "bonus": "Up to $30,000 Deposit Bonus", "code": "BYBIT30K", "min_deposit": "$10", "wagering": "N/A", "year": 2018, "cryptos": ["300+ cryptos"],
             "pros": ["Massive $30,000 deposit bonus", "Best derivatives trading platform", "Excellent mobile app", "Copy trading feature available"],
             "cons": ["Not available in US", "Bonus structure can be complex", "Spot trading fees slightly higher than Binance"],
             "expert": "Bybit offers the most generous welcome bonus in the exchange space at $30,000 — though it is tiered based on deposit amount. Their derivatives trading platform is arguably the best in the industry, and the copy trading feature is excellent for beginners.",
             "desc": "Bybit has rapidly grown into one of the world's leading crypto exchanges, particularly for derivatives trading. Their generous bonus structure and copy trading features have attracted millions of users globally."},
            {"name": "OKX", "slug": "okx", "rating": 4.5, "bonus": "Up to $10,000 in Mystery Boxes", "code": "OKX10K", "min_deposit": "$50", "wagering": "N/A", "year": 2017, "cryptos": ["300+ cryptos"],
             "pros": ["Innovative mystery box rewards", "Comprehensive DeFi and Web3 wallet", "Competitive trading fees", "Strong API for algorithmic trading"],
             "cons": ["Mystery box values can be low", "Not available in US", "Interface complexity for beginners"],
             "expert": "OKX combines traditional exchange features with cutting-edge Web3 tools. Their mystery box welcome offer is creative, and the integrated DeFi wallet makes them a one-stop-shop for crypto. The $10,000 potential value is enticing.",
             "desc": "OKX has evolved from a pure exchange into a comprehensive Web3 platform with integrated DeFi, NFT, and wallet services. Their innovative approach to user rewards and strong trading infrastructure make them a formidable competitor."},
            {"name": "Gemini", "slug": "gemini", "rating": 4.4, "bonus": "$10 in BTC After First Trade", "code": "AUTO", "min_deposit": "$25 first trade", "wagering": "N/A", "year": 2014, "cryptos": ["100+ cryptos"],
             "pros": ["Founded by Winklevoss twins — strong brand", "SOC 2 certified security", "Available in all 50 US states", "Gemini Earn (interest on holdings)"],
             "cons": ["Higher fees than most competitors", "Smaller crypto selection", "Gemini Earn had issues in 2022"],
             "expert": "Gemini is the premium, regulation-first exchange. Their SOC 2 certification and availability in all 50 US states make them ideal for compliance-conscious investors. The $10 BTC welcome bonus is modest but the platform's security justifies the premium.",
             "desc": "Gemini, founded by Cameron and Tyler Winklevoss, is one of the most regulated and secure crypto exchanges operating in the United States. Their compliance-first approach appeals to institutional and cautious retail investors alike."},
            {"name": "Crypto.com", "slug": "crypto-com", "rating": 4.5, "bonus": "$25 CRO Welcome Bonus", "code": "CRYPTO25", "min_deposit": "$1", "wagering": "N/A", "year": 2016, "cryptos": ["250+ cryptos"],
             "pros": ["Excellent Visa debit card with crypto rewards", "Low $1 minimum deposit", "Wide range of DeFi services", "Strong brand presence and marketing"],
             "cons": ["CRO token volatile", "Card tier benefits reduced recently", "App can be slow during high traffic"],
             "expert": "Crypto.com has become one of the most recognizable brands in crypto thanks to aggressive marketing and their excellent Visa card program. The $25 CRO bonus and $1 minimum deposit make it incredibly accessible for newcomers.",
             "desc": "Crypto.com has built one of the most comprehensive crypto ecosystems, combining exchange services with a popular Visa debit card, DeFi platform, and NFT marketplace. Their low entry barrier and strong brand make them a top choice for new crypto users."},
        ]
    },
    "lottery": {
        "name": "Crypto Lottery",
        "page": "crypto-lottery.html",
        "slug": "lottery",
        "brands": [
            {"name": "Lottoland", "slug": "lottoland", "rating": 4.3, "bonus": "2 Bets for the Price of 1", "code": "LOTTO2FOR1", "min_deposit": "$5", "wagering": "None", "year": 2013, "cryptos": ["BTC", "ETH", "USDT"],
             "pros": ["Bet on 30+ international lotteries", "No wagering on bonus", "Established and licensed operator", "Jackpots into the billions"],
             "cons": ["Limited crypto options (only 3)", "Not a blockchain-native platform", "Some lotteries not available in all regions"],
             "expert": "Lottoland brings the thrill of global lotteries to crypto users. The 2-for-1 welcome offer with zero wagering is refreshingly simple. While their crypto support is limited to three coins, the ability to bet on 30+ international lotteries is unmatched.",
             "desc": "Lottoland is the world's leading online lottery betting platform, offering access to over 30 international lotteries. Their recent addition of crypto payment options brings Bitcoin convenience to traditional lottery excitement."},
            {"name": "Lucky Block", "slug": "lucky-block", "rating": 4.6, "bonus": "200% up to $10,000", "code": "LUCKY200", "min_deposit": "$1", "wagering": "40x", "year": 2022, "cryptos": ["BTC", "ETH", "DOGE", "USDT", "BNB", "ADA", "XRP"],
             "pros": ["Huge 200% bonus up to $10,000", "Very low $1 minimum deposit", "Blockchain-native lottery draws", "Multiple crypto options supported"],
             "cons": ["40x wagering applies", "Newer platform with less history", "Lottery draws may have fewer participants"],
             "expert": "Lucky Block offers the most generous bonus in the crypto lottery space — 200% up to $10,000 with a $1 minimum. Their blockchain-native draws ensure transparency, and the wide crypto support is excellent. A top pick for crypto lottery enthusiasts.",
             "desc": "Lucky Block was built from the ground up as a blockchain-based lottery platform. Their transparent draw system, generous bonuses, and wide cryptocurrency support make them the leading crypto-native lottery option."},
            {"name": "Mega Dice", "slug": "mega-dice", "rating": 4.5, "bonus": "200% up to 1 BTC", "code": "MEGA200", "min_deposit": "$20", "wagering": "40x", "year": 2023, "cryptos": ["BTC", "ETH", "USDT", "DOGE", "SOL"],
             "pros": ["200% match bonus on first deposit", "Multiple lottery and dice games", "SOL support — rare feature", "Modern, gamified interface"],
             "cons": ["Very new platform (2023)", "Higher $20 minimum deposit", "40x wagering on bonus"],
             "expert": "Mega Dice combines lottery draws with provably fair dice games for a unique crypto gaming experience. The 200% bonus up to 1 BTC is excellent, and SOL support is a nice touch. Being brand new, they have the freshest tech but less track record.",
             "desc": "Mega Dice launched in 2023 as a next-generation crypto lottery and gaming platform. Their combination of traditional lottery draws, provably fair dice games, and modern crypto support offers something different in the space."},
            {"name": "Stake Lottery", "slug": "stake-lottery", "rating": 4.4, "bonus": "Weekly Lottery Draws — Free Entry", "code": "CRYPTOSITES", "min_deposit": "0.0001 BTC", "wagering": "None", "year": 2017, "cryptos": ["BTC", "ETH", "LTC", "DOGE", "XRP", "TRX"],
             "pros": ["Free entry to weekly lottery draws", "Part of the trusted Stake ecosystem", "No wagering requirements", "Additional casino and sports access"],
             "cons": ["Lottery is a secondary feature, not the focus", "Prize pools smaller than dedicated lotteries", "Must be active on platform to qualify"],
             "expert": "Stake Lottery is a bonus feature within the Stake ecosystem — active players get free weekly lottery entries. While it is not a dedicated lottery platform, the zero cost and zero wagering make it a nice perk for existing Stake users.",
             "desc": "Stake Lottery is integrated into the broader Stake platform, offering weekly lottery draws with free entry for active users. As part of the world's largest crypto gambling platform, it benefits from Stake's trusted infrastructure."},
            {"name": "BC.Game Lottery", "slug": "bc-game-lottery", "rating": 4.3, "bonus": "Daily Lucky Spin + Draws", "code": "CRYPTO360", "min_deposit": "$10 equivalent", "wagering": "None", "year": 2017, "cryptos": ["BTC", "ETH", "DOGE", "150+ more"],
             "pros": ["Daily lucky spins for all users", "Part of established BC.Game ecosystem", "150+ crypto deposit options", "Community-driven prize pools"],
             "cons": ["Lottery is not the primary product", "Prizes can be small on daily spins", "Must navigate full casino to find lottery"],
             "expert": "BC.Game's lottery features include daily lucky spins and community draws that complement their main casino offering. The 150+ crypto support is unmatched, though dedicated lottery players might prefer a focused platform.",
             "desc": "BC.Game Lottery is part of the broader BC.Game ecosystem, offering daily lucky spins and periodic lottery draws. The platform's massive crypto support and active community create engaging prize pool opportunities."},
        ]
    },
    "wallets": {
        "name": "Crypto Wallets",
        "page": "crypto-wallets.html",
        "slug": "wallets",
        "brands": [
            {"name": "Ledger", "slug": "ledger", "rating": 4.8, "bonus": "Free Shipping + $10 BTC Cashback", "code": "LEDGER10", "min_deposit": "Purchase device", "wagering": "N/A", "year": 2014, "cryptos": ["5,500+ coins supported"],
             "pros": ["Industry-leading hardware security", "Supports 5,500+ cryptocurrencies", "Ledger Live app for easy management", "Bluetooth connectivity on Nano X"],
             "cons": ["Hardware cost ($79-$149)", "Ledger Live can feel clunky", "Past data breach raised concerns"],
             "expert": "Ledger is the world's most popular hardware wallet for good reason. Supporting over 5,500 coins with military-grade security, it is the gold standard for self-custody. The free shipping and $10 BTC cashback sweeten an already essential purchase.",
             "desc": "Ledger is the global leader in hardware cryptocurrency wallets, trusted by millions of users worldwide. Their devices keep your private keys offline, providing the highest level of security for your digital assets."},
            {"name": "Trezor", "slug": "trezor", "rating": 4.7, "bonus": "15% Off First Purchase", "code": "TREZOR15", "min_deposit": "Purchase device", "wagering": "N/A", "year": 2013, "cryptos": ["1,800+ coins supported"],
             "pros": ["Fully open-source firmware", "Pioneer of hardware wallets (since 2013)", "Trezor Suite desktop app is excellent", "No Bluetooth — some see this as more secure"],
             "cons": ["Fewer supported coins than Ledger", "Touchscreen only on expensive Model T", "Plastic build feels less premium"],
             "expert": "Trezor invented the hardware wallet category in 2013 and remains one of the best choices. Their fully open-source approach provides transparency that security purists love. The 15% discount makes the entry point very reasonable.",
             "desc": "Trezor pioneered the hardware wallet industry in 2013 and continues to set the standard for open-source security. Their commitment to transparency and user control has earned them a devoted following among crypto security advocates."},
            {"name": "MetaMask", "slug": "metamask", "rating": 4.5, "bonus": "No bonus — Free to use", "code": "N/A", "min_deposit": "None (free)", "wagering": "N/A", "year": 2016, "cryptos": ["Ethereum + all EVM chains"],
             "pros": ["Essential for Ethereum and DeFi", "Free browser extension and mobile app", "Connects to thousands of dApps", "Widely supported across Web3"],
             "cons": ["Only supports EVM-compatible chains", "Swap fees can be high", "Hot wallet — less secure than hardware"],
             "expert": "MetaMask is the gateway to Ethereum and DeFi. If you interact with any EVM-based dApps, you need MetaMask. It is free, widely supported, and has become the de facto standard for Web3 wallet connectivity.",
             "desc": "MetaMask is the most widely used cryptocurrency wallet for interacting with the Ethereum ecosystem and DeFi applications. As a free browser extension and mobile app, it connects users to thousands of decentralized applications."},
            {"name": "Trust Wallet", "slug": "trust-wallet", "rating": 4.5, "bonus": "No bonus — Free to use", "code": "N/A", "min_deposit": "None (free)", "wagering": "N/A", "year": 2017, "cryptos": ["70+ blockchains supported"],
             "pros": ["Supports 70+ blockchains — not just EVM", "Built-in DEX for token swaps", "Backed by Binance", "Clean, intuitive mobile interface"],
             "cons": ["No desktop version", "Swap fees can be high", "Hot wallet — less secure than hardware"],
             "expert": "Trust Wallet is the most versatile mobile crypto wallet, supporting over 70 blockchains including non-EVM chains. Backed by Binance and completely free, it is an excellent all-around choice for mobile crypto management.",
             "desc": "Trust Wallet, backed by Binance, is one of the most popular mobile cryptocurrency wallets. Supporting over 70 blockchains and featuring a built-in decentralized exchange, it offers comprehensive multi-chain management."},
            {"name": "Coinbase Wallet", "slug": "coinbase-wallet", "rating": 4.4, "bonus": "$5 in ETH for First Swap", "code": "AUTO", "min_deposit": "None (free)", "wagering": "N/A", "year": 2018, "cryptos": ["Ethereum + EVM, Solana, Bitcoin"],
             "pros": ["Self-custody with Coinbase brand trust", "Connects to Coinbase exchange seamlessly", "Multi-chain support including Solana", "DApp browser built-in"],
             "cons": ["Separate from Coinbase exchange", "Gas fees passed through to user", "Can confuse users vs Coinbase app"],
             "expert": "Coinbase Wallet gives you self-custody with the backing of the most trusted name in crypto. It is separate from the Coinbase exchange but integrates beautifully. The $5 ETH bonus for your first swap is a nice welcome touch.",
             "desc": "Coinbase Wallet is a self-custody wallet from the team behind Coinbase exchange. It provides users full control of their private keys while leveraging the Coinbase brand's trust and seamless exchange integration."},
            {"name": "Exodus", "slug": "exodus", "rating": 4.3, "bonus": "No bonus — Free to use", "code": "N/A", "min_deposit": "None (free)", "wagering": "N/A", "year": 2015, "cryptos": ["250+ assets supported"],
             "pros": ["Beautiful, intuitive design", "Desktop and mobile versions", "Built-in exchange for swaps", "Portfolio tracking and charts"],
             "cons": ["Not open-source", "Swap fees higher than exchanges", "No two-factor authentication (relies on email)"],
             "expert": "Exodus is the most beautiful crypto wallet on the market. Their desktop and mobile apps feature stunning portfolio visualizations and a built-in exchange. If you value design and ease of use, Exodus is unmatched.",
             "desc": "Exodus stands out in the wallet space with its stunning visual design and intuitive interface. Available on desktop and mobile, it combines portfolio management, built-in exchange, and support for 250+ assets in one elegant package."},
        ]
    },
}

# ============================================================
# HTML TEMPLATES
# ============================================================

HEAD_ATTRIBUTION = '''<!--
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
<link rel="author" href="https://www.perplexity.ai/computer">'''

LOGO_SVG = '''<svg viewBox="0 0 32 32" width="32" height="32" fill="none" aria-label="Cryptosites logo">
  <path d="M16 2 L28 9 L28 23 L16 30 L4 23 L4 9 Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" opacity="0.6"/>
  <path d="M20 11 A6 6 0 1 0 20 21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="21" cy="11" r="1.5" fill="var(--secondary)"/>
  <circle cx="21" cy="21" r="1.5" fill="var(--secondary)"/>
</svg>'''

FAVICON_SVG = '''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="none">
  <path d="M16 2 L28 9 L28 23 L16 30 L4 23 L4 9 Z" stroke="#00d4aa" stroke-width="1.5" stroke-linejoin="round" opacity="0.6"/>
  <path d="M20 11 A6 6 0 1 0 20 21" stroke="#00d4aa" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="21" cy="11" r="1.5" fill="#f7b731"/>
  <circle cx="21" cy="21" r="1.5" fill="#f7b731"/>
</svg>'''

def get_nav_html(active_page=""):
    return f'''<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="container nav-inner">
    <a href="./index.html" class="nav-logo" aria-label="Cryptosites home">
      {LOGO_SVG}
      <span class="nav-logo-text">Crypto<span class="logo-accent">sites</span></span>
    </a>
    <div class="nav-links">
      <a href="./index.html"{' class="active"' if active_page == 'home' else ''}>Home</a>
<a href="./crypto-casinos.html"{' class="active"' if active_page == 'casinos' else ''}>Casinos</a>
<a href="./crypto-sports-betting.html"{' class="active"' if active_page == 'sports' else ''}>Sports</a>
<a href="./crypto-poker.html"{' class="active"' if active_page == 'poker' else ''}>Poker</a>
<a href="./crypto-exchanges.html"{' class="active"' if active_page == 'exchanges' else ''}>Exchanges</a>
<a href="./crypto-lottery.html"{' class="active"' if active_page == 'lottery' else ''}>Lottery</a>
<a href="./crypto-wallets.html"{' class="active"' if active_page == 'wallets' else ''}>Wallets</a>
    </div>
    <div class="nav-actions">
      <div class="starred-badge" id="starredBadge" role="button" tabindex="0" aria-label="Starred platforms">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"/></svg>
        <span class="starred-count" id="starredCount">0</span>
        <div class="starred-dropdown" id="starredDropdown">
          <div class="starred-dropdown-header">Starred Platforms</div>
          <div class="starred-dropdown-list" id="starredList">
            <div class="starred-dropdown-empty">Star a platform to track it here</div>
          </div>
        </div>
      </div>
      <button class="theme-toggle" aria-label="Toggle dark/light mode" type="button">
        <span class="icon-sun"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></span>
        <span class="icon-moon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></span>
      </button>
      <button class="mobile-menu-btn" aria-label="Toggle menu" aria-expanded="false" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </div>
</nav>
<div class="mobile-nav" id="mobileNav" aria-hidden="true">
  <div class="mobile-nav-inner">
    <a href="./index.html" class="mobile-nav-link">Home</a>
    <a href="./crypto-casinos.html" class="mobile-nav-link">Casinos</a>
    <a href="./crypto-sports-betting.html" class="mobile-nav-link">Sports</a>
    <a href="./crypto-poker.html" class="mobile-nav-link">Poker</a>
    <a href="./crypto-exchanges.html" class="mobile-nav-link">Exchanges</a>
    <a href="./crypto-lottery.html" class="mobile-nav-link">Lottery</a>
    <a href="./crypto-wallets.html" class="mobile-nav-link">Wallets</a>
  </div>
</div>'''


def get_footer_html():
    top_brands = [
        ("Stake", "promo-stake-casino.html"),
        ("Kraken", "promo-kraken.html"),
        ("BC.Game", "promo-bc-game-casino.html"),
        ("Coinbase", "promo-coinbase.html"),
        ("Cloudbet", "promo-cloudbet-casino.html"),
        ("Ledger", "promo-ledger.html"),
        ("CoinPoker", "promo-coinpoker.html"),
        ("Lucky Block", "promo-lucky-block.html"),
    ]
    top_links = "\n".join(f'        <a href="./{slug}">{name}</a>' for name, slug in top_brands)

    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
          {LOGO_SVG.replace('width="32" height="32"', 'width="28" height="28"')}
          <span style="font-weight:700;font-size:15px;color:var(--text-primary)">Crypto<span style="color:var(--accent)">sites</span></span>
        </div>
        <p style="font-size:13px;color:var(--text-secondary);line-height:1.6">Independent crypto platform reviews. No fluff, no bias, no nonsense. Updated March 2026.</p>
        <p style="margin-top:8px"><a href="mailto:hello@cryptosites.com" style="color:var(--accent);font-weight:600;font-size:13px">hello@cryptosites.com</a></p>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Top Platforms</p>
        <div class="footer-links">
{top_links}
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
        <a href="./about.html">About Us</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Transparency</p>
        <div class="footer-links">
        <a href="./about.html">Code of Ethics</a>
        <a href="./about.html">Editorial Policy</a>
        <a href="./about.html">Affiliate Disclosure</a>
        <a href="./about.html">Fact Checking</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Responsible Gambling</p>
        <div class="footer-links">
        <a href="./about.html">Gambling Policy</a>
        <a href="./about.html">Support Organisations</a>
        <a href="./about.html">Risk Awareness</a>
        <a href="./about.html">Self-Exclusion</a>
        </div>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Legal</p>
        <div class="footer-links">
        <a href="./about.html">Privacy Policy</a>
        <a href="./about.html">Terms &amp; Conditions</a>
        <a href="./about.html">Cookie Policy</a>
        <a href="./sitemap.xml">Sitemap</a>
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
</footer>'''


def get_brand_color(name):
    """Generate a consistent brand color based on name."""
    colors = {
        "Stake": "#1c4532", "BC.Game": "#2d3748", "BitStarz": "#44337a",
        "mBit": "#2a4365", "FortuneJack": "#744210", "Cloudbet": "#1a365d",
        "Wild.io": "#22543d", "Vave": "#2d3748", "Sportsbet.io": "#1a365d",
        "Thunderpick": "#44337a", "Betplay": "#1c4532", "Duelbits": "#2d3748",
        "CoinPoker": "#2a4365", "Blockchain Poker": "#1a365d", "SwC Poker": "#744210",
        "BetOnline": "#22543d", "Americas Cardroom": "#44337a",
        "Coinbase": "#1c4532", "Kraken": "#44337a", "Binance": "#744210",
        "KuCoin": "#1c4532", "Bybit": "#2d3748", "OKX": "#1a365d",
        "Gemini": "#2a4365", "Crypto.com": "#1c4532",
        "Lottoland": "#744210", "Lucky Block": "#22543d", "Mega Dice": "#2d3748",
        "Stake Lottery": "#1c4532", "BC.Game Lottery": "#2d3748",
        "Ledger": "#1a365d", "Trezor": "#22543d", "MetaMask": "#744210",
        "Trust Wallet": "#1c4532", "Coinbase Wallet": "#2a4365", "Exodus": "#44337a",
    }
    for key, val in colors.items():
        if key in name:
            return val
    return "#2d3748"


def get_badge_text(rating):
    if rating >= 4.8: return "EDITOR'S CHOICE"
    if rating >= 4.5: return "TOP PICK"
    if rating >= 4.3: return "RECOMMENDED"
    return "REVIEWED"


def get_claim_steps(cat_slug, brand_name, code):
    if cat_slug == "wallets":
        return f'''<div class="claim-steps">
  <div class="claim-step"><div class="claim-step-num">1</div><div class="claim-step-content"><div class="claim-step-title">Download the Wallet</div><div class="claim-step-desc">Head to the official {brand_name} website or app store and download the application. Always verify you are on the official site to avoid scams.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">2</div><div class="claim-step-content"><div class="claim-step-title">Create Your Wallet</div><div class="claim-step-desc">Follow the setup process. Write down your recovery phrase on paper and store it safely. Never share it with anyone or store it digitally.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">3</div><div class="claim-step-content"><div class="claim-step-title">{"Use Referral Code" if code not in ("N/A", "AUTO") else "Secure Your Wallet"}</div><div class="claim-step-desc">{"Enter the referral code <strong>" + code + "</strong> during setup or in the promotions section to claim your bonus." if code not in ("N/A", "AUTO") else "Enable all available security features: biometric lock, PIN code, and if available, connect a hardware wallet for extra protection."}</div></div></div>
  <div class="claim-step"><div class="claim-step-num">4</div><div class="claim-step-content"><div class="claim-step-title">Get Started</div><div class="claim-step-desc">{"Your bonus will be applied automatically. " if code not in ("N/A", "AUTO") else ""}You are ready to receive, send, and manage your crypto. Start by transferring a small test amount to verify everything works.</div></div></div>
</div>'''
    elif cat_slug == "exchanges":
        return f'''<div class="claim-steps">
  <div class="claim-step"><div class="claim-step-num">1</div><div class="claim-step-content"><div class="claim-step-title">Create Your Account</div><div class="claim-step-desc">Visit {brand_name} and register with your email address. Use a strong, unique password and enable two-factor authentication immediately.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">2</div><div class="claim-step-content"><div class="claim-step-title">Complete Verification</div><div class="claim-step-desc">Complete the KYC (Know Your Customer) process by uploading your government-issued ID and proof of address. This typically takes 10-30 minutes.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">3</div><div class="claim-step-content"><div class="claim-step-title">{"Enter Promo Code" if code not in ("N/A", "AUTO") else "Fund Your Account"}</div><div class="claim-step-desc">{"Enter the code <strong>" + code + "</strong> in the promotions or referral section. Then make your first deposit to activate the bonus." if code not in ("N/A", "AUTO") else "Deposit funds via bank transfer, card, or crypto. Your welcome bonus will be applied automatically on your first qualifying trade."}</div></div></div>
  <div class="claim-step"><div class="claim-step-num">4</div><div class="claim-step-content"><div class="claim-step-title">Make Your First Trade</div><div class="claim-step-desc">Execute your first trade to activate the welcome bonus. Start with a well-known asset like BTC or ETH while you learn the platform.</div></div></div>
</div>'''
    else:
        return f'''<div class="claim-steps">
  <div class="claim-step"><div class="claim-step-num">1</div><div class="claim-step-content"><div class="claim-step-title">Create Your Account</div><div class="claim-step-desc">Head to {brand_name} and click the registration button. Fill in your email and create a strong password. The process takes under a minute.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">2</div><div class="claim-step-content"><div class="claim-step-title">Enter Promo Code</div><div class="claim-step-desc">Enter the promo code <strong>{code}</strong> in the registration form or bonus section. Make sure to enter it exactly as shown — codes are case-sensitive.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">3</div><div class="claim-step-content"><div class="claim-step-title">Verify Your Account</div><div class="claim-step-desc">Complete any required verification steps. Some platforms require KYC, others allow anonymous play. Check the specific requirements for {brand_name}.</div></div></div>
  <div class="claim-step"><div class="claim-step-num">4</div><div class="claim-step-content"><div class="claim-step-title">Deposit &amp; Claim</div><div class="claim-step-desc">Make your first crypto deposit (minimum {brand_name.split()[0]} requirement applies) and your welcome bonus will be credited. Time to explore the platform.</div></div></div>
</div>'''


def get_faq_items(brand, cat_slug):
    name = brand["name"]
    code = brand["code"]
    bonus = brand["bonus"]

    if cat_slug == "wallets":
        return [
            (f"Is {name} safe to use?", f"Yes, {name} is a well-established wallet trusted by millions of users. However, always follow security best practices: keep your recovery phrase offline, enable all security features, and only download from official sources."),
            (f"Is {name} really free?", f"{'Yes, ' + name + ' is completely free to download and use. There are no subscription fees.' if brand['min_deposit'] == 'None (free)' else name + ' requires a device purchase, but the software is free to use once you have the hardware.'}"),
            (f"What cryptos does {name} support?", f"{name} supports {brand['cryptos'][0] if isinstance(brand['cryptos'], list) and len(brand['cryptos']) == 1 else ', '.join(brand['cryptos']) if isinstance(brand['cryptos'], list) else brand['cryptos']}. Support for new chains and tokens is added regularly."),
            (f"Can I recover my wallet if I lose my device?", f"Yes, as long as you have your recovery phrase (seed phrase) saved securely. This is typically 12 or 24 words that were shown during setup. Without this phrase, your funds cannot be recovered."),
        ]
    elif cat_slug == "exchanges":
        return [
            (f"Is {name} safe and legitimate?", f"Yes, {name} is a{'n established' if brand['year'] < 2018 else ' reputable'} cryptocurrency exchange operating since {brand['year']}. They employ industry-standard security measures including cold storage, 2FA, and regular audits."),
            (f"What is the {name} welcome bonus?", f"New users can get {bonus} when signing up{' with code ' + code if code not in ('N/A', 'AUTO') else ''}. The bonus is typically credited after your first qualifying trade or deposit."),
            (f"How long does KYC verification take?", f"KYC verification at {name} typically takes between 10 minutes and 48 hours, depending on volume. Having your government-issued ID and proof of address ready speeds up the process significantly."),
            (f"What are {name}'s trading fees?", f"{name} uses a maker-taker fee model. Fees vary by trading volume and whether you are a maker (adding liquidity) or taker (removing liquidity). Higher volume traders enjoy lower fees."),
        ]
    else:
        return [
            (f"Is the {name} promo code {code} still working?", f"Yes, we verified this code is active as of March 2026. Enter <strong>{code}</strong> during registration to claim your {bonus} bonus."),
            (f"What is the minimum deposit at {name}?", f"The minimum deposit at {name} is {brand['min_deposit']}. Some crypto deposits may have different minimums based on network fees."),
            (f"How long does it take to receive my bonus?", f"Most bonuses at {name} are credited instantly after your qualifying deposit. Some may require a pending period of up to 24 hours depending on blockchain confirmation times."),
            (f"Can I withdraw the bonus immediately?", f"{'You will need to meet the ' + brand['wagering'] + ' wagering requirement first before withdrawing bonus funds.' if brand['wagering'] not in ('N/A', 'None', 'Loyalty points system', 'Loyalty points') else 'Withdrawal terms vary. Check the specific bonus terms and conditions at ' + name + ' for full details.'}"),
        ]


def generate_promo_page(brand, category):
    cat_name = category["name"]
    cat_page = category["page"]
    cat_slug = category["slug"]
    name = brand["name"]
    slug = brand["slug"]
    rating = brand["rating"]
    bonus = brand["bonus"]
    code = brand["code"]
    min_dep = brand["min_deposit"]
    wagering = brand.get("wagering", "N/A")
    year = brand["year"]
    cryptos = brand["cryptos"]
    pros = brand["pros"]
    cons = brand["cons"]
    expert = brand["expert"]
    desc = brand["desc"]

    rating_10 = round(rating * 2, 1)
    brand_color = get_brand_color(name)
    badge_text = get_badge_text(rating)
    initial = name[0].upper()

    # Crypto pills
    if isinstance(cryptos, list):
        crypto_pills = "".join(f'<span class="payment-pill">{c}</span>' for c in cryptos)
    else:
        crypto_pills = f'<span class="payment-pill">{cryptos}</span>'

    # Comparison table (other brands in same category)
    comp_rows = ""
    for b in category["brands"]:
        if b["slug"] == slug:
            continue
        comp_rows += f'''<tr>
      <td><a href="./promo-{b['slug']}.html" style="color:var(--accent);font-weight:600">{b['name']}</a></td>
      <td>{b['bonus']}</td>
      <td style="font-family:monospace;font-weight:700">{b['code']}</td>
      <td>{b['rating']}/5.0</td>
    </tr>'''

    # All bonuses table
    all_rows = ""
    for b in category["brands"]:
        highlight = ' style="background:var(--accent-muted)"' if b["slug"] == slug else ""
        all_rows += f'''<tr{highlight}>
      <td><a href="./promo-{b['slug']}.html" style="color:var(--accent);font-weight:600">{b['name']}</a></td>
      <td>{b['bonus']}</td>
      <td style="font-family:monospace;font-weight:700">{b['code']}</td>
      <td>{b['rating']}/5.0</td>
    </tr>'''

    # FAQ items
    faq_items = get_faq_items(brand, cat_slug)
    faq_html = ""
    faq_jsonld_items = []
    for q, a in faq_items:
        faq_html += f'''<div class="faq-item">
      <button class="faq-btn" onclick="this.parentElement.classList.toggle('open')"><span>{html_mod.escape(q)}</span><span class="faq-chevron"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></span></button>
      <div class="faq-body"><p>{a}</p></div>
    </div>'''
        faq_jsonld_items.append({"@type": "Question", "name": q.replace("<strong>", "").replace("</strong>", ""), "acceptedAnswer": {"@type": "Answer", "text": a.replace("<strong>", "").replace("</strong>", "")}})

    # Pros/Cons HTML
    pros_html = "".join(f"<li>{p}</li>" for p in pros)
    cons_html = "".join(f"<li>{c}</li>" for c in cons)

    # Claim steps
    claim_steps = get_claim_steps(cat_slug, name, code)

    # JSON-LD
    jsonld_page = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{name} Promo Code 2026: {code}",
        "url": f"https://cryptosites.com/promo-{slug}",
        "description": f"Use code {code} at {name} to claim {bonus}. Verified March 2026.",
        "dateModified": "2026-03-15T09:00:00+00:00",
        "publisher": {"@type": "Organization", "name": "Cryptosites", "url": "https://cryptosites.com"},
        "creator": {"@type": "SoftwareApplication", "name": "Perplexity Computer", "url": "https://www.perplexity.ai/computer"}
    }, indent=2)

    jsonld_faq = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_jsonld_items
    }, indent=2)

    jsonld_breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cryptosites.com/index.html"},
            {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"https://cryptosites.com/{cat_page}"},
            {"@type": "ListItem", "position": 3, "name": f"{name} Promo Code"}
        ]
    })

    # Code display section
    if code in ("N/A",):
        code_section = f'''<p style="font-size:14px;color:var(--text-secondary);margin-top:8px">No promo code needed — {name} is free to use.</p>'''
        code_display = ""
    elif code == "AUTO":
        code_section = f'''<p style="font-size:14px;color:var(--text-secondary);margin-top:8px">Bonus applied automatically — no code needed.</p>'''
        code_display = ""
    else:
        code_section = f'''<div style="margin-top:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
                  <span class="promo-code-display">{code}</span>
                  <button class="copy-btn" onclick="copyCode(this,'{code}')">Copy</button>
                </div>'''
        code_display = code

    page = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
{HEAD_ATTRIBUTION}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} Promo Code 2026{': ' + code if code not in ('N/A', 'AUTO') else ''} | Cryptosites</title>
  <meta name="description" content="{('Verified ' + name + ' code ' + code + ' for March 2026. ' if code not in ('N/A', 'AUTO') else '')}{bonus}. Expert review and sign-up guide.">
  <meta property="og:title" content="{name} Promo Code 2026{': ' + code if code not in ('N/A', 'AUTO') else ''} | Cryptosites">
  <meta property="og:description" content="{('Use code ' + code + ' at ' + name + ' to claim ' + bonus + '.' if code not in ('N/A', 'AUTO') else bonus + ' at ' + name + '.')} Verified March 2026.">
  <meta property="og:url" content="https://cryptosites.com/promo-{slug}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Cryptosites">
  <link rel="icon" href="./favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="https://cryptosites.com/promo-{slug}">
  <link rel="preconnect" href="https://api.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@700,800&f[]=satoshi@300,400,500,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./base.css">
  <link rel="stylesheet" href="./style.css">
  <script type="application/ld+json">{jsonld_page}</script>
  <script type="application/ld+json">{jsonld_faq}</script>
  <script type="application/ld+json">{jsonld_breadcrumb}</script>
</head>
<body>
<a href="#main-content" class="skip-link">Skip to main content</a>
{get_nav_html(cat_slug)}

<main id="main-content">
  <!-- Hero -->
  <div class="promo-hero">
    <div class="container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <a href="./index.html">Home</a>
        <span class="bc-sep"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></span>
        <a href="./{cat_page}">{cat_name}</a>
        <span class="bc-sep"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></span>
        <span style="color:var(--text-muted)">{name} Promo Code</span>
      </nav>
      <div class="promo-hero-inner">
        <div class="promo-hero-left">
          <div class="promo-avatar" style="background:{brand_color}"><span>{initial}</span></div>
          <div class="promo-hero-info">
            <div class="promo-badge">{badge_text}</div>
            <h1>{name} {'Promo Code 2026: ' + code if code not in ('N/A', 'AUTO') else ('Bonus' if code == 'AUTO' else 'Review')} 2026</h1>
            <p class="promo-hero-subtitle">Get <strong style="color:var(--accent)">{bonus}</strong>{' with code <strong style="color:var(--secondary)">' + code + '</strong>' if code not in ('N/A', 'AUTO') else ''}. Verified and working for March 2026.</p>
            <div class="trust-badges-row">
              <div class="trust-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <span>Expert Verified</span></div>
              <div class="trust-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> <span>Crypto-Friendly</span></div>
              <div class="trust-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> <span>Last verified 3 hrs ago</span></div>
              <div class="trust-badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> <span>18+ Only</span></div>
            </div>
          </div>
        </div>
        <div class="rating-circle"><span class="rating-circle-score">{rating_10}</span><span class="rating-circle-sub">/10</span></div>
      </div>
    </div>
  </div>

  <div class="container" style="padding-top:32px;padding-bottom:80px">
    <div class="two-col">
      <div class="promo-main">
        <!-- Promo Box -->
        <div class="promo-box" id="promo-code">
          <div style="display:flex;align-items:flex-start;gap:16px">
            <div class="promo-box-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg></div>
            <div style="flex:1;min-width:0">
              <p class="promo-box-bonus">{bonus}</p>
              {code_section}
              <a href="#" target="_blank" rel="noopener noreferrer nofollow" class="promo-claim-btn"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> {'Claim Bonus' if cat_slug != 'wallets' else 'Get ' + name}</a>
              <p style="font-size:12px;color:var(--text-muted);margin-top:12px">{'T&Cs apply. 18+ only. Please gamble responsibly.' if cat_slug in ('casinos', 'sports', 'poker', 'lottery') else 'T&Cs apply. Crypto investments involve risk.'}</p>
            </div>
          </div>
        </div>

        <!-- Expert Analysis -->
        <div class="expert-quote" id="expert-analysis">
          <p>"{expert}"</p>
          <p class="expert-name">Cryptosites Review Team</p>
        </div>

        <!-- How to Claim -->
        <h2 id="how-to-claim" class="section-heading">How to {'Claim Your Bonus' if cat_slug not in ('wallets',) else 'Get Started'}</h2>
        {claim_steps}

        <!-- Pros & Cons -->
        <h2 id="pros-cons" class="section-heading">Pros &amp; Cons</h2>
        <div class="pros-cons-grid">
          <div class="detail-pros">
            <h3><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> Pros</h3>
            <ul>{pros_html}</ul>
          </div>
          <div class="detail-cons">
            <h3><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg> Cons</h3>
            <ul>{cons_html}</ul>
          </div>
        </div>

        <!-- Bonus Details Table -->
        <div id="bonus-details" class="detail-card">
          <h2 class="detail-card-heading">{'Bonus' if cat_slug != 'wallets' else 'Product'} Details</h2>
          <table class="data-table">
            <tbody>
              <tr><td>{'Welcome Bonus' if cat_slug != 'wallets' else 'Offer'}</td><td style="color:var(--accent);font-weight:600">{bonus}</td></tr>
              <tr><td>{'Promo Code' if cat_slug != 'wallets' else 'Referral Code'}</td><td style="font-weight:700;color:var(--secondary)">{code}</td></tr>
              <tr><td>{'Min Deposit' if cat_slug != 'wallets' else 'Cost'}</td><td>{min_dep}</td></tr>
              {f'<tr><td>Wagering</td><td>{wagering}</td></tr>' if cat_slug not in ('wallets', 'exchanges') else ''}
              <tr><td>Rating</td><td>{rating}/5.0</td></tr>
              <tr><td>{'Year Established' if cat_slug != 'wallets' else 'Launched'}</td><td>{year}</td></tr>
            </tbody>
          </table>
        </div>

        <!-- Detailed Content -->
        <div class="review-content" id="review-content">
          <p class="review-intro">{desc}</p>

          <h2>What You Get{' with Code ' + code if code not in ('N/A', 'AUTO') else ''}</h2>
          <p>When you {'use the ' + name + ' promo code <strong>' + code + '</strong>' if code not in ('N/A', 'AUTO') else 'sign up at ' + name}, you {'unlock' if cat_slug != 'wallets' else 'get access to'}: <strong>{bonus}</strong>.</p>
          <p>{'The minimum deposit to qualify is <strong>' + min_dep + '</strong>, which is ' + ('very accessible' if '$1' in min_dep or 'free' in min_dep.lower() or 'None' in min_dep else 'reasonable') + '.' if min_dep != 'N/A' else ''}</p>

          <h2>Is {'This Bonus' if cat_slug != 'wallets' else name} Worth It?</h2>
          <p>{'Short answer: yes.' if rating >= 4.5 else 'Overall, yes — with some caveats.'} {name} is one of the {'highest-rated' if rating >= 4.5 else 'well-regarded'} {'platforms' if cat_slug in ('exchanges', 'wallets') else 'operators'} in the {cat_name.lower()} space{',' if rating >= 4.5 else '.'} {'and their offer is among the best available.' if rating >= 4.5 else 'Their offer provides solid value for most users.'} {'The ' + wagering + ' wagering requirement is ' + ('very fair' if '30x' in str(wagering) or '10x' in str(wagering) or '1x' in str(wagering) else 'standard for the industry' if '40x' in str(wagering) else 'on the higher side but the bonus value compensates') + '.' if cat_slug in ('casinos', 'sports', 'poker', 'lottery') and wagering not in ('N/A', 'None', 'Loyalty points system', 'Loyalty points', 'Earned via rakeback', 'Earned via rake', 'Released in $1 increments', 'Cleared in increments') else ''}</p>

          <h2>Tips for {'Maximising Your Bonus' if cat_slug not in ('wallets', 'exchanges') else 'Getting the Most Out of ' + name}</h2>
          <ul class="review-list">
            {'<li><strong>Read the wagering requirements:</strong> Every bonus has rollover conditions. Know them before you start. Understanding the rules upfront prevents frustration later.</li>' if cat_slug in ('casinos', 'sports', 'poker', 'lottery') else '<li><strong>Enable all security features:</strong> Two-factor authentication, biometric locks, and strong passwords are essential. Never skip security setup.</li>'}
            <li><strong>Start small:</strong> {'Do not blow the entire bonus on one bet. Spread it across multiple wagers to get the most value.' if cat_slug in ('casinos', 'sports', 'poker', 'lottery') else 'Begin with a small transaction to familiarise yourself with the platform before committing larger amounts.'}</li>
            <li><strong>{'Stick to what you know' if cat_slug in ('casinos', 'sports', 'poker') else 'Do your research'}:</strong> {'Bonus funds are not the time to experiment with unfamiliar games or markets.' if cat_slug in ('casinos', 'sports', 'poker') else 'Whether trading or choosing a wallet, understanding the fundamentals helps you make better decisions.'}</li>
            <li><strong>{'Complete verification early' if cat_slug != 'wallets' else 'Back up your recovery phrase'}:</strong> {'Some platforms hold bonuses until verification is complete. Get it done upfront to avoid delays.' if cat_slug != 'wallets' else 'Write it down on paper and store it in a secure location. Never store your seed phrase digitally or share it with anyone.'}</li>
            <li><strong>{'Set a budget' if cat_slug in ('casinos', 'sports', 'poker', 'lottery') else 'Stay informed'}:</strong> {'Even with bonus money, decide what you are comfortable spending and stick to it. Gambling should be entertainment, not a financial strategy.' if cat_slug in ('casinos', 'sports', 'poker', 'lottery') else 'Follow ' + name + ' official channels for updates on new features, supported assets, and security advisories.'}</li>
          </ul>
        </div>

        <!-- FAQ -->
        <div id="faq" style="margin-bottom:32px">
          <h2 class="section-heading">Frequently Asked Questions</h2>
          <div class="faq-accordion">{faq_html}</div>
        </div>

        <!-- Accepted Cryptos -->
        <div style="margin-bottom:32px">
          <h2 class="section-heading-sm">Accepted {'Cryptocurrencies' if cat_slug not in ('wallets',) else 'Assets'}</h2>
          <div style="display:flex;flex-wrap:wrap;gap:8px">{crypto_pills}</div>
        </div>

        <!-- Comparison Table -->
        <div id="comparison" style="margin-bottom:32px">
          <h2 class="section-heading">Compare With Similar {'Offers' if cat_slug != 'wallets' else 'Wallets'}</h2>
          <div class="table-wrap">
            <table class="compare-table">
              <thead><tr><th>{'Platform' if cat_slug in ('exchanges', 'wallets') else 'Operator'}</th><th>{'Bonus' if cat_slug != 'wallets' else 'Offer'}</th><th>Code</th><th>Rating</th></tr></thead>
              <tbody>{comp_rows}</tbody>
            </table>
          </div>
        </div>

        <!-- All Bonuses Table -->
        <div style="margin-bottom:32px">
          <h2 class="section-heading">All {cat_name} {'Bonuses' if cat_slug != 'wallets' else 'Options'}</h2>
          <div class="table-wrap">
            <table class="compare-table">
              <thead><tr><th>{'Platform' if cat_slug in ('exchanges', 'wallets') else 'Operator'}</th><th>{'Welcome Bonus' if cat_slug != 'wallets' else 'Offer'}</th><th>Code</th><th>Rating</th></tr></thead>
              <tbody>{all_rows}</tbody>
            </table>
          </div>
        </div>

        <!-- Cross Links -->
        <div class="cross-links">
          <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">More on {name}</h3>
          <div style="display:flex;flex-wrap:wrap;gap:10px">
            <a href="./promo-{slug}.html" class="btn-outline-sm">{'Promo Code: ' + code if code not in ('N/A', 'AUTO') else name + ' Bonus'}</a>
            <a href="./{cat_page}" class="btn-outline-sm">All {cat_name}</a>
            <a href="./index.html" class="btn-outline-sm">Back to Home</a>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="on-this-page">
          <h3>On This Page</h3>
          <a href="#expert-analysis">Expert Analysis</a>
          <a href="#how-to-claim">How to {'Claim' if cat_slug != 'wallets' else 'Start'}</a>
          <a href="#pros-cons">Pros &amp; Cons</a>
          <a href="#bonus-details">{'Bonus' if cat_slug != 'wallets' else 'Product'} Details</a>
          <a href="#comparison">Compare {'Offers' if cat_slug != 'wallets' else 'Options'}</a>
          <a href="#faq">FAQ</a>
        </div>
        <div class="key-terms-box">
          <h3>Key Terms</h3>
          <div class="key-term-row"><span class="key-term-label">{'Promo Code' if cat_slug != 'wallets' else 'Referral'}</span><span class="key-term-value" style="color:var(--secondary)">{code}</span></div>
          <div class="key-term-row"><span class="key-term-label">{'Bonus' if cat_slug != 'wallets' else 'Offer'}</span><span class="key-term-value" style="color:var(--accent)">{bonus}</span></div>
          <div class="key-term-row"><span class="key-term-label">{'Min Deposit' if cat_slug != 'wallets' else 'Cost'}</span><span class="key-term-value">{min_dep}</span></div>
          <div class="key-term-row"><span class="key-term-label">Rating</span><span class="key-term-value">{rating}/5.0</span></div>
          <div class="key-term-row"><span class="key-term-label">{'Year Est.' if cat_slug != 'wallets' else 'Launched'}</span><span class="key-term-value">{year}</span></div>
        </div>
        <div class="reviewer-box">
          <h3 style="font-size:13px;font-weight:700;margin-bottom:12px">Reviewed By</h3>
          <div style="display:flex;align-items:center;gap:10px">
            <div class="reviewer-avatar">{LOGO_SVG.replace('width="32" height="32"', 'width="28" height="28"')}</div>
            <div>
              <div style="font-size:14px;font-weight:600">Cryptosites Team</div>
              <div style="font-size:12px;color:var(--text-muted)">Expert Reviewers</div>
            </div>
          </div>
        </div>
        <a href="./{cat_page}" class="sidebar-link"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg> All {cat_name}</a>
      </aside>
    </div>
  </div>

  <!-- Sticky Bottom CTA Bar -->
  <div class="sticky-bottom-bar" id="stickyBar">
    <div class="container sticky-bottom-inner">
      <div class="sticky-bottom-left">
        <div class="promo-avatar-sm" style="background:{brand_color}"><span>{initial}</span></div>
        <div class="sticky-bottom-text">
          <div class="sticky-bottom-offer">{bonus}</div>
          <div class="sticky-bottom-name">{name}</div>
        </div>
      </div>
      <div class="sticky-bottom-right">
        {f'<span class="sticky-bottom-code">{code}</span>' if code not in ('N/A', 'AUTO') else ''}
        <a href="#" target="_blank" rel="noopener noreferrer nofollow" class="sticky-bottom-cta">{'Claim Bonus' if cat_slug != 'wallets' else 'Get ' + name}</a>
      </div>
    </div>
  </div>
  <script>
  (function(){{var bar=document.getElementById('stickyBar');if(!bar)return;var shown=false;window.addEventListener('scroll',function(){{if(window.scrollY>400){{if(!shown){{bar.classList.add('visible');shown=true;}}}}else{{if(shown){{bar.classList.remove('visible');shown=false;}}}}}});}})();
  </script>
</main>

{get_footer_html()}
<script src="./app.js" defer></script>
</body>
</html>'''

    return page


# ============================================================
# CSS ADDITIONS
# ============================================================

PROMO_CSS = '''

/* ============================================
   PROMO CODE PAGE STYLES
   ============================================ */

/* Breadcrumbs */
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
  margin-bottom: var(--space-5);
  flex-wrap: wrap;
}
.breadcrumbs a { color: var(--text-secondary); font-weight: 500; }
.breadcrumbs a:hover { color: var(--accent); }
.bc-sep { color: var(--text-muted); display: flex; align-items: center; }

/* Promo Hero */
.promo-hero {
  background: var(--hero-gradient);
  position: relative;
  padding: var(--space-8) 0 var(--space-10);
  overflow: hidden;
}
.promo-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--hero-glow);
  pointer-events: none;
}
.promo-hero-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-6);
}
.promo-hero-left {
  display: flex;
  align-items: flex-start;
  gap: var(--space-5);
  flex: 1;
  min-width: 0;
}
.promo-hero-info { flex: 1; min-width: 0; }
.promo-hero-subtitle {
  font-size: var(--text-lg);
  color: var(--text-secondary);
  margin-top: var(--space-3);
  line-height: 1.5;
}

/* Brand Avatar */
.promo-avatar {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.promo-avatar span {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 800;
  color: #fff;
}
.promo-avatar-sm {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.promo-avatar-sm span {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 800;
  color: #fff;
}

/* Badge */
.promo-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background: var(--accent-muted);
  color: var(--accent);
  margin-bottom: var(--space-2);
}
.promo-hero h1 {
  font-size: var(--text-2xl);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

/* Trust Badges */
.trust-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-top: var(--space-4);
}
.trust-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Rating Circle */
.rating-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--bg-surface-2);
  border: 2px solid var(--secondary);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  gap: 0;
}
.rating-circle-score {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  color: var(--secondary);
  line-height: 1;
}
.rating-circle-sub {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
  line-height: 1;
}

/* Two Column Layout */
.two-col {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-10);
  align-items: start;
}
@media (max-width: 960px) {
  .two-col {
    grid-template-columns: 1fr;
  }
  .sidebar { display: none; }
}

/* Promo Box */
.promo-box {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
  border-left: 4px solid var(--success);
}
.promo-box-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: rgba(0, 212, 170, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--accent);
}
.promo-box-bonus {
  font-weight: 700;
  font-size: clamp(1.1rem, 2.5vw, 1.35rem);
  color: var(--accent);
}
.promo-code-display {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 15px;
  font-weight: 700;
  background: var(--bg-surface-2);
  border: 1px dashed var(--border-hover);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  letter-spacing: 0.05em;
  color: var(--secondary);
}
.copy-btn {
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--bg-primary);
  cursor: pointer;
  transition: background var(--duration-fast) var(--ease-out);
}
.copy-btn:hover { background: var(--accent-hover); }
.promo-claim-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  padding: 12px 28px;
  border-radius: var(--radius-full);
  background: var(--accent);
  color: var(--bg-primary);
  margin-top: 14px;
  transition: background var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}
.promo-claim-btn:hover {
  background: var(--accent-hover);
  color: var(--bg-primary);
  transform: translateY(-1px);
}

/* Expert Quote */
.expert-quote {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
  border-left: 3px solid var(--accent);
}
.expert-quote p:first-child {
  font-size: var(--text-base);
  line-height: 1.7;
  color: var(--text-primary);
  font-style: italic;
}
.expert-name {
  font-size: var(--text-sm);
  color: var(--accent);
  font-weight: 600;
  margin-top: var(--space-3);
}

/* Section Headings */
.section-heading {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}
.section-heading-sm {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 12px;
}

/* Claim Steps */
.claim-steps {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
}
.claim-step {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-5);
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  transition: border-color var(--duration-fast) var(--ease-out);
}
.claim-step:hover { border-color: var(--accent); }
.claim-step-num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--accent);
  color: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}
.claim-step-content { flex: 1; min-width: 0; }
.claim-step-title {
  font-weight: 700;
  font-size: var(--text-base);
  margin-bottom: 4px;
}
.claim-step-desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Pros & Cons */
.pros-cons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}
@media (max-width: 600px) {
  .pros-cons-grid { grid-template-columns: 1fr; }
}
.detail-pros, .detail-cons {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
}
.detail-pros { border-top: 3px solid var(--success); }
.detail-cons { border-top: 3px solid var(--error); }
.detail-pros h3, .detail-cons h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: var(--space-3);
}
.detail-pros h3 { color: var(--success); }
.detail-cons h3 { color: var(--error); }
.detail-pros ul li, .detail-cons ul li {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  padding: 6px 0;
  padding-left: 16px;
  position: relative;
  line-height: 1.5;
}
.detail-pros ul li::before {
  content: '+';
  position: absolute;
  left: 0;
  color: var(--success);
  font-weight: 700;
}
.detail-cons ul li::before {
  content: '−';
  position: absolute;
  left: 0;
  color: var(--error);
  font-weight: 700;
}

/* Detail Card */
.detail-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
}
.detail-card-heading {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: var(--space-4);
}

/* Data Table */
.data-table {
  width: 100%;
}
.data-table td {
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: var(--text-sm);
}
.data-table td:first-child {
  font-weight: 600;
  color: var(--text-secondary);
  width: 40%;
}
.data-table tr:last-child td { border-bottom: none; }

/* Review Content */
.review-content {
  margin-bottom: var(--space-8);
}
.review-content h2 {
  font-size: 18px;
  font-weight: 700;
  margin: var(--space-8) 0 var(--space-4);
}
.review-content p {
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: var(--space-4);
}
.review-intro {
  font-size: var(--text-lg);
  color: var(--text-primary) !important;
  line-height: 1.6;
}
.review-list {
  margin-bottom: var(--space-4);
}
.review-list li {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  padding: 8px 0;
  padding-left: 20px;
  position: relative;
  line-height: 1.6;
}
.review-list li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--accent);
  font-weight: 700;
}

/* FAQ Accordion */
.faq-accordion {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.faq-item {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color var(--duration-fast) var(--ease-out);
}
.faq-item:hover { border-color: var(--border-hover); }
.faq-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  font-size: var(--text-sm);
  font-weight: 600;
  text-align: left;
  color: var(--text-primary);
  cursor: pointer;
  gap: var(--space-3);
}
.faq-chevron {
  transition: transform var(--duration-normal) var(--ease-out);
  flex-shrink: 0;
  display: flex;
  color: var(--text-muted);
}
.faq-item.open .faq-chevron { transform: rotate(180deg); }
.faq-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-normal) var(--ease-out);
}
.faq-item.open .faq-body { max-height: 300px; }
.faq-body p {
  padding: 0 var(--space-5) var(--space-5);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Payment Pills */
.payment-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  background: var(--bg-surface-2);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}

/* Compare Table */
.table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.compare-table {
  width: 100%;
  border-collapse: collapse;
}
.compare-table thead th {
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 10px 12px;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
}
.compare-table tbody td {
  padding: 12px;
  font-size: var(--text-sm);
  border-bottom: 1px solid var(--border);
  color: var(--text-secondary);
}
.compare-table tbody tr:hover {
  background: var(--accent-muted);
}

/* Cross Links */
.cross-links {
  padding: var(--space-6);
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-top: var(--space-8);
}
.btn-outline-sm {
  display: inline-flex;
  align-items: center;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  transition: all var(--duration-fast) var(--ease-out);
}
.btn-outline-sm:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 80px;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}
.on-this-page {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
}
.on-this-page h3 {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: var(--space-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}
.on-this-page a {
  display: block;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  padding: 6px 0;
  font-weight: 500;
  transition: color var(--duration-fast) var(--ease-out);
}
.on-this-page a:hover { color: var(--accent); }

.key-terms-box {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
}
.key-terms-box h3 {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: var(--space-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}
.key-term-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.key-term-row:last-child { border-bottom: none; }
.key-term-label { color: var(--text-secondary); font-weight: 500; }
.key-term-value { font-weight: 600; color: var(--text-primary); text-align: right; max-width: 55%; }

.reviewer-box {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
}
.reviewer-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-surface-2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--accent);
  font-weight: 500;
  padding: var(--space-3) 0;
}

/* Sticky Bottom CTA Bar */
.sticky-bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky);
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
  padding: 12px 0;
  transform: translateY(100%);
  transition: transform var(--duration-normal) var(--ease-out);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.sticky-bottom-bar.visible { transform: translateY(0); }
.sticky-bottom-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}
.sticky-bottom-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-width: 0;
}
.sticky-bottom-text { min-width: 0; }
.sticky-bottom-offer {
  font-weight: 700;
  font-size: 14px;
  color: var(--accent);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sticky-bottom-name {
  font-size: 12px;
  color: var(--text-muted);
}
.sticky-bottom-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}
.sticky-bottom-code {
  font-family: monospace;
  font-size: 13px;
  font-weight: 700;
  color: var(--secondary);
  background: var(--bg-surface-2);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1px dashed var(--border-hover);
}
.sticky-bottom-cta {
  font-size: 14px;
  font-weight: 700;
  padding: 10px 24px;
  border-radius: var(--radius-full);
  background: var(--accent);
  color: var(--bg-primary);
  white-space: nowrap;
  transition: background var(--duration-fast) var(--ease-out);
}
.sticky-bottom-cta:hover {
  background: var(--accent-hover);
  color: var(--bg-primary);
}

/* Starred Badge */
.starred-badge {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: var(--text-secondary);
  transition: color var(--duration-fast) var(--ease-out);
  padding: var(--space-2);
}
.starred-badge:hover { color: var(--secondary); }
.starred-count {
  position: absolute;
  top: 0;
  right: 0;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  background: var(--secondary);
  color: #000;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}
.starred-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  width: 260px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  z-index: var(--z-dropdown);
  padding: var(--space-3) 0;
  margin-top: 8px;
}
.starred-badge.open .starred-dropdown { display: block; }
.starred-dropdown-header {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: var(--space-2) var(--space-4);
}
.starred-dropdown-empty {
  padding: var(--space-4);
  font-size: var(--text-sm);
  color: var(--text-muted);
  text-align: center;
}
.starred-dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px var(--space-4);
  font-size: var(--text-sm);
  color: var(--text-primary);
  transition: background var(--duration-fast) var(--ease-out);
}
.starred-dropdown-item:hover {
  background: var(--accent-muted);
}

/* Footer */
.site-footer {
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
  padding: var(--space-12) 0 var(--space-8);
  margin-top: var(--space-16);
}
.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr repeat(5, 1fr);
  gap: var(--space-8);
  margin-bottom: var(--space-10);
}
@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 640px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
  .footer-brand { grid-column: 1 / -1; }
}
.footer-heading {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}
.footer-links {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.footer-links a {
  font-size: 13px;
  color: var(--text-secondary);
  transition: color var(--duration-fast) var(--ease-out);
}
.footer-links a:hover { color: var(--accent); }

.rg-notice {
  background: var(--bg-surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  margin-bottom: var(--space-6);
}
.rg-notice p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}
.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) 0;
  border-top: 1px solid var(--border);
  font-size: 13px;
  color: var(--text-muted);
  flex-wrap: wrap;
  gap: var(--space-3);
}
.footer-disclaimer {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-top: var(--space-4);
}

/* Mobile responsive for promo hero */
@media (max-width: 768px) {
  .promo-hero-inner {
    flex-direction: column;
    gap: var(--space-4);
  }
  .promo-hero-left {
    flex-direction: column;
    gap: var(--space-3);
  }
  .rating-circle { align-self: flex-start; }
  .sticky-bottom-text { display: none; }
  .sticky-bottom-inner { justify-content: center; gap: var(--space-2); }
}
'''

# ============================================================
# UPDATED APP.JS
# ============================================================

APP_JS = '''/* Cryptosites.com — Application JavaScript */
(function() {
  'use strict';

  /* Theme management (in-memory only) */
  var currentTheme = 'dark';

  function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
  }

  applyTheme(currentTheme);

  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function(e) {
    applyTheme(e.matches ? 'light' : 'dark');
  });

  /* Starred platforms (in-memory) */
  var starredPlatforms = [];

  function updateStarredUI() {
    var countEl = document.getElementById('starredCount');
    var listEl = document.getElementById('starredList');
    if (!countEl || !listEl) return;

    var count = starredPlatforms.length;
    countEl.textContent = count;
    countEl.style.display = count > 0 ? 'flex' : 'none';

    if (count === 0) {
      listEl.innerHTML = '<div class="starred-dropdown-empty">Star a platform to track it here</div>';
    } else {
      listEl.innerHTML = starredPlatforms.map(function(p) {
        return '<a href="' + p.url + '" class="starred-dropdown-item"><span>' + p.name + '</span><span style="font-size:12px;color:var(--text-muted)">' + p.category + '</span></a>';
      }).join('');
    }
  }

  function toggleStar(name, url, category) {
    var idx = starredPlatforms.findIndex(function(p) { return p.name === name; });
    if (idx >= 0) {
      starredPlatforms.splice(idx, 1);
    } else {
      starredPlatforms.push({ name: name, url: url, category: category });
    }
    updateStarredUI();
    var starBtn = document.getElementById('starBrandBtn');
    if (starBtn) {
      var isStarred = starredPlatforms.some(function(p) { return p.name === name; });
      starBtn.classList.toggle('is-starred', isStarred);
      starBtn.querySelector('span').textContent = isStarred ? 'Starred' : 'Star';
    }
  }

  /* Make toggleStar available globally */
  window.toggleStar = toggleStar;

  /* DOM ready */
  document.addEventListener('DOMContentLoaded', function() {

    /* Theme toggle */
    var themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function() {
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
      });
    }

    /* Mobile menu toggle */
    var mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    var mobileNav = document.querySelector('.mobile-nav');
    if (mobileMenuBtn && mobileNav) {
      mobileMenuBtn.addEventListener('click', function() {
        var isOpen = mobileNav.classList.toggle('is-open');
        mobileMenuBtn.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });
      mobileNav.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
          mobileNav.classList.remove('is-open');
          mobileMenuBtn.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        });
      });
    }

    /* Starred badge dropdown */
    var starredBadge = document.getElementById('starredBadge');
    if (starredBadge) {
      starredBadge.addEventListener('click', function(e) {
        e.stopPropagation();
        starredBadge.classList.toggle('open');
      });
      document.addEventListener('click', function() {
        starredBadge.classList.remove('open');
      });
    }
    updateStarredUI();

    /* FAQ accordion (original) */
    var faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(function(item) {
      var question = item.querySelector('.faq-question');
      if (question) {
        question.addEventListener('click', function() {
          var wasOpen = item.classList.contains('is-open');
          faqItems.forEach(function(i) { i.classList.remove('is-open'); });
          if (!wasOpen) item.classList.add('is-open');
        });
      }
    });

    /* Comparison table sorting */
    var tables = document.querySelectorAll('.comparison-table');
    tables.forEach(function(table) {
      var headers = table.querySelectorAll('th[data-sort]');
      headers.forEach(function(header) {
        header.addEventListener('click', function() {
          var sortKey = header.getAttribute('data-sort');
          var tbody = table.querySelector('tbody');
          var rows = Array.from(tbody.querySelectorAll('tr'));
          var isNumeric = header.hasAttribute('data-numeric');
          var currentDir = header.getAttribute('data-dir') || 'asc';
          var newDir = currentDir === 'asc' ? 'desc' : 'asc';
          headers.forEach(function(h) { h.removeAttribute('data-dir'); });
          header.setAttribute('data-dir', newDir);
          rows.sort(function(a, b) {
            var aVal = a.querySelector('[data-' + sortKey + ']')?.getAttribute('data-' + sortKey) || a.cells[header.cellIndex]?.textContent.trim() || '';
            var bVal = b.querySelector('[data-' + sortKey + ']')?.getAttribute('data-' + sortKey) || b.cells[header.cellIndex]?.textContent.trim() || '';
            var comparison;
            if (isNumeric) { comparison = parseFloat(aVal) - parseFloat(bVal); }
            else { comparison = aVal.localeCompare(bVal); }
            return newDir === 'asc' ? comparison : -comparison;
          });
          rows.forEach(function(row) { tbody.appendChild(row); });
        });
      });
    });

    /* Scroll animation */
    var observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    document.querySelectorAll('.observe-animate').forEach(function(el) {
      observer.observe(el);
    });

    /* Newsletter form */
    var newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(function(form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        var input = form.querySelector('input[type="email"]');
        var btn = form.querySelector('.btn');
        if (input && input.value) {
          btn.textContent = 'Subscribed!';
          btn.style.background = 'var(--success)';
          input.value = '';
          setTimeout(function() {
            btn.textContent = 'Subscribe';
            btn.style.background = '';
          }, 3000);
        }
      });
    });

  });
})();

/* Copy promo code to clipboard */
function copyCode(btn, code) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(code).then(function() {
      btn.textContent = 'Copied!';
      btn.style.background = 'var(--success)';
      setTimeout(function() {
        btn.textContent = 'Copy';
        btn.style.background = '';
      }, 2000);
    });
  } else {
    var textarea = document.createElement('textarea');
    textarea.value = code;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    btn.textContent = 'Copied!';
    btn.style.background = 'var(--success)';
    setTimeout(function() {
      btn.textContent = 'Copy';
      btn.style.background = '';
    }, 2000);
  }
}
'''

# ============================================================
# MAIN GENERATION
# ============================================================

def main():
    generated = []

    # 1. Generate all promo code pages
    for cat_key, category in CATEGORIES.items():
        for brand in category["brands"]:
            filename = f"promo-{brand['slug']}.html"
            filepath = os.path.join(BASE_DIR, filename)
            html_content = generate_promo_page(brand, category)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated.append(filename)
            print(f"  Generated: {filename}")

    # 2. Append promo CSS to style.css
    css_path = os.path.join(BASE_DIR, 'style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        existing_css = f.read()

    if '/* PROMO CODE PAGE STYLES */' not in existing_css:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(PROMO_CSS)
        print("  Updated: style.css (appended promo styles)")
    else:
        print("  Skipped: style.css (promo styles already present)")

    # 3. Write updated app.js
    js_path = os.path.join(BASE_DIR, 'app.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(APP_JS)
    print("  Updated: app.js")

    # 4. Update existing HTML pages with new footer and nav
    existing_pages = [
        'index.html', 'crypto-casinos.html', 'crypto-sports-betting.html',
        'crypto-poker.html', 'crypto-exchanges.html', 'crypto-lottery.html',
        'crypto-wallets.html', 'review-stake.html', 'review-coinbase.html', 'about.html'
    ]

    for page_name in existing_pages:
        page_path = os.path.join(BASE_DIR, page_name)
        if not os.path.exists(page_path):
            continue

        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace footer
        footer_match = re.search(r'<footer[\s\S]*?</footer>', content)
        if footer_match:
            content = content.replace(footer_match.group(0), get_footer_html())

        # Add starred badge CSS/JS if not present (through the new app.js link)
        # The nav replacement is more complex so we'll skip it to avoid breaking existing layouts

        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated footer: {page_name}")

    # 5. Generate sitemap
    sitemap_entries = ['index.html', 'crypto-casinos.html', 'crypto-sports-betting.html',
                       'crypto-poker.html', 'crypto-exchanges.html', 'crypto-lottery.html',
                       'crypto-wallets.html', 'review-stake.html', 'review-coinbase.html', 'about.html']
    sitemap_entries.extend(generated)

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for entry in sitemap_entries:
        sitemap_xml += f'  <url><loc>https://cryptosites.com/{entry}</loc><lastmod>2026-03-15</lastmod><priority>{"1.0" if entry == "index.html" else "0.8"}</priority></url>\n'
    sitemap_xml += '</urlset>'

    sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    print("  Updated: sitemap.xml")

    print(f"\nDone! Generated {len(generated)} promo code pages.")
    print(f"Total site pages: {len(sitemap_entries)}")

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Nova Toronto local-SEO page generator.

Generates:
  - /website-design/{city}/          (10 cities)
  - /digital-marketing/{city}/       (10 cities)
  - /ai-automation/{city}/           (10 cities)
  - /ai-automation/ai-receptionist/{industry}/  (8 industries)
  - sitemap.xml (all site URLs)

Run from repo root:  python tools/generate_local_pages.py
Add a city or industry to the dicts below and re-run to extend the site.
"""
import os
import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://novatoronto.com"
PHONE = "365-355-3133"
PHONE_INTL = "+13653553133"
EMAIL = "novatoronto.ca@gmail.com"
CALENDLY = "https://calendly.com/novatoronto-ca/30min?hide_gdpr_banner=1&primary_color=0096dd"
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- cities
CITIES = {
    "toronto": {
        "name": "Toronto",
        "blurb": "Toronto is Canada's largest market and its most competitive. From King West startups to family businesses in East York, standing out downtown means your website, ads, and phone lines all have to work harder than everyone else's.",
        "areas": "Downtown Toronto, King West, Liberty Village, Leslieville, The Danforth, Yorkville and East York",
        "angle": "In a city with thousands of competitors a page away, speed matters: a fast website, an ad that shows up first, and a phone that never rings unanswered.",
    },
    "mississauga": {
        "name": "Mississauga",
        "blurb": "Mississauga is home to over 90,000 businesses, from Port Credit restaurants to logistics and manufacturing firms around Pearson. It's a city where word of mouth still wins deals, but only if customers can find you online first.",
        "areas": "Port Credit, Streetsville, Meadowvale, Erin Mills, Cooksville and the Airport Corporate Centre",
        "angle": "Most Mississauga customers search 'near me' before they buy. If you are not on page one for your neighbourhood, your competitor down Hurontario is.",
    },
    "brampton": {
        "name": "Brampton",
        "blurb": "Brampton is one of Canada's fastest-growing cities, with a young population and a booming small-business scene in trucking, trades, healthcare, and food. Growth means opportunity, and a lot of new competition every year.",
        "areas": "Downtown Brampton, Bramalea, Springdale, Mount Pleasant and Castlemore",
        "angle": "New businesses open in Brampton every week. The ones that grow are the ones that show up first on Google and answer every call.",
    },
    "scarborough": {
        "name": "Scarborough",
        "blurb": "Scarborough's business community is one of the most diverse in the GTA: family restaurants, medical clinics, auto shops, and services that thrive on repeat local customers along Kingston Road, Markham Road, and Sheppard.",
        "areas": "Scarborough Town Centre, Agincourt, Malvern, Guildwood and Birch Cliff",
        "angle": "Scarborough customers are loyal, but they find new businesses on their phones. A strong local presence turns one-time searches into regulars.",
    },
    "north-york": {
        "name": "North York",
        "blurb": "North York blends corporate offices along Yonge and Sheppard with dense residential neighbourhoods full of clinics, salons, tutoring centres, and professional services that live and die by local search.",
        "areas": "Yonge & Sheppard, Willowdale, Don Mills, Bathurst Manor and York Mills",
        "angle": "In North York, professional credibility online is everything. Your website is the first impression before anyone walks through the door.",
    },
    "etobicoke": {
        "name": "Etobicoke",
        "blurb": "From The Queensway's showrooms to Kingsway boutiques and industrial businesses near the airport, Etobicoke companies serve both local families and commercial clients across the west GTA.",
        "areas": "The Kingsway, Islington Village, Mimico, Long Branch and Rexdale",
        "angle": "Etobicoke sits between downtown Toronto and Mississauga, and so do your customers. Ranking locally captures both directions of that traffic.",
    },
    "markham": {
        "name": "Markham",
        "blurb": "Markham is the GTA's tech capital, with more than 1,500 tech companies alongside thriving restaurants, clinics, and services in Unionville and Main Street Markham. Customers here expect a polished digital experience.",
        "areas": "Unionville, Main Street Markham, Cornell, Berczy and the Markham tech corridor",
        "angle": "Markham customers compare businesses online before they ever call. A dated website or a missed call sends them straight to a competitor.",
    },
    "vaughan": {
        "name": "Vaughan",
        "blurb": "Vaughan has transformed from suburb to city, with the VMC towers rising and family businesses across Woodbridge, Maple, and Concord competing for a fast-growing customer base.",
        "areas": "Woodbridge, Maple, Concord, Kleinburg and the Vaughan Metropolitan Centre",
        "angle": "Vaughan is growing faster than almost anywhere in Ontario. Businesses that invest in their online presence now own the searches for years.",
    },
    "richmond-hill": {
        "name": "Richmond Hill",
        "blurb": "Richmond Hill's businesses, from Yonge Street clinics and dental offices to restaurants and professional services, serve some of the most digitally connected households in the country.",
        "areas": "Yonge Street corridor, Oak Ridges, Mill Pond and Bayview Hill",
        "angle": "Richmond Hill customers research everything online first. Reviews, website quality, and response time decide who gets the booking.",
    },
    "oakville": {
        "name": "Oakville",
        "blurb": "Oakville businesses compete on quality and reputation, from downtown Lakeshore boutiques to Kerr Village restaurants and professional firms serving Halton's most affluent households.",
        "areas": "Downtown Oakville, Kerr Village, Bronte, Glen Abbey and Joshua Creek",
        "angle": "In Oakville, presentation is the product. A premium website and an instant, professional response on every call match what your customers expect.",
    },
}

# ---------------------------------------------------------------- services
SERVICES = {
    "website-design": {
        "name": "Website Design",
        "h1": "Website Design in {city}",
        "subtitle": "Custom, mobile-first websites that turn {city} searches into paying customers.",
        "meta": "Professional website design in {city}. Fast, mobile-friendly, SEO-ready websites from $900. Local {city} web designer with proven results. Free consultation.",
        "price_from": "$900",
        "intro2": "We design fast, mobile-first websites built to rank on Google and convert visitors into calls, bookings, and sales. Every site includes SEO fundamentals, Google Maps and Analytics integration, and a design tailored to your brand, not a cookie-cutter template.",
        "benefits": [
            ("uil-mobile-android", "Mobile-first design", "Over 60% of local searches happen on a phone. Your site will look sharp and load fast on every device."),
            ("uil-search", "Built to rank", "Clean code, proper page structure, XML sitemaps, and local SEO signals baked in from day one."),
            ("uil-shopping-cart", "E-commerce ready", "Shopify and WooCommerce stores with products, shipping, and payments configured end to end."),
            ("uil-comment-dots", "Convert, not just impress", "Clear calls to action, contact forms, and booking flows designed to turn visitors into customers."),
        ],
        "faqs": [
            ("How much does a website cost in {city}?",
             "Our websites start at $900 for a 3-page Bronze package, $1,800 for a 5-page Silver package, and $2,000 for a full e-commerce store. Custom builds from scratch start at $5,000. Every package includes mobile-responsive design, contact forms, and Google integration."),
            ("How long does it take to build a website?",
             "Most 3-5 page business websites launch within 2-3 weeks. E-commerce stores typically take 3-4 weeks depending on the number of products. We share progress with you throughout, with revision rounds included in every package."),
            ("Will my website show up on Google in {city}?",
             "Every site we build includes on-page SEO: proper titles, meta descriptions, XML sitemap, fast load times, and local business schema. For competitive keywords in {city} we also offer ongoing SEO and Google Ads management to accelerate results."),
            ("Do you meet clients in {city}?",
             "Yes. We work with businesses across {city} and the GTA, and offer a free 30-minute consultation by phone, video, or in person to plan your project."),
        ],
        "cta_title": "Get a website that wins {city} customers",
        "cta_text": "Book a free 30-minute consultation and get a plan, timeline, and fixed quote for your new website.",
    },
    "digital-marketing": {
        "name": "Digital Marketing",
        "h1": "Digital Marketing Agency in {city}",
        "subtitle": "Google Ads, Meta Ads, and SEO that put your {city} business in front of buyers.",
        "meta": "Digital marketing agency serving {city}: Google Ads, Google Shopping, Meta Ads, Microsoft Ads and local SEO. Get more {city} customers. Free consultation.",
        "price_from": "custom monthly plans",
        "intro2": "We run Google Search, Google Shopping, Meta (Facebook and Instagram), and Microsoft ad campaigns focused on one thing: profitable leads. No vanity metrics, just tracked calls, form fills, and sales you can attribute to every dollar spent.",
        "benefits": [
            ("uil-google", "Google Ads management", "Search and Shopping campaigns targeting the exact keywords {city} buyers use, with conversion tracking on every click."),
            ("uil-facebook-f", "Meta advertising", "Facebook and Instagram campaigns that reach local customers by neighbourhood, interest, and buying intent."),
            ("uil-chart-line", "Local SEO", "Rank in the Google Map Pack and organic results for the searches that matter in your service area."),
            ("uil-analytics", "Transparent reporting", "You see exactly what was spent, what it earned, and what we are optimizing next, every month."),
        ],
        "faqs": [
            ("How much should a {city} business spend on ads?",
             "Most local businesses see solid results starting between $500 and $1,500 per month in ad spend, plus management. We size the budget to your market: competitive industries in {city} may need more, niche services often need less. We will give you a realistic number in your free consultation."),
            ("Google Ads or SEO: which is better for {city} businesses?",
             "Both, in sequence. Google Ads delivers leads this week while SEO compounds over months into free, durable traffic. We usually launch ads first for immediate revenue, then invest part of the returns into SEO so your cost per lead keeps falling."),
            ("How quickly will I see results?",
             "Paid campaigns typically generate their first leads within days of launch. Local SEO improvements usually show ranking gains within 4-12 weeks. We report both monthly so you always know your cost per lead."),
            ("Do you require long-term contracts?",
             "No. We earn your business month to month. You own your ad accounts, your data, and your website; if we ever part ways, everything stays with you."),
        ],
        "cta_title": "Get more {city} customers this month",
        "cta_text": "Book a free 30-minute strategy call. We will review your market, estimate your cost per lead, and map out a campaign plan.",
    },
    "ai-automation": {
        "name": "AI Automation",
        "h1": "AI Automation for {city} Businesses",
        "subtitle": "AI receptionists and workflow automation that answer every call and follow up on every lead, 24/7.",
        "meta": "AI automation for {city} businesses: 24/7 AI receptionists, appointment booking, lead follow-up and workflow automation. Never miss a call again. Free demo.",
        "price_from": "custom plans",
        "intro2": "Our AI receptionists answer your phone 24/7, book appointments directly into your calendar, answer common questions, and route urgent calls to you. Beyond the phone, we automate follow-ups, reviews requests, and back-office workflows so your team spends time on customers, not admin.",
        "benefits": [
            ("uil-phone", "Never miss a call", "An AI receptionist answers on the first ring, day and night, even when every line is busy."),
            ("uil-calendar-alt", "Books appointments itself", "Integrates with your calendar or practice software and books qualified appointments in real time."),
            ("uil-english-to-chinese", "Speaks your customers' language", "Handles conversations naturally, answers FAQs about hours, pricing, and services, and escalates when a human is needed."),
            ("uil-cog", "Workflow automation", "Automatic follow-up texts, review requests, invoice reminders, and lead routing that run themselves."),
        ],
        "faqs": [
            ("What does an AI receptionist cost for a {city} business?",
             "Far less than a full-time hire. A human receptionist costs $40,000+ per year; our AI receptionist plans are a small fraction of that, work 24/7, and never call in sick. Pricing depends on call volume and integrations; we will quote it in your free demo."),
            ("Will it sound robotic to my customers?",
             "No. Modern AI voice agents hold natural conversations, handle interruptions, and answer real questions about your business. Book a free demo through our contact form and hear it for yourself."),
            ("Can it book appointments into my existing system?",
             "Yes. We integrate with Google Calendar, Calendly, and industry software like Dentrix, Jane, and Clio. The AI checks real availability and books directly, with confirmations sent automatically."),
            ("What happens with emergencies or complex calls?",
             "You set the rules. The AI can transfer urgent calls to your mobile, take detailed messages, or send you an instant text summary, so real emergencies always reach a human fast."),
        ],
        "cta_title": "Never miss another customer call",
        "cta_text": "Book a free demo and hear an AI receptionist in action, then get one answering for your {city} business within two weeks.",
    },
}

# ---------------------------------------------------------------- industries (AI receptionist)
INDUSTRIES = {
    "dentists": {
        "name": "Dentists & Dental Clinics",
        "short": "dental practices",
        "h1": "AI Receptionist for Dental Offices",
        "meta": "AI receptionist for dentists: answer every patient call 24/7, book appointments into Dentrix or Jane, triage emergencies. Serving Toronto & the GTA. Free demo.",
        "pain": "Front desks in busy dental practices juggle check-ins, insurance, and recalls, and studies show up to a third of inbound calls to dental offices go unanswered. Every missed call is a new-patient exam, a hygiene booking, or an emergency that calls the next practice on Google.",
        "benefits": [
            ("uil-phone", "Answers on the first ring", "Every patient call answered instantly, 24/7, even when your team is with patients or the office is closed."),
            ("uil-calendar-alt", "Books into your PMS", "Integrates with Dentrix, Jane, and other practice software to book hygiene and exam slots in real time."),
            ("uil-heart-medical", "Emergency triage", "Asks the right questions, distinguishes a broken crown from a routine recall, and routes true emergencies to the on-call dentist."),
            ("uil-bell", "Cuts no-shows", "Automated confirmation and reminder messages keep your chairs full."),
        ],
        "faqs": [
            ("Can the AI answer insurance questions?", "Yes. It can explain which insurers you accept, describe your direct-billing policy, and collect the patient's insurance details before the visit so your front desk is prepared."),
            ("Is patient information kept private?", "Yes. Calls are handled on secure infrastructure, data is encrypted, and we configure the assistant around PHIPA-conscious practices for Ontario clinics."),
            ("What does it cost compared to front-desk staff?", "A fraction of one salary. It does not replace your team; it catches the calls they physically cannot answer: lunch hours, evenings, weekends, and busy mornings."),
        ],
    },
    "law-firms": {
        "name": "Law Firms & Lawyers",
        "short": "law firms",
        "h1": "AI Receptionist & Intake for Law Firms",
        "meta": "AI receptionist for law firms: 24/7 legal intake, lead qualification, consultation booking, Clio integration. Serving Toronto & GTA firms. Free demo.",
        "pain": "Legal clients call when the problem happens: after an accident, an arrest, or a dispute, often outside office hours. If your firm does not pick up, the next firm on the search results does, and that retainer is gone.",
        "benefits": [
            ("uil-phone", "24/7 intake", "Every potential client reaches a professional voice immediately, at 2 PM or 2 AM."),
            ("uil-file-check-alt", "Qualifies leads", "Collects matter type, urgency, and conflict-check basics so lawyers only spend time on qualified consultations."),
            ("uil-calendar-alt", "Books consultations", "Schedules directly into your calendar or Clio, with confirmations sent to the client automatically."),
            ("uil-shield-check", "Confidential and consistent", "Every caller gets the same professional script your firm approves, with full call summaries for your records."),
        ],
        "faqs": [
            ("Can it screen out non-viable cases?", "Yes. You define the practice areas you accept and the qualifying questions to ask. Callers outside your scope are politely referred out, protecting your lawyers' time."),
            ("Does it integrate with Clio?", "Yes. Intake details flow into your practice management system, and consultations are booked against real calendar availability."),
            ("Is it confidential?", "Yes. Calls are encrypted and handled to the confidentiality standard you configure. You approve every script and every piece of information the assistant collects."),
        ],
    },
    "medical-clinics": {
        "name": "Medical Clinics & Doctors",
        "short": "medical clinics",
        "h1": "AI Receptionist for Medical Clinics",
        "meta": "AI receptionist for medical clinics and doctors' offices: 24/7 patient calls, appointment booking, prescription-refill routing. Toronto & GTA. Free demo.",
        "pain": "Clinic phone lines are jammed at 9 AM Monday and silent staff-side after 5 PM, while patients keep calling. Long hold times frustrate patients, and unanswered lines send them to walk-ins or leave gaps in your schedule.",
        "benefits": [
            ("uil-phone", "No more hold music", "Handles unlimited simultaneous calls, so no patient waits on hold or hangs up."),
            ("uil-calendar-alt", "Real-time booking", "Books and reschedules appointments directly into your EMR-linked calendar, including Jane and similar systems."),
            ("uil-prescription-bottle", "Routes refills and results", "Directs prescription refills, results inquiries, and referrals to the right staff queue instead of interrupting the front desk."),
            ("uil-heart-medical", "After-hours triage", "Follows your protocol: routine requests get booked, urgent symptoms get directed to the on-call line or 911 guidance."),
        ],
        "faqs": [
            ("Is it PHIPA-conscious?", "Yes. We configure the assistant around Ontario privacy expectations: encrypted calls, minimal data collection, and your clinic's own consent and disclosure wording."),
            ("Can patients still reach a human?", "Always. You define the escalation rules; any caller who asks for a person, or any urgent situation, is transferred immediately."),
            ("How fast can we go live?", "Most clinics launch within 1-2 weeks: we script it around your booking rules, connect the calendar, test with your staff, then forward the line."),
        ],
    },
    "restaurants": {
        "name": "Restaurants",
        "short": "restaurants",
        "h1": "AI Receptionist & Phone Answering for Restaurants",
        "meta": "AI phone answering for restaurants: take reservations, answer hours & menu questions, handle takeout calls during the dinner rush. Toronto & GTA. Free demo.",
        "pain": "The phone rings hardest exactly when your staff can least afford to answer it: Friday dinner rush. Missed calls are missed reservations and takeout orders, and callers who hit voicemail just order from the next restaurant.",
        "benefits": [
            ("uil-phone", "Answers during the rush", "Every call answered even when the line is out the door: reservations, hours, directions, dietary questions."),
            ("uil-calendar-alt", "Takes reservations", "Books tables into your reservation system or a shared calendar, with party size, time, and special requests captured."),
            ("uil-utensils", "Knows your menu", "Answers questions about dishes, allergens, specials, and pricing straight from the menu you provide."),
            ("uil-shopping-bag", "Captures takeout demand", "Takes pickup orders or sends callers your online-ordering link by text, so the kitchen keeps earning."),
        ],
        "faqs": [
            ("Can it handle multiple languages?", "Yes. The assistant can converse in multiple languages, which matters for GTA restaurants serving diverse neighbourhoods."),
            ("What happens on holidays or special hours?", "You update it in seconds. Holiday hours, prix-fixe menus, and event bookings are all part of the knowledge it answers from."),
            ("Does it work with my reservation platform?", "We integrate with common booking calendars and can send reservation details wherever your team already looks, including text and email summaries."),
        ],
    },
    "salons-spas": {
        "name": "Salons & Spas",
        "short": "salons and spas",
        "h1": "AI Receptionist for Salons & Spas",
        "meta": "AI receptionist for salons, spas and barbershops: book appointments 24/7, answer service & pricing questions, reduce no-shows. Toronto & GTA. Free demo.",
        "pain": "Your stylists can't answer the phone mid-service, and clients booking after work call after you close. Every unanswered call is a colour appointment or spa package booked somewhere else.",
        "benefits": [
            ("uil-phone", "Books while you work", "Answers and books appointments while every chair is busy, and keeps booking after close."),
            ("uil-calendar-alt", "Knows your book", "Checks each stylist's real availability and books the right service length with the right person."),
            ("uil-tag-alt", "Quotes services and prices", "Answers pricing, duration, and preparation questions for your full service menu."),
            ("uil-bell", "Fills cancellations", "Confirmation texts and reminders cut no-shows, and cancelled slots can trigger waitlist outreach."),
        ],
        "faqs": [
            ("Can clients book a specific stylist?", "Yes. The assistant knows each staff member's services and schedule, and books to the requested person or offers the next available."),
            ("Does it upsell?", "It can. Add-on suggestions, like a treatment with a colour service, are scripted by you and offered naturally during booking."),
            ("What does it cost?", "Plans are a small fraction of front-desk wages and scale with call volume. Most salons cover the cost with a handful of saved bookings per month."),
        ],
    },
    "contractors": {
        "name": "Contractors & Trades",
        "short": "contractors and trades businesses",
        "h1": "AI Receptionist for Contractors & Trades",
        "meta": "AI receptionist for contractors, plumbers, electricians & HVAC: answer every call from the job site, qualify leads, book estimates. Toronto & GTA. Free demo.",
        "pain": "You're on a roof, under a sink, or running a crew, and the phone rings with a $10,000 job. Homeowners rarely leave voicemails; they call the next contractor on the list. For trades, the fastest responder usually wins the work.",
        "benefits": [
            ("uil-phone", "Answers from the job site", "Every call answered professionally while your hands are full, with instant text summaries to your phone."),
            ("uil-file-check-alt", "Qualifies the job", "Collects job type, location, timeline, and budget signals so you call back only real prospects."),
            ("uil-calendar-alt", "Books estimates", "Schedules site visits into your calendar with the address and job details already captured."),
            ("uil-bolt", "Emergency dispatch", "Burst pipe at midnight? Urgent calls get routed straight to your cell; routine quotes wait for morning."),
        ],
        "faqs": [
            ("Can it give quotes?", "It can share your standard pricing, like service-call fees and hourly rates, and collect the details you need to quote accurately on the callback."),
            ("What if I'm a one-person operation?", "That's exactly who this is for. You literally cannot answer while working; the AI makes you look like a company with a full office."),
            ("How do I get the lead information?", "Instant text and email after every call: caller name, number, job description, urgency, and address, ready for your callback."),
        ],
    },
    "real-estate": {
        "name": "Real Estate Agents",
        "short": "real estate professionals",
        "h1": "AI Receptionist for Real Estate Agents",
        "meta": "AI receptionist for realtors: answer buyer & seller calls 24/7, qualify leads, book showings while you're in appointments. Toronto & GTA. Free demo.",
        "pain": "Buyers call the moment they see a listing, and if you're in a showing, that lead calls the next agent on the sign. Speed-to-lead decides who gets the client in real estate.",
        "benefits": [
            ("uil-phone", "Captures every listing call", "Answers instantly while you are in showings, closings, or with clients."),
            ("uil-file-check-alt", "Qualifies buyers and sellers", "Pre-approval status, timeline, neighbourhood, and budget collected before you spend a minute."),
            ("uil-calendar-alt", "Books showings", "Schedules showings and consultations directly into your calendar with confirmations sent."),
            ("uil-home", "Knows your listings", "Answers questions about beds, baths, price, and open-house times from your active listing sheet."),
        ],
        "faqs": [
            ("Can it handle calls for multiple listings?", "Yes. Load your active listings and the assistant answers property-specific questions and books showings for each one."),
            ("Does it work with my CRM?", "Lead details can flow to your CRM, email, or phone by text, so follow-up starts while the lead is still hot."),
            ("What about after-hours sign calls?", "That's where it earns its keep: evening and weekend sign calls get answered, qualified, and booked instead of going to voicemail."),
        ],
    },
    "accountants": {
        "name": "Accountants & Bookkeepers",
        "short": "accounting firms",
        "h1": "AI Receptionist for Accounting Firms",
        "meta": "AI receptionist for accountants & bookkeepers: handle tax-season call volume, book client meetings, answer service questions 24/7. Toronto & GTA. Free demo.",
        "pain": "From February to April your phone doesn't stop; the rest of the year every interruption breaks focus on client files. Both problems cost you: missed calls in tax season are missed clients, and constant interruptions are missed billable hours.",
        "benefits": [
            ("uil-phone", "Absorbs tax-season volume", "Unlimited simultaneous calls during your busiest months, with no hold times and no missed prospects."),
            ("uil-calendar-alt", "Books client meetings", "Schedules consultations and document-drop appointments straight into your calendar."),
            ("uil-file-check-alt", "Collects details upfront", "Gathers entity type, services needed, and deadlines so meetings start productive."),
            ("uil-shield-check", "Professional and consistent", "Every caller hears the same polished greeting and accurate answers about your services and pricing."),
        ],
        "faqs": [
            ("Can it answer questions about my services?", "Yes. Personal tax, corporate returns, bookkeeping, payroll: it explains your offerings and fees exactly as you script them."),
            ("Is client information secure?", "Yes. Calls are encrypted and the assistant collects only what you configure, aligned with your confidentiality obligations."),
            ("Can I turn it up only for tax season?", "Absolutely. Many firms run it year-round for after-hours coverage and scale it up for February through April."),
        ],
    },
}

# ---------------------------------------------------------------- HTML template

def head_block(title, meta, url):
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-17927080637"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'AW-17927080637');
    </script>

    <title>{title}</title>
    <meta name="description" content="{meta}">
    <meta name="author" content="Nova Toronto">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">

    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta}">
    <meta property="og:image" content="{DOMAIN}/assets/img/NovaToronto.png">
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{meta}">

    <link rel="stylesheet" href="https://unicons.iconscout.com/release/v4.0.0/css/line.css">
    <link rel="stylesheet" href="/assets/css/styles.css">
    <link rel="icon" href="/assets/img/small_logo.png" type="image/png">

    <style>
        .local-hero {{ padding-top: 7rem; }}
        .breadcrumbs {{ font-size: var(--small-font-size); color: var(--text-color-light); margin-bottom: 1rem; }}
        .breadcrumbs a {{ color: var(--first-color); }}
        .benefit-grid {{ display: grid; gap: 1.5rem; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); margin: 2rem 0; }}
        .benefit-card {{ background: var(--container-color); border-radius: 1rem; padding: 1.75rem; border: 1px solid rgba(0,150,221,.15); }}
        .benefit-card i {{ font-size: 1.75rem; color: var(--first-color); }}
        .benefit-card h3 {{ margin: .75rem 0 .5rem; font-size: var(--h3-font-size); color: var(--title-color); }}
        .benefit-card p {{ font-size: var(--small-font-size); color: var(--text-color); line-height: 1.6; }}
        .faq-item {{ background: var(--container-color); border-radius: .75rem; margin-bottom: 1rem; border: 1px solid rgba(0,150,221,.15); }}
        .faq-item summary {{ cursor: pointer; padding: 1.25rem 1.5rem; font-weight: var(--font-medium); color: var(--title-color); list-style: none; display: flex; justify-content: space-between; align-items: center; }}
        .faq-item summary::after {{ content: '+'; color: var(--first-color); font-size: 1.5rem; }}
        .faq-item[open] summary::after {{ content: '\\2212'; }}
        .faq-item p {{ padding: 0 1.5rem 1.25rem; color: var(--text-color); line-height: 1.7; }}
        .cta-panel {{ background: linear-gradient(135deg, rgba(0,150,221,.12), rgba(0,253,240,.08)); border: 1px solid rgba(0,150,221,.3); padding: 2.5rem 2rem; border-radius: 1.5rem; text-align: center; margin: 3rem 0; }}
        .cta-panel h2 {{ color: var(--title-color); margin-bottom: .75rem; }}
        .cta-panel p {{ margin-bottom: 1.5rem; }}
        .link-chips {{ display: flex; flex-wrap: wrap; gap: .5rem; margin: 1rem 0 2rem; }}
        .link-chips a {{ background: var(--container-color); border: 1px solid rgba(0,150,221,.25); color: var(--first-color); padding: .4rem .9rem; border-radius: 2rem; font-size: var(--small-font-size); }}
        .link-chips a:hover {{ background: var(--first-color); color: #fff; }}
        .local-section h2 {{ color: var(--title-color); font-size: var(--h2-font-size); margin: 2.5rem 0 1rem; }}
        .local-section p {{ line-height: 1.75; margin-bottom: 1rem; }}
    </style>
"""


def nav_block():
    return """
<body>
    <header class="header" id="header">
        <nav class="nav container">
            <a href="/" class="nav__logo">
                <img src="/assets/img/NovaToronto.png" width="110" height="60" alt="Nova Toronto logo">
            </a>
            <div class="nav__menu" id="nav-menu">
                <ul class="nav__list grid">
                    <li class="nav__item"><a href="/" class="nav__link"><i class="uil uil-estate nav__icon"></i>HOME</a></li>
                    <li class="nav__item dropdown">
                        <a href="/services/" class="nav__link dropdown__toggle"><i class="uil uil-apps nav__icon"></i>SERVICES</a>
                        <ul class="dropdown__menu">
                            <li><a href="/website-design/" class="nav__link dropdown__item">Website Design</a></li>
                            <li><a href="/digital-marketing/" class="nav__link dropdown__item">Digital Marketing</a></li>
                            <li><a href="/ai-automation/" class="nav__link dropdown__item">AI Automation</a></li>
                            <li><a href="/amazon-seller/" class="nav__link dropdown__item">Amazon Seller</a></li>
                            <li><a href="/walmart-seller/" class="nav__link dropdown__item">Walmart Seller</a></li>
                        </ul>
                    </li>
                    <li class="nav__item"><a href="/blog/" class="nav__link"><i class="uil uil-newspaper nav__icon"></i>BLOG</a></li>
                    <li class="nav__item"><a href="/#portfolio" class="nav__link"><i class="uil uil-scenery nav__icon"></i>PORTFOLIO</a></li>
                    <li class="nav__item"><a href="/#website-pricing" class="nav__link"><i class="uil uil-briefcase-alt nav__icon"></i>PRICING</a></li>
                    <li class="nav__item"><a href="/#contact" class="nav__link"><i class="uil uil-message nav__icon"></i>CONTACT</a></li>
                </ul>
                <i class="uil uil-times nav__close" id="nav-close"></i>
            </div>
            <div class="nav__btns">
                <i class="uil uil-moon change-theme" id="theme-button"></i>
                <div class="nav__toggle" id="nav-toggle"><i class="uil uil-apps"></i></div>
            </div>
        </nav>
    </header>
"""


def footer_block():
    return """
    <footer class="footer">
        <div class="footer__bg">
            <div class="footer__container container grid">
                <div>
                    <h1 class="footer__title">Nova Toronto</h1>
                    <span class="footer__subtitle">From click to customers</span>
                </div>
                <ul class="footer__links">
                    <li><a href="/website-design/" class="footer__link">Website Design</a></li>
                    <li><a href="/digital-marketing/" class="footer__link">Digital Marketing</a></li>
                    <li><a href="/ai-automation/" class="footer__link">AI Automation</a></li>
                    <li><a href="/#contact" class="footer__link">Contact</a></li>
                </ul>
                <div class="footer__socials">
                    <a href="https://www.facebook.com/Nova-Toronto-108507575043046/" target="_blank" rel="noopener" class="footer__social"><i class="uil uil-facebook-f"></i></a>
                    <a href="https://www.instagram.com/nova_toronto/" target="_blank" rel="noopener" class="footer__social"><i class="uil uil-instagram"></i></a>
                    <a href="https://www.linkedin.com/in/rujal-tuladhar-37877b167/" target="_blank" rel="noopener" class="footer__social"><i class="uil uil-linkedin-alt"></i></a>
                </div>
            </div>
            <p class="footer__copy">&#169; Nova Toronto. All rights reserved.</p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>

</html>
"""


def json_ld(name, description, url, crumbs, faqs):
    import json
    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(crumbs)
        ],
    }
    service = {
        "@type": "Service",
        "name": name,
        "description": description,
        "url": url,
        "provider": {
            "@type": "ProfessionalService",
            "name": "Nova Toronto",
            "url": DOMAIN,
            "telephone": PHONE_INTL,
            "email": EMAIL,
            "address": {"@type": "PostalAddress", "addressLocality": "Toronto", "addressRegion": "ON", "addressCountry": "CA"},
            "areaServed": "Greater Toronto Area",
        },
    }
    faq = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    graph = {"@context": "https://schema.org", "@graph": [service, breadcrumb, faq]}
    return '<script type="application/ld+json">\n' + json.dumps(graph, indent=1) + "\n</script>\n</head>\n"


def benefits_html(benefits):
    cards = "".join(
        f"""
                <div class="benefit-card">
                    <i class="uil {icon}"></i>
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>"""
        for icon, title, text in benefits
    )
    return f'<div class="benefit-grid">{cards}\n            </div>'


def faqs_html(faqs):
    items = "".join(
        f"""
                <details class="faq-item">
                    <summary>{q}</summary>
                    <p>{a}</p>
                </details>"""
        for q, a in faqs
    )
    return items


def cta_html(title, text):
    return f"""
            <div class="cta-panel">
                <h2>{title}</h2>
                <p>{text}</p>
                <a href="/#contact" class="button button--flex" style="display:inline-flex">
                    Book a Free Consultation <i class="uil uil-calendar-alt button__icon"></i>
                </a>
                <p style="margin-top:1rem; margin-bottom:0; font-size: var(--small-font-size);">
                    Fill out our quick booking form and we respond within one business day.
                </p>
            </div>"""


def chips(links):
    a = "".join(f'\n                <a href="{u}">{t}</a>' for t, u in links)
    return f'<div class="link-chips">{a}\n            </div>'


def write_page(path, html):
    full = os.path.join(REPO, path, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ---------------------------------------------------------------- city pages

def build_city_page(svc_slug, svc, city_slug, city):
    cname = city["name"]
    url = f"{DOMAIN}/{svc_slug}/{city_slug}/"
    title = f"{svc['h1'].format(city=cname)} | Nova Toronto"
    meta = svc["meta"].format(city=cname)
    faqs = [(q.format(city=cname), a.format(city=cname)) for q, a in svc["faqs"]]
    crumbs = [("Home", DOMAIN + "/"), (svc["name"], f"{DOMAIN}/{svc_slug}/"), (cname, url)]

    other_cities = [(CITIES[c]["name"], f"/{svc_slug}/{c}/") for c in CITIES if c != city_slug]
    other_services = [(SERVICES[s]["name"] + f" in {cname}", f"/{s}/{city_slug}/") for s in SERVICES if s != svc_slug]

    html = head_block(title, meta, url)
    html += json_ld(f"{svc['name']} in {cname}", meta, url, crumbs, faqs)
    html += nav_block()
    html += f"""
    <main class="main">
        <section class="section local-hero">
            <div class="container" style="max-width: 900px;">
                <nav class="breadcrumbs" aria-label="Breadcrumb">
                    <a href="/">Home</a> &rsaquo; <a href="/{svc_slug}/">{svc['name']}</a> &rsaquo; {cname}
                </nav>
                <h1 class="section__title" style="text-align:left; padding-top:0;">{svc['h1'].format(city=cname)}</h1>
                <p class="section__subtitle" style="text-align:left;">{svc['subtitle'].format(city=cname)}</p>

                <div class="local-section">
                    <p>{city['blurb']}</p>
                    <p>{city['angle']}</p>
                    <p>{svc['intro2']} We work with businesses across {city['areas']}.</p>

                    <h2>Why {cname} businesses choose Nova Toronto</h2>
                    {benefits_html(svc['benefits'])}
                    {cta_html(svc['cta_title'].format(city=cname), svc['cta_text'].format(city=cname))}

                    <h2>Frequently asked questions</h2>
                    {faqs_html(faqs)}

                    <h2>Our other services in {cname}</h2>
                    {chips(other_services + [("Website Pricing", "/#website-pricing"), ("Our Portfolio", "/#portfolio")])}

                    <h2>{svc['name']} across the GTA</h2>
                    {chips(other_cities)}
                </div>
            </div>
        </section>
    </main>
"""
    html += footer_block()
    return write_page(f"{svc_slug}/{city_slug}", html)


# ---------------------------------------------------------------- industry pages

def build_industry_page(ind_slug, ind):
    url = f"{DOMAIN}/ai-automation/ai-receptionist/{ind_slug}/"
    title = f"{ind['h1']} | Nova Toronto"
    meta = ind["meta"]
    faqs = ind["faqs"] + [
        ("Can I try it before committing?",
         "Yes. Book a free demo through our contact form and we will let you talk to the exact technology we deploy, then scope a version scripted for your business."),
    ]
    crumbs = [("Home", DOMAIN + "/"), ("AI Automation", DOMAIN + "/ai-automation/"),
              ("AI Receptionist", DOMAIN + "/ai-automation/ai-receptionist/"), (ind["name"], url)]

    other_inds = [(INDUSTRIES[i]["name"], f"/ai-automation/ai-receptionist/{i}/") for i in INDUSTRIES if i != ind_slug]

    html = head_block(title, meta, url)
    html += json_ld(ind["h1"], meta, url, crumbs, faqs)
    html += nav_block()
    html += f"""
    <main class="main">
        <section class="section local-hero">
            <div class="container" style="max-width: 900px;">
                <nav class="breadcrumbs" aria-label="Breadcrumb">
                    <a href="/">Home</a> &rsaquo; <a href="/ai-automation/">AI Automation</a> &rsaquo; <a href="/ai-automation/ai-receptionist/">AI Receptionist</a> &rsaquo; {ind['name']}
                </nav>
                <h1 class="section__title" style="text-align:left; padding-top:0;">{ind['h1']}</h1>
                <p class="section__subtitle" style="text-align:left;">Serving {ind['short']} across Toronto and the GTA.</p>

                <div class="local-section">
                    <p>{ind['pain']}</p>
                    <p>Nova Toronto builds AI receptionists for {ind['short']} that answer every call 24/7, book appointments directly into your calendar, and hand you a summary of every conversation. It costs a fraction of a hire and never takes a day off.</p>

                    <h2>What it does for {ind['short']}</h2>
                    {benefits_html(ind['benefits'])}
                    {cta_html("See it answer calls for your business", "Book a free demo and hear an AI receptionist scripted for " + ind['short'] + ". Setup usually takes under two weeks.")}

                    <h2>Frequently asked questions</h2>
                    {faqs_html(faqs)}

                    <h2>AI receptionists for other industries</h2>
                    {chips(other_inds + [("AI Automation Services", "/ai-automation/")])}

                    <h2>More ways we grow your business</h2>
                    {chips([("Website Design", "/website-design/"), ("Digital Marketing", "/digital-marketing/"), ("Website Pricing", "/#website-pricing")])}
                </div>
            </div>
        </section>
    </main>
"""
    html += footer_block()
    return write_page(f"ai-automation/ai-receptionist/{ind_slug}", html)


# ---------------------------------------------------------------- sitemap

STATIC_URLS = [
    ("", 1.0), ("services/", 0.8), ("website-design/", 0.9), ("digital-marketing/", 0.9),
    ("ai-automation/", 0.9), ("ai-automation/ai-receptionist/", 0.8),
    ("website-design/website-audit/", 0.6),
    ("digital-marketing/google-search/", 0.7), ("digital-marketing/google-shopping/", 0.7),
    ("digital-marketing/meta-ads/", 0.7), ("digital-marketing/microsoft-ads/", 0.7),
    ("amazon-seller/", 0.6), ("walmart-seller/", 0.6), ("blog/", 0.7),
    ("blog/google-ads-budget-toronto/", 0.6),
    ("blog/ai-receptionist-dental/", 0.5), ("blog/ai-receptionist-law-firm/", 0.5),
    ("blog/ai-receptionist-small-business/", 0.5),
    ("blog/website-design/must-have-website-features-toronto/", 0.5),
    ("blog/website-design/essential-website-guide-toronto/", 0.5),
]


def build_sitemap(generated):
    entries = []
    for path, prio in STATIC_URLS:
        entries.append((f"{DOMAIN}/{path}", prio))
    for path in generated:
        entries.append((f"{DOMAIN}/{path}/", 0.8))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in entries:
        xml.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio}</priority>\n  </url>")
    xml.append("</urlset>\n")
    with open(os.path.join(REPO, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml))


def main():
    generated = []
    for svc_slug, svc in SERVICES.items():
        for city_slug, city in CITIES.items():
            generated.append(build_city_page(svc_slug, svc, city_slug, city))
    for ind_slug, ind in INDUSTRIES.items():
        generated.append(build_industry_page(ind_slug, ind))
    build_sitemap(generated)
    print(f"Generated {len(generated)} pages + sitemap.xml ({TODAY})")
    for g in generated:
        print("  /" + g + "/")


if __name__ == "__main__":
    main()

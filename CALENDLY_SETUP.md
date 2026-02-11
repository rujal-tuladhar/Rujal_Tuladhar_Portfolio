# Calendly Setup Guide - Google Calendar Integration

This is the **BEST** solution for your requirements because:
✅ Syncs with Google Calendar in real-time
✅ Shows only YOUR available slots (7-10am, 8-11pm EST)
✅ Automatically blocks booked times
✅ Creates calendar events automatically
✅ Sends confirmation emails
✅ Works perfectly on GitHub Pages
✅ **100% FREE** for basic use

---

## Step 1: Create Calendly Account (2 minutes)

1. Go to **https://calendly.com/signup**
2. Sign up with your email: **novatoronto.ca@gmail.com**
3. Choose the **FREE** plan (perfect for your needs)

## Step 2: Connect Google Calendar (1 minute)

1. In Calendly dashboard, go to **"Calendar Connection"**
2. Click **"Connect Calendar"**
3. Choose **Google Calendar**
4. Sign in with **novatoronto.ca@gmail.com**
5. Allow Calendly to access your calendar

**This enables:**
- Calendly checks your Google Calendar for conflicts
- Automatically blocks times when you're busy
- Creates events in your Google Calendar when someone books

## Step 3: Set Your Availability (2 minutes)

1. Go to **"Availability"** in Calendly
2. Click **"Set your weekly hours"**
3. Configure your schedule:

**Monday - Sunday:**
- **Morning:** 7:00 AM - 10:00 AM EST
- **Evening:** 8:00 PM - 11:00 PM EST

4. Set timezone to **Eastern Time (US & Canada)**
5. Click **Save**

## Step 4: Create Event Type (2 minutes)

1. Go to **"Event Types"**
2. Click **"+ New Event Type"**
3. Choose **"One-on-One"**
4. Configure:
   - **Event name:** "Traffic Consultation"
   - **Duration:** 30 minutes
   - **Location:** Phone call or Zoom (your choice)
   - **Description:** "Free 30-minute consultation to discuss strategies for increasing your website traffic and growing your business online."

5. Click **Save & Close**

## Step 5: Get Your Calendly Link (30 seconds)

1. Click on your event type
2. Copy your Calendly link (looks like: `https://calendly.com/yourname/30min`)
3. This is your scheduling link!

## Step 6: Update Your Website (1 minute)

Open `index.html` and find this line (around line 1120):

```html
data-url="https://calendly.com/YOUR_CALENDLY_USERNAME/30min?hide_gdpr_banner=1&primary_color=6e57e0"
```

Replace `YOUR_CALENDLY_USERNAME/30min` with your actual Calendly link:

```html
data-url="https://calendly.com/novatoronto/traffic-consultation?hide_gdpr_banner=1&primary_color=6e57e0"
```

**Save the file and you're done!** 🎉

---

## How It Works

1. **Customer visits your website** → Sees available time slots
2. **Customer selects time** → Only sees 7-10am or 8-11pm EST slots
3. **Customer books** → Enters name, email, phone
4. **Calendly creates event** → Automatically added to YOUR Google Calendar
5. **Both get emails** → Confirmation with calendar invite
6. **Conversion tracked** → Calendly can redirect to your thank-you.html page

---

## Advanced: Redirect to Thank You Page

1. In Calendly, go to your event type settings
2. Scroll to **"Confirmation Page"**
3. Choose **"Redirect to an external site"**
4. Enter: `https://novatoronto.com/thank-you.html`

Now after booking, customers will be redirected to your thank you page with Google Tag Manager tracking!

---

## What You Get (FREE Plan)

✅ **Unlimited** bookings
✅ **1 event type** (perfect for your consultation)
✅ **Google Calendar sync** (2-way sync)
✅ **Email notifications** to you and customer
✅ **Automated reminders** to reduce no-shows
✅ **Mobile responsive** booking page
✅ **Custom branding** (your colors)
✅ **Buffer time** between meetings (optional)
✅ **Timezone detection** (shows customer's local time)

---

## Why Calendly is Better Than Custom Forms

| Feature | Custom Form | Calendly |
|---------|-------------|----------|
| Shows real availability | ❌ No | ✅ Yes |
| Blocks booked times | ❌ No | ✅ Yes |
| Google Calendar sync | ❌ No | ✅ Yes |
| Auto calendar events | ❌ No | ✅ Yes |
| Handles timezones | ❌ No | ✅ Yes |
| Sends reminders | ❌ No | ✅ Yes |
| Setup time | 2 hours | 10 minutes |
| Maintenance | High | Zero |

---

## Customization Options

**Change colors** to match your brand:
- In Calendly settings → **Branding**
- Set primary color to: `#6e57e0` (your purple)

**Add custom questions:**
- In event type → **Invitee Questions**
- Add: "What's your current monthly website traffic?"
- Add: "What's your main goal for this consultation?"

**Set buffer time:**
- In event type → **Scheduling Conditions**
- Add 15-minute buffer between meetings if needed

---

## Testing

1. Save your changes
2. Open your website
3. Scroll to the booking section
4. You should see the Calendly widget embedded
5. Try booking a test appointment
6. Check your Google Calendar - it should appear!

---

## Support

- Calendly has excellent documentation: https://help.calendly.com
- Free plan includes email support
- Video tutorials available

---

## Alternative: Keep Custom Form with Web3Forms

If you absolutely want a custom form instead of Calendly, I can keep the Web3Forms implementation, but you'll need to:
- Manually add bookings to Google Calendar
- Manually track which slots are booked
- No automatic conflict detection

**My recommendation: Use Calendly** - it solves all your requirements perfectly and is actually easier than the custom form!

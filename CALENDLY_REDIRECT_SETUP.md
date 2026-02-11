# Calendly Redirect Setup - Thank You Page

## Quick Setup (2 minutes)

After a customer books an appointment through Calendly, you can automatically redirect them to your thank you page where Google Tag Manager will track the conversion.

---

## Step-by-Step Instructions

### 1. Log into Calendly
Go to https://calendly.com and sign in with your account (novatoronto.ca@gmail.com)

### 2. Navigate to Your Event Type
- Click on **"Event Types"** in the left sidebar
- Find your **"30 Minute Meeting"** event
- Click on the event name or the gear icon to edit it

### 3. Configure Confirmation Page
- Scroll down to the **"Confirmation Page"** section
- You'll see two options:
  - ⭕ Display confirmation page on Calendly
  - ⭕ **Redirect to an external site** ← **Select this one**

### 4. Enter Your Thank You Page URL
In the URL field, enter:
```
https://novatoronto.com/thank-you.html
```

Or if you're testing locally first:
```
https://yourdomain.com/thank-you.html
```

### 5. Save Changes
- Click **"Save & Close"** at the top right
- Your redirect is now active! 🎉

---

## What Happens Now

1. **Customer visits your website** → Clicks "Schedule Now"
2. **Scrolls to booking section** → Sees Calendly widget
3. **Selects date & time** → Fills out name, email, phone
4. **Clicks "Schedule Event"** → Booking confirmed
5. **Automatically redirected** → To your thank you page
6. **Google Tag Manager fires** → Conversion event tracked
7. **Customer sees** → Confirmation message and next steps

---

## Testing the Flow

1. Go to your website: https://novatoronto.com
2. Click "Schedule Now" button
3. Book a test appointment (use your own email)
4. After clicking "Schedule Event", you should be redirected to `/thank-you.html`
5. Check your browser console (F12) to verify GTM event fired
6. Check your Google Calendar - the appointment should appear

---

## Google Tag Manager Conversion Tracking

Your thank you page already has:

✅ **GTM Container**: GTM-MNFPW6W7
✅ **Conversion Event**: `consultation_booked`
✅ **Event Type**: `form_submission`

The conversion event fires automatically when the thank you page loads.

---

## Alternative: Custom Redirect with Parameters

If you want to pass booking details to the thank you page, Calendly supports URL parameters:

```
https://novatoronto.com/thank-you.html?event={event_type_name}&name={invitee_name}&email={invitee_email}
```

This allows you to personalize the thank you page with the customer's name.

---

## Troubleshooting

**Redirect not working?**
- Make sure you saved the event type settings
- Clear your browser cache
- Try in incognito mode

**Thank you page not loading?**
- Verify the URL is correct
- Make sure `thank-you.html` is in your root directory
- Check that the file is deployed to your live site

**GTM not firing?**
- Open browser console (F12)
- Look for GTM debug messages
- Verify GTM container ID is correct

---

## Optional: Customize Confirmation Email

While you're in Calendly settings, you can also customize the confirmation email:

1. Go to **"Notifications & Workflows"**
2. Click **"Email Confirmations"**
3. Customize the message your customers receive
4. Add your branding and additional information

---

## Summary

✅ Calendly handles the booking
✅ Customer gets redirected to your thank you page
✅ Google Tag Manager tracks the conversion
✅ You get the booking in your Google Calendar
✅ Customer gets confirmation email

**Everything is automated!** No manual work needed.

# EmailJS Setup Guide

## Overview
EmailJS allows you to send emails directly from your website without a backend server. Follow these steps to complete the booking system setup.

## Step 1: Create EmailJS Account
1. Go to [https://www.emailjs.com/](https://www.emailjs.com/)
2. Click "Sign Up" and create a free account
3. Verify your email address

## Step 2: Add Email Service
1. In your EmailJS dashboard, go to "Email Services"
2. Click "Add New Service"
3. Choose "Gmail" (since you're using novatoronto.ca@gmail.com)
4. Click "Connect Account" and sign in with novatoronto.ca@gmail.com
5. Give it a Service ID (e.g., "service_nova_toronto")
6. Click "Create Service"

## Step 3: Create Email Template
1. Go to "Email Templates" in the dashboard
2. Click "Create New Template"
3. Give it a Template ID (e.g., "template_booking")
4. Set up the template with these variables:

**Subject Line:**
```
New Consultation Booking from {{name}}
```

**Email Body:**
```
You have a new consultation booking!

Client Details:
- Name: {{name}}
- Email: {{email}}
- Phone: {{phone}}

Appointment Details:
- Date: {{date}}
- Time: {{time}}

Message from client:
{{message}}

---
This booking was submitted through the Nova Toronto website.
```

5. Set "To Email" to: novatoronto.ca@gmail.com
6. Click "Save"

## Step 4: Get Your Public Key
1. Go to "Account" → "General"
2. Copy your "Public Key" (it looks like: `xYz123AbC456`)

## Step 5: Update Your Website Code
Open `/Users/loversboy/Desktop/Github/Rujal_Tuladhar_Portfolio/index.html` and find this line (around line 1545):

```javascript
// emailjs.init('YOUR_PUBLIC_KEY');
```

Replace it with:
```javascript
emailjs.init('YOUR_ACTUAL_PUBLIC_KEY_HERE');
```

Then find this commented section (around line 1655):

```javascript
/* 
// UNCOMMENT THIS WHEN YOU SET UP EMAILJS:
await emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', formData);
showStatus('success', 'Booking submitted successfully! Redirecting...');
setTimeout(() => {
    window.location.href = '/thank-you.html';
}, 1500);
*/
```

**Uncomment it and update** with your actual IDs:
```javascript
await emailjs.send('service_nova_toronto', 'template_booking', formData);
showStatus('success', 'Booking submitted successfully! Redirecting...');
setTimeout(() => {
    window.location.href = '/thank-you.html';
}, 1500);
```

**Then comment out or remove** the mailto fallback code (lines 1620-1640).

## Step 6: Test the Form
1. Save your changes
2. Open your website
3. Fill out the booking form with test data
4. Submit and check if:
   - You receive an email at novatoronto.ca@gmail.com
   - You're redirected to the thank you page
   - Google Tag Manager fires the conversion event

## Free Tier Limits
- 200 emails per month
- If you need more, upgrade to a paid plan ($15/month for 1,000 emails)

## Troubleshooting
- **No email received?** Check your EmailJS dashboard logs
- **Error on submit?** Open browser console (F12) to see error details
- **Gmail blocking?** Make sure you've connected the correct Gmail account in EmailJS

## Alternative: Keep Mailto Fallback
If you prefer to keep it simple for now, the current mailto implementation will work. It opens the user's email client with pre-filled information. However, EmailJS provides a better user experience as it sends emails automatically without requiring the user to have an email client configured.

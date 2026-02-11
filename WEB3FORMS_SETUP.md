# Web3Forms Setup Guide - Quick & Easy!

Web3Forms is **FREE**, works perfectly with GitHub Pages, and takes only 2 minutes to set up.

## Step 1: Get Your Access Key (1 minute)

1. Go to **https://web3forms.com**
2. Enter your email: **novatoronto.ca@gmail.com**
3. Click "Create Access Key"
4. Check your email and copy the access key (looks like: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

## Step 2: Update Your Website (30 seconds)

Open `index.html` and find this line (around line 1600):

```javascript
formData.append("access_key", "YOUR_WEB3FORMS_ACCESS_KEY_HERE");
```

Replace `YOUR_WEB3FORMS_ACCESS_KEY_HERE` with your actual access key:

```javascript
formData.append("access_key", "a1b2c3d4-e5f6-7890-abcd-ef1234567890");
```

## Step 3: Test It! (30 seconds)

1. Save the file
2. Open your website
3. Fill out the booking form
4. Click "Book Consultation"
5. Check your email at novatoronto.ca@gmail.com

**That's it!** 🎉

## What You Get (FREE Forever)

✅ **250 submissions per month** (free tier)
✅ **Direct email delivery** to novatoronto.ca@gmail.com
✅ **No user interference** - emails send automatically
✅ **Works on GitHub Pages** - no backend needed
✅ **Spam protection** included
✅ **Automatic redirect** to thank-you.html
✅ **Google Tag Manager** conversion tracking

## The Thank You Page

The thank you page is already created at:
📄 `/thank-you.html`

It includes:
- Success confirmation message
- Google Tag Manager tracking (GTM-MNFPW6W7)
- Conversion event: `consultation_booked`
- Next steps for the customer
- Links back to your site

## How It Works

1. User fills out form → 2. Clicks "Book Consultation" → 3. Web3Forms sends email to you → 4. User sees success message → 5. Redirects to thank-you.html → 6. Google Tag Manager fires conversion

## Need More Submissions?

- **Free:** 250/month
- **Pro:** $4.99/month for 1,000 submissions
- **Business:** $9.99/month for 5,000 submissions

For your traffic consultation business, the free tier should be more than enough!

## Troubleshooting

**No email received?**
- Check spam folder
- Verify access key is correct
- Check Web3Forms dashboard for submission logs

**Form not submitting?**
- Open browser console (F12) to see errors
- Make sure you replaced the access key
- Check internet connection

## Why Web3Forms?

✅ Simpler than EmailJS (no templates needed)
✅ More reliable than mailto (actually sends emails)
✅ Works with static hosting (GitHub Pages, Netlify, etc.)
✅ No backend server required
✅ Professional and trusted by thousands

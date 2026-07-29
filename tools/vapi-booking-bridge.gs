/*
 * DEPLOYMENT STATUS (2026-07-29) - NOVATORONTO ACCOUNT
 * -----------------------------------------------------------------
 * LIVE PROJECT (code written + SAVED + verified after reload):
 *   Account : novatoronto.ca@gmail.com  (Chrome account index /u/2/)
 *   Project : https://script.google.com/u/2/home/projects/1twHXBVdrtdgWdZeO-J6e7zNojvRYpChYPHjyF66Y3nIdaJjRLpbZRtTk/edit
 *   Emails go to novatoronto.ca@gmail.com; Calendar events land on
 *   novatoronto.ca@gmail.com's default calendar.
 *
 * REMAINING (user must click - OAuth popup opens as a separate browser
 * WINDOW, outside automation reach):
 *   Deploy > New deployment > gear "Select type" > Web app
 *     Execute as   : Me (novatoronto.ca@gmail.com)
 *     Who has access: Anyone            <-- REQUIRED so Vapi can POST
 *   Deploy > Authorize access > choose novatoronto.ca@gmail.com >
 *   Advanced > "Go to Untitled project (unsafe)" > Allow
 *   Then copy the /exec URL and hand it to Claude.
 *
 * Claude then runs (API key already stored in .vapi-key):
 *   PATCH assistant  server = { url: "<EXEC_URL>?token=<SHARED_TOKEN>" }
 *                    serverMessages = ["end-of-call-report"]
 *
 * An earlier abandoned copy exists under rujal.tuladhar@gmail.com
 * (never authorized, harmless - delete it if you like).
 *
 * EDITOR AUTOMATION NOTE: monaco setValue() does NOT persist in Apps
 * Script; use editor.executeEdits(...) (fires a genuine edit) then click
 * "Save project to Drive".
 * -----------------------------------------------------------------
 */

/**
 * Nova Toronto — Vapi → Gmail + Google Calendar bridge
 * =====================================================
 * Receives Vapi's end-of-call report and:
 *   1. Emails every call summary + booking details to novatoronto.ca@gmail.com
 *   2. Creates a 30-min Google Calendar event when an appointment was booked
 *
 * DEPLOY (one time, ~5 minutes, do this logged in as novatoronto.ca@gmail.com):
 *   1. Go to script.google.com  →  New project
 *   2. Delete the starter code, paste THIS ENTIRE FILE, name it "Vapi Bridge"
 *   3. Click Deploy → New deployment → gear icon → Web app
 *        - Execute as:  Me
 *        - Who has access:  Anyone
 *      → Deploy. Authorize when Google asks (it will warn "unverified" —
 *        Advanced → Go to Vapi Bridge — this is YOUR script in YOUR account).
 *   4. Copy the Web app URL (ends in /exec) and give it to Claude —
 *      it gets wired into the Vapi assistant as the server URL, and from
 *      then on every call lands in your inbox automatically.
 */

var NOTIFY_EMAIL = 'novatoronto.ca@gmail.com';

function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var msg = payload.message || {};
    if (msg.type !== 'end-of-call-report') {
      return ContentService.createTextOutput('ignored');
    }

    var analysis = msg.analysis || {};
    var data = analysis.structuredData || {};
    var summary = analysis.summary || '(no summary)';
    var call = msg.call || {};
    var booked = data.appointmentBooked === true;

    // ---- 1. Email the call report ----
    var subject = (booked ? 'BOOKED: ' : 'Call: ') +
      (data.callerName || 'Unknown caller') +
      (data.serviceInterested ? ' - ' + data.serviceInterested : '');

    var lines = [
      'New call handled by Nova (AI receptionist)',
      '',
      'Name:      ' + (data.callerName || '-'),
      'Phone:     ' + (data.phoneNumber || '-'),
      'Email:     ' + (data.email || '-'),
      'Business:  ' + (data.businessType || '-'),
      'Service:   ' + (data.serviceInterested || '-'),
      'Booked:    ' + (booked ? 'YES' : 'no'),
      'When:      ' + (data.preferredDateTime || '-'),
      'Notes:     ' + (data.notes || '-'),
      '',
      '--- Call summary ---',
      summary,
      '',
      'Transcript & recording: https://dashboard.vapi.ai/calls/' + (call.id || '')
    ];
    MailApp.sendEmail(NOTIFY_EMAIL, subject, lines.join('\n'));

    // ---- 2. Calendar event when a time was agreed ----
    if (booked && data.preferredDateTime) {
      var start = new Date(data.preferredDateTime);
      if (!isNaN(start.getTime())) {
        var end = new Date(start.getTime() + 30 * 60 * 1000);
        CalendarApp.getDefaultCalendar().createEvent(
          'Consultation: ' + (data.callerName || 'caller') +
            (data.phoneNumber ? ' (' + data.phoneNumber + ')' : ''),
          start, end,
          { description: summary + '\n\nService: ' + (data.serviceInterested || '-') +
                         '\nPhone: ' + (data.phoneNumber || '-') }
        );
      }
      // If the date didn't parse, the email above still has the caller's words.
    }

    return ContentService.createTextOutput('ok');
  } catch (err) {
    // Fail-safe: still email the raw payload so nothing is ever lost
    try {
      MailApp.sendEmail(NOTIFY_EMAIL, 'Vapi bridge error',
        String(err) + '\n\n' + (e && e.postData ? e.postData.contents : 'no payload'));
    } catch (ignored) {}
    return ContentService.createTextOutput('error');
  }
}

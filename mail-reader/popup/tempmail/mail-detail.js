        // Parse query parameters from URL
        const params = new URLSearchParams(window.location.search);
        const subject = params.get('subject');
        const sender = params.get('sender');
        const message = params.get('message');

        // Populate HTML elements with email details
        document.getElementById('subject').textContent = subject;
        document.getElementById('sender').textContent = `From: ${sender}`;
        document.getElementById('message').textContent = message;
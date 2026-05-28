def render_dashboard(statuses: dict) -> str:
    cards = []

    for name, status in statuses.items():
        badge = "UP" if status.is_up else "DOWN"
        badge_class = "up" if status.is_up else "down"
        status_code = status.status_code if status.status_code is not None else "N/A"
        response_time = (
            f"{status.response_time_ms} ms"
            if status.response_time_ms is not None
            else "N/A"
        )
        error_html = f"<p class='error'>{status.error}</p>" if status.error else ""

        cards.append(
            f"""
            <article class="card">
                <div class="card-header">
                    <h2>{name}</h2>
                    <span class="badge {badge_class}">{badge}</span>
                </div>
                <p><strong>URL:</strong> <a href="{status.url}" target="_blank">{status.url}</a></p>
                <p><strong>Status code:</strong> {status_code}</p>
                <p><strong>Response time:</strong> {response_time}</p>
                <p><strong>Checked at:</strong> {status.checked_at}</p>
                {error_html}
            </article>
            """
        )

    body = "\n".join(cards) or "<p>No endpoints configured.</p>"

    return f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>API Status Monitor</title>
        <style>
            body {{
                margin: 0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: #f5f7fb;
                color: #18212f;
            }}
            header {{
                padding: 32px 24px;
                background: #111827;
                color: white;
            }}
            main {{
                max-width: 960px;
                margin: 24px auto;
                padding: 0 16px;
                display: grid;
                gap: 16px;
            }}
            .card {{
                background: white;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
            }}
            .card-header {{
                display: flex;
                justify-content: space-between;
                gap: 16px;
                align-items: center;
            }}
            h1, h2 {{ margin: 0; }}
            a {{ color: #2563eb; }}
            .badge {{
                border-radius: 999px;
                padding: 6px 12px;
                font-weight: 700;
                font-size: 12px;
            }}
            .up {{ background: #dcfce7; color: #166534; }}
            .down {{ background: #fee2e2; color: #991b1b; }}
            .error {{ color: #991b1b; }}
            .actions {{ margin-top: 12px; }}
            button {{
                border: 0;
                border-radius: 10px;
                padding: 10px 14px;
                background: #2563eb;
                color: white;
                cursor: pointer;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>API Status Monitor</h1>
            <p>Simple uptime monitoring for your APIs and websites.</p>
            <div class="actions">
                <button onclick="fetch('/api/check-now', {{ method: 'POST' }}).then(() => location.reload())">
                    Check now
                </button>
            </div>
        </header>
        <main>{body}</main>
    </body>
    </html>
    """

#!/usr/bin/env python3
"""
LinkedIn Auto-Poster for RemoteProduktif
Posts teaser content to LinkedIn feed + adds article link as first comment.

Usage:
    python3 linkedin-auto-post.py <slug>
    python3 linkedin-auto-post.py --latest   # Post latest article
    python3 linkedin-auto-post.py --all-pending  # Post all that haven't been posted yet

Credentials: fmindrayana@gmail.com / indrayana21
"""

import json, os, re, sys, time
from datetime import datetime, date

REPO = '/tmp/remote-produktif'
POSTS_DIR = os.path.join(REPO, 'linkedin-posts')
LOG_FILE = os.path.join(POSTS_DIR, '_posted.json')

LINKEDIN_USER = "fmindrayana@gmail.com"
LINKEDIN_PASS = "indrayana21"

from playwright.sync_api import sync_playwright

def load_posted_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            return json.load(f)
    return {"posted": []}

def save_posted_log(slug):
    log = load_posted_log()
    if slug not in log["posted"]:
        log["posted"].append(slug)
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def get_article_url(slug):
    return f"https://remoteproduktif.online/{slug}"

def read_post_text(slug):
    fpath = os.path.join(POSTS_DIR, f'{slug}-linkedin.txt')
    if not os.path.exists(fpath):
        return None
    with open(fpath) as f:
        return f.read().strip()

def get_latest_article():
    with open(os.path.join(REPO, 'artikel.json')) as f:
        data = json.load(f)
    return data[0]

def get_linkedin_post_text(slug):
    """Try to read existing post file, otherwise generate one."""
    text = read_post_text(slug)
    if text:
        return text
    
    # Generate on the fly using the script
    script = os.path.join(REPO, 'scripts', 'generate-linkedin-post.py')
    if os.path.exists(script):
        import subprocess
        result = subprocess.run(['python3', script, slug], capture_output=True, text=True, cwd=REPO)
        if result.returncode == 0:
            return read_post_text(slug)
    return None

def post_to_linkedin(post_text, article_url):
    """Login to LinkedIn and create a post with the article link in comments."""
    print("🚀 Opening LinkedIn...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        ctx = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 900}
        )
        page = ctx.new_page()
        
        # === STEP 1: Login ===
        print("🔑 Logging in...")
        page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded', timeout=30000)
        page.wait_for_timeout(3000)
        
        # LinkedIn uses dynamic IDs - there are 2 sets of fields (one hidden, one visible)
        # Find the VISIBLE email and password fields
        all_emails = page.query_selector_all('input[type="email"]')
        all_pwds = page.query_selector_all('input[type="password"]')
        
        email_input = None
        for el in all_emails:
            if el.is_visible():
                email_input = el
                break
        
        password_input = None
        for el in all_pwds:
            if el.is_visible():
                password_input = el
                break
        
        if not email_input or not password_input:
            print("❌ Could not find login form fields")
            page.screenshot(path='/tmp/linkedin-error.png')
            browser.close()
            return False
        
        email_input.fill(LINKEDIN_USER)
        password_input.fill(LINKEDIN_PASS)
        page.wait_for_timeout(500)
        
        # Find submit button - visible button with text "Sign in"
        submit_btn = None
        for btn in page.query_selector_all('button'):
            text = (btn.inner_text() or '').strip()
            if text == "Sign in" and btn.is_visible():
                submit_btn = btn
                break
        
        if submit_btn:
            submit_btn.click()
        else:
            # Press Enter instead
            page.keyboard.press('Enter')
        
        # Wait for login to complete
        page.wait_for_timeout(8000)
        print(f"📌 URL after login: {page.url}")
        
        if 'checkpoint' in page.url:
            print("⚠️ LinkedIn checkpoint/verification required!")
            page.screenshot(path='/tmp/linkedin-checkpoint.png')
            browser.close()
            return False
        
        if 'feed' not in page.url and '/in/' not in page.url:
            print(f"⚠️ Unexpected URL after login: {page.url}")
            page.screenshot(path='/tmp/linkedin-unexpected.png')
            # Try to continue anyway
        
        # === STEP 2: Click "Start a post" ===
        print("✍️ Clicking 'Start a post'...")
        page.wait_for_timeout(2000)
        
        # Try various selectors for the post button
        post_button = page.query_selector('button:has-text("Start a post")')
        if not post_button:
            post_button = page.query_selector('[aria-label*="Start a post"]')
        if not post_button:
            post_button = page.query_selector('[data-control-name="create_post"]')
        if not post_button:
            post_button = page.query_selector('button:has-text("Post")')
        if not post_button:
            # Try the share box area
            post_button = page.query_selector('.share-box-feed-entry__trigger')
        if not post_button:
            post_button = page.query_selector('.share-creation-state')
        
        if post_button:
            post_button.click()
            print("✅ Clicked post button")
        else:
            print("⚠️ Could not find 'Start a post' button, trying URL approach")
            # Try navigating directly to the post creation page
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(3000)
        
        page.wait_for_timeout(2000)
        
        # === STEP 3: Type the post content ===
        print("📝 Typing post content...")
        
        # Wait for the editor to appear
        editor = None
        for selector in [
            '[role="textbox"]',
            '.ql-editor',
            '[contenteditable="true"]',
            'div[data-placeholder*="What do you want"]',
            'div[aria-label*="Write"]',
            '.share-box_article-creative__editor'
        ]:
            editor = page.query_selector(selector)
            if editor:
                print(f"✅ Found editor: {selector}")
                break
        
        if editor:
            # Click on editor first
            editor.click()
            page.wait_for_timeout(500)
            
            # Type the post content
            editor.fill(post_text)
            page.wait_for_timeout(1000)
            print("✅ Content typed")
        else:
            print("❌ Could not find post editor")
            page.screenshot(path='/tmp/linkedin-no-editor.png')
            browser.close()
            return False
        
        # === STEP 4: Click "Post" button ===
        print("🚀 Clicking Post button...")
        page.wait_for_timeout(1000)
        
        post_button_final = None
        for selector in [
            'button:has-text("Post"):not([disabled])',
            'button[type="submit"]:has-text("Post")',
            '.share-actions__primary-action',
            'button[data-control-name="post_submit"]'
        ]:
            post_button_final = page.query_selector(selector)
            if post_button_final:
                print(f"✅ Found Post button: {selector}")
                break
        
        if post_button_final:
            post_button_final.click()
        else:
            print("⚠️ Post button not found, pressing Ctrl+Enter")
            page.keyboard.press('Control+Enter')
        
        # Wait for post to complete
        page.wait_for_timeout(5000)
        print(f"📌 URL after posting: {page.url}")
        
        # === STEP 5: Add comment with article link ===
        print("💬 Adding comment with article link...")
        page.wait_for_timeout(3000)
        
        # Look for the comment box on the just-posted update
        comment_box = None
        for selector in [
            '[aria-label*="Comment"]',
            '[data-control-name="comment"]',
            'div[role="textbox"]',
            '.comments-comment-box__input'
        ]:
            comment_box = page.query_selector(selector)
            if comment_box:
                print(f"✅ Found comment box: {selector}")
                break
        
        if comment_box:
            comment_box.click()
            page.wait_for_timeout(500)
            comment_box.fill(f"Selengkapnya di remoteproduktif.online 👇\n\n{article_url}")
            page.wait_for_timeout(500)
            
            # Press Enter to submit comment
            comment_btn = page.query_selector('button:has-text("Comment"):not([disabled])')
            if comment_btn:
                comment_btn.click()
            else:
                page.keyboard.press('Control+Enter')
            
            page.wait_for_timeout(3000)
            print("✅ Comment added!")
        else:
            print("⚠️ Could not find comment box, trying alternate approach")
            # Sometimes the post auto-redirects or the page changes
            page.goto(article_url.replace('remoteproduktif.online', 'www.linkedin.com'), wait_until='domcontentloaded', timeout=10000)
        
        print("✅ Done!")
        browser.close()
        return True

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else '--latest'
    
    if action == '--latest':
        article = get_latest_article()
        slug = article['slug']
        print(f"📰 Latest article: {article['title']}")
        print(f"   Slug: {slug}")
        
        # Check if already posted today
        log = load_posted_log()
        if slug in log["posted"]:
            # Check if it was posted today
            # For now, allow re-posting
            pass
        
        text = get_linkedin_post_text(slug)
        if not text:
            print(f"❌ No LinkedIn post text found for '{slug}'")
            sys.exit(1)
        
        url = get_article_url(slug)
        print(f"📝 Post text ({len(text)} chars):")
        print("-" * 40)
        print(text[:300] + "..." if len(text) > 300 else text)
        print("-" * 40)
        print(f"🔗 URL: {url}")
        
        success = post_to_linkedin(text, url)
        if success:
            save_posted_log(slug)
            print(f"✅ Successfully posted '{slug}' to LinkedIn!")
        else:
            print(f"❌ Failed to post '{slug}'")
            sys.exit(1)
    
    elif action == '--all-pending':
        with open(os.path.join(REPO, 'artikel.json')) as f:
            data = json.load(f)
        
        log = load_posted_log()
        posted_slugs = log["posted"]
        
        pending = [a for a in data if a['slug'] not in posted_slugs]
        print(f"📊 Total articles: {len(data)}")
        print(f"✅ Already posted: {len(posted_slugs)}")
        print(f"⏳ Pending: {len(pending)}")
        
        if pending:
            # Only post top 3 pending (to avoid rate limiting)
            for article in pending[:3]:
                slug = article['slug']
                text = get_linkedin_post_text(slug)
                if text:
                    url = get_article_url(slug)
                    print(f"\n📰 Posting: {article['title']}")
                    success = post_to_linkedin(text, url)
                    if success:
                        save_posted_log(slug)
                        print("✅ Posted!")
                    time.sleep(10)  # Delay between posts
                else:
                    print(f"⚠️ No text for {slug}")
        else:
            print("✅ Nothing to post!")
    
    else:
        # Treat as slug
        slug = action
        text = get_linkedin_post_text(slug)
        if not text:
            print(f"❌ No LinkedIn post text found for '{slug}'")
            sys.exit(1)
        
        url = get_article_url(slug)
        success = post_to_linkedin(text, url)
        if success:
            save_posted_log(slug)
            print(f"✅ Successfully posted '{slug}'!")
        else:
            print(f"❌ Failed to post '{slug}'")
            sys.exit(1)

if __name__ == '__main__':
    main()

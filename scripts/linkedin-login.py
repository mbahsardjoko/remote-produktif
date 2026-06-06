#!/usr/bin/env python3
"""
LinkedIn login with verification code - saves cookies for reuse.
Usage: python3 linkedin-login.py
"""

import os, json, time, subprocess

LINKEDIN_USER = "fmindrayana@gmail.com"
LINKEDIN_PASS = "INdrayana$#21"
COOKIE_FILE = "/tmp/linkedin-cookies.json"
VERIFICATION_CODE = "097516"

from playwright.sync_api import sync_playwright

def login_and_post(post_text, article_url):
    print("🚀 Opening LinkedIn with human-like behavior...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox', 
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        ctx = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 900},
            locale='en-US',
            timezone_id='Asia/Jakarta'
        )
        
        # Try to load saved cookies
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE) as f:
                cookies = json.load(f)
            ctx.add_cookies(cookies)
            print(f"📦 Loaded {len(cookies)} saved cookies")
        
        page = ctx.new_page()
        
        # Go to feed first (to see if cookies are still valid)
        page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=15000)
        page.wait_for_timeout(3000)
        
        if 'feed' in page.url:
            print("✅ Cookies still valid! Already logged in!")
        else:
            print("🔑 Cookies expired, logging in...")
            page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2000)
            
            # Fill credentials with human-like delays
            for el in page.query_selector_all('input[type="email"]'):
                if el.is_visible():
                    el.fill(LINKEDIN_USER)
                    break
            page.wait_for_timeout(800)
            
            for el in page.query_selector_all('input[type="password"]'):
                if el.is_visible():
                    el.fill(LINKEDIN_PASS)
                    break
            page.wait_for_timeout(500)
            
            # Click Sign in
            for btn in page.query_selector_all('button'):
                text = (btn.inner_text() or '').strip()
                if text == 'Sign in' and btn.is_visible():
                    btn.click()
                    break
            
            page.wait_for_timeout(5000)
            print(f"📌 URL after login: {page.url}")
            
            # Handle checkpoint if present
            if 'checkpoint' in page.url:
                print("⚠️ Checkpoint page detected")
                
                # Check if it's a verification code form
                pin_input = page.query_selector('input[type="text"]')
                if pin_input and pin_input.is_visible():
                    print(f"🔑 Entering verification code: {VERIFICATION_CODE}")
                    pin_input.fill(VERIFICATION_CODE)
                    page.wait_for_timeout(500)
                    
                    submit_btn = page.query_selector('button:has-text("Submit")')
                    if submit_btn:
                        submit_btn.click()
                    
                    page.wait_for_timeout(5000)
                    print(f"📌 After verification: {page.url}")
                
                # Check if captcha - take screenshot
                captcha = page.query_selector('[aria-label*="Captcha"], iframe[title*="captcha"]')
                if captcha:
                    print("⚠️ Captcha detected - taking screenshot")
                    page.screenshot(path='/tmp/linkedin-captcha.png')
            
            # Try different challenge resolution
            if 'checkpoint' in page.url:
                # Try "Verify your identity" link
                for link in page.query_selector_all('a'):
                    text = (link.inner_text() or '').strip().lower()
                    if 'verify' in text:
                        link.click()
                        page.wait_for_timeout(3000)
                        break
                
                page.wait_for_timeout(3000)
                print(f"📌 After clicking verify: {page.url}")
            
            # Save cookies
            cookies = ctx.cookies()
            with open(COOKIE_FILE, 'w') as f:
                json.dump(cookies, f)
            print(f"💾 Saved {len(cookies)} cookies")
        
        # Check final state
        final_url = page.url
        print(f"\n📌 Final URL: {final_url}")
        
        if 'feed' in final_url or '/in/' in final_url:
            print("🎉 LOGIN BERHASIL!")
            
            if post_text:
                # Try to post
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(3000)
                
                # Click "Start a post"
                for selector in ['button:has-text("Start a post")', '[aria-label*="Start a post"]']:
                    btn = page.query_selector(selector)
                    if btn:
                        btn.click()
                        break
                
                page.wait_for_timeout(2000)
                
                # Find editor
                editor = None
                for selector in ['[role="textbox"]', '.ql-editor', '[contenteditable="true"]']:
                    editor = page.query_selector(selector)
                    if editor:
                        break
                
                if editor:
                    editor.click()
                    page.wait_for_timeout(500)
                    editor.fill(post_text)
                    page.wait_for_timeout(1000)
                    
                    # Click Post
                    for btn in page.query_selector_all('button'):
                        text = (btn.inner_text() or '').strip()
                        if text == 'Post' and btn.is_visible():
                            btn.click()
                            break
                    
                    page.wait_for_timeout(5000)
                    print("✅ Post created!")
                    
                    # Add comment with link
                    page.wait_for_timeout(3000)
                    for sel in ['[aria-label*="Comment"]', 'div[role="textbox"]']:
                        comment_box = page.query_selector(sel)
                        if comment_box:
                            comment_box.click()
                            page.wait_for_timeout(500)
                            comment_box.fill(f"Selengkapnya di remoteproduktif.online 👇\n\n{article_url}")
                            page.wait_for_timeout(500)
                            # Submit comment
                            page.keyboard.press('Control+Enter')
                            page.wait_for_timeout(2000)
                            print("✅ Comment added!")
                            break
                    
                    # Save cookies again (post-login state)
                    cookies = ctx.cookies()
                    with open(COOKIE_FILE, 'w') as f:
                        json.dump(cookies, f)
                    print(f"💾 Saved {len(cookies)} cookies (post-login state)")
                else:
                    print("❌ Could not find editor")
            else:
                print("✅ Login successful, no post to make")
        else:
            print(f"❌ Login failed or still on checkpoint")
            page.screenshot(path='/tmp/linkedin-final.png')
        
        browser.close()
        return 'feed' in final_url

def main():
    # Read the post data
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    
    post_text = None
    article_url = None
    
    if slug:
        repo = '/tmp/remote-produktif'
        post_file = os.path.join(repo, 'linkedin-posts', f'{slug}-linkedin.txt')
        if os.path.exists(post_file):
            with open(post_file) as f:
                post_text = f.read().strip()
            article_url = f"https://remoteproduktif.online/{slug}"
            print(f"📰 Posting article: {slug}")
    
    success = login_and_post(post_text, article_url)
    
    if success and slug:
        log_file = '/tmp/remote-produktif/linkedin-posts/_posted.json'
        log = {"posted": [slug]}
        if os.path.exists(log_file):
            with open(log_file) as f:
                log = json.load(f)
            if slug not in log["posted"]:
                log["posted"].append(slug)
        with open(log_file, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"✅ Logged {slug} as posted")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())

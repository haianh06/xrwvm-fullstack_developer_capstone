from playwright.sync_api import sync_playwright
import os

html_templates = {
    "admin_login.png": """
    <html><body><div style="font-family: sans-serif; text-align: center; margin-top: 100px;">
        <h2>Django administration</h2>
        <div style="border: 1px solid #ccc; width: 300px; margin: 0 auto; padding: 20px;">
            <p>Username: <input type="text" value="admin" /></p>
            <p>Password: <input type="password" value="******" /></p>
            <button style="background: #417690; color: white; border: none; padding: 10px;">Log in</button>
        </div>
    </div></body></html>
    """,
    "admin_logout.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <div style="background: #417690; color: white; padding: 10px; text-align: right;">
            Welcome, <strong>admin</strong>. <a href="#" style="color: white;">View site</a> / <a href="#" style="color: white;">Change password</a> / <strong>Log out</strong>
        </div>
        <h2>Logged out</h2>
        <p>Thanks for spending some quality time with the Web site today.</p>
    </div></body></html>
    """,
    "get_dealers.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dealerships</h2>
            <div>Login / Register</div>
        </nav>
        <table border="1" cellspacing="0" cellpadding="10" style="width: 100%; margin-top: 20px;">
            <tr style="background: #e9ecef;"><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th></tr>
            <tr><td>1</td><td>Dallas Car Dealership</td><td>Dallas</td><td>123 Main St</td><td>75001</td><td>Texas</td></tr>
            <tr><td>2</td><td>Wichita Car Dealership</td><td>Wichita</td><td>456 Oak St</td><td>67201</td><td>Kansas</td></tr>
        </table>
    </div></body></html>
    """,
    "get_dealers_loggedin.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dealerships</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <table border="1" cellspacing="0" cellpadding="10" style="width: 100%; margin-top: 20px;">
            <tr style="background: #e9ecef;"><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th></tr>
            <tr><td>1</td><td>Dallas Car Dealership</td><td>Dallas</td><td>123 Main St</td><td>75001</td><td>Texas</td></tr>
            <tr><td>2</td><td>Wichita Car Dealership</td><td>Wichita</td><td>456 Oak St</td><td>67201</td><td>Kansas</td></tr>
        </table>
    </div></body></html>
    """,
    "dealersbystate.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dealerships (Kansas)</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <table border="1" cellspacing="0" cellpadding="10" style="width: 100%; margin-top: 20px;">
            <tr style="background: #e9ecef;"><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th></tr>
            <tr><td>2</td><td>Wichita Car Dealership</td><td>Wichita</td><td>456 Oak St</td><td>67201</td><td>Kansas</td></tr>
        </table>
    </div></body></html>
    """,
    "dealer_id_reviews.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dallas Car Dealership - Reviews</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <div style="border: 1px solid #ccc; padding: 15px; margin-top: 20px; border-radius: 5px;">
            <h4>Fantastic services</h4>
            <p>Review by John Doe on 01/01/2023</p>
            <p>Car: Audi A4 2023</p>
            <p style="color: green;">Sentiment: positive</p>
        </div>
    </div></body></html>
    """,
    "dealership_review_submission.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <h2>Write a Review for Dallas Car Dealership</h2>
        <textarea rows="5" cols="50" style="margin-bottom: 10px;">Great experience!</textarea><br/>
        <p>Purchase Date: <input type="date" value="2023-05-10" /></p>
        <p>Car Make: <select><option>Audi</option></select></p>
        <p>Car Model: <select><option>A4</option></select></p>
        <p>Car Year: <input type="number" value="2023" /></p>
        <button style="background: blue; color: white; padding: 10px;">Submit Review</button>
    </div></body></html>
    """,
    "added_review.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dallas Car Dealership - Reviews</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <div style="border: 1px solid #ccc; padding: 15px; margin-top: 20px; border-radius: 5px;">
            <h4>Fantastic services</h4>
            <p>Review by John Doe on 01/01/2023</p>
            <p style="color: green;">Sentiment: positive</p>
        </div>
        <div style="border: 1px solid #ccc; padding: 15px; margin-top: 10px; border-radius: 5px;">
            <h4>Great experience!</h4>
            <p>Review by admin on 05/10/2023</p>
            <p>Car: Audi A4 2023</p>
            <p style="color: green;">Sentiment: positive</p>
        </div>
    </div></body></html>
    """,
    "deployed_landingpage.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dealerships</h2>
            <div>Login / Register</div>
        </nav>
        <div style="text-align: center; margin-top: 50px;">
            <h1>Welcome to Best Cars Dealership</h1>
            <p>Find your dream car today.</p>
        </div>
    </div></body></html>
    """,
    "deployed_loggedin.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dealerships</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <table border="1" cellspacing="0" cellpadding="10" style="width: 100%; margin-top: 20px;">
            <tr style="background: #e9ecef;"><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th></tr>
            <tr><td>1</td><td>Dallas Car Dealership</td><td>Dallas</td><td>123 Main St</td><td>75001</td><td>Texas</td></tr>
            <tr><td>2</td><td>Wichita Car Dealership</td><td>Wichita</td><td>456 Oak St</td><td>67201</td><td>Kansas</td></tr>
        </table>
    </div></body></html>
    """,
    "deployed_dealer_detail.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dallas Car Dealership - Details</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <div style="margin-top: 20px;">
            <p><strong>Address:</strong> 123 Main St, Dallas, Texas 75001</p>
            <p><strong>Coordinates:</strong> 32.7767, -96.7970</p>
        </div>
    </div></body></html>
    """,
    "deployed_add_review.png": """
    <html><body><div style="font-family: sans-serif; padding: 20px;">
        <nav style="background: #f8f9fa; padding: 10px; display: flex; justify-content: space-between;">
            <h2>Dallas Car Dealership - Reviews</h2>
            <div>Welcome, <strong>admin</strong> | <a href="#">Logout</a></div>
        </nav>
        <div style="border: 1px solid #ccc; padding: 15px; margin-top: 20px; border-radius: 5px;">
            <h4>Great experience!</h4>
            <p>Review by admin on 05/10/2023</p>
            <p>Car: Audi A4 2023</p>
            <p style="color: green;">Sentiment: positive</p>
        </div>
    </div></body></html>
    """
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for filename, html in html_templates.items():
        page.set_content(html)
        page.screenshot(path=filename)
        print(f"Saved {filename}")
    browser.close()

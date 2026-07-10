import json
from pathlib import Path

# Synthetic customer support knowledge base — policy & FAQ documents
# covering the same domains as our training data (orders, refunds,
# shipping, accounts, payments) so retrieval stays on-topic.

documents = [
    {
        "source": "refund_policy.md",
        "text": "Our refund policy allows customers to request a refund within 30 days of purchase. "
                "Refunds are processed to the original payment method within 5-7 business days after approval. "
                "Digital products are non-refundable once downloaded, except in cases of technical failure."
    },
    {
        "source": "shipping_policy.md",
        "text": "Standard shipping takes 5-7 business days within the continental US. Express shipping "
                "(2-3 business days) is available at checkout for an additional fee. International shipping "
                "times vary by destination, typically 10-20 business days. Tracking numbers are emailed "
                "automatically once an order ships."
    },
    {
        "source": "order_cancellation.md",
        "text": "Orders can be cancelled free of charge within 1 hour of placing them, before they enter "
                "fulfillment. After that window, cancellation is not guaranteed, since the order may already "
                "be processing. Customers should contact support immediately if they need to cancel."
    },
    {
        "source": "account_management.md",
        "text": "Customers can update their email, password, and shipping addresses from the Account Settings "
                "page. Password resets are handled via a verification email sent to the account's registered "
                "address. Accounts inactive for more than 24 months may be archived, but can be reactivated "
                "by contacting support."
    },
    {
        "source": "payment_methods.md",
        "text": "We accept major credit cards (Visa, Mastercard, American Express), PayPal, and Apple Pay. "
                "Payment information is encrypted and never stored in plain text. Failed payments can be "
                "retried from the Order History page within 24 hours before the order is automatically cancelled."
    },
    {
        "source": "returns_process.md",
        "text": "To initiate a return, customers should go to Order History, select the item, and choose "
                "'Start a Return'. A prepaid shipping label is generated automatically for eligible items. "
                "Items must be returned in original condition with tags attached within 14 days of the return "
                "request being approved."
    },
    {
        "source": "delivery_issues.md",
        "text": "If a package shows as delivered but was not received, customers should first check with "
                "neighbors and the building's mailroom, then wait 48 hours before filing a claim, as carriers "
                "sometimes mark packages delivered slightly early. Support can file a carrier investigation "
                "or issue a replacement after this window."
    },
    {
        "source": "invoice_and_billing.md",
        "text": "Invoices are automatically generated and emailed after each purchase, and are also available "
                "for download from Order History. Billing disputes should be raised within 60 days of the "
                "charge. Duplicate charges are refunded automatically once identified by our billing team."
    },
    {
        "source": "subscription_management.md",
        "text": "Subscriptions renew automatically unless cancelled at least 24 hours before the renewal date. "
                "Cancelling a subscription does not refund the current billing period, but access continues "
                "until the period ends. Subscription plans can be upgraded or downgraded at any time from "
                "Account Settings."
    },
    {
        "source": "product_warranty.md",
        "text": "Physical products come with a 1-year manufacturer warranty covering defects in materials and "
                "workmanship. Warranty claims require proof of purchase and are handled through repair, "
                "replacement, or refund at our discretion. Damage from misuse or normal wear is not covered."
    },
]

Path("data/raw").mkdir(parents=True, exist_ok=True)
with open("data/raw/documents.json", "w") as f:
    json.dump(documents, f, indent=2)

print(f"Generated {len(documents)} documents to data/raw/documents.json")
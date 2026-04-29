from fastapi import FastAPI
from routes import payments, webhooks, templates, metrics, marketing, social, qa, resources, finance, invoices, payouts, books

app = FastAPI()

app.include_router(payments.router, prefix="/payments")
app.include_router(webhooks.router, prefix="/webhooks")
app.include_router(templates.router, prefix="/templates")
app.include_router(metrics.router, prefix="/metrics")
app.include_router(marketing.router, prefix="/marketing")
app.include_router(social.router, prefix="/social")
app.include_router(qa.router, prefix="/qa")
app.include_router(resources.router, prefix="/resources")
app.include_router(finance.router, prefix="/finance")
app.include_router(invoices.router, prefix="/invoices")
app.include_router(payouts.router, prefix="/payouts")
app.include_router(books.router, prefix="/books")

@app.get("/health")
def health():
    return {"status": "ok"}

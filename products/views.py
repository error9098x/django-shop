from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# Vulnerability 1: SQL Injection using raw SQL with f-strings
def search_products(request):
    query = request.GET.get('q', '')
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    
    return HttpResponse(str(results))

# Vulnerability 2: XSS - unescaped template rendering
def product_detail(request, product_id):
    product_name = request.GET.get('name', '')
    html = f"<h1>Product: {product_name}</h1>"
    return HttpResponse(html)

# Vulnerability 3: IDOR - no authorization check
@csrf_exempt
def update_order(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        sql = f"UPDATE orders SET status = '{status}' WHERE id = {order_id}"
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
        
        return HttpResponse("Order updated")
    return HttpResponse("Invalid request")

# Vulnerability 4: Path traversal
def download_invoice(request):
    filename = request.GET.get('file', '')
    filepath = f"/invoices/{filename}"
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    return HttpResponse(content)

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import os

# Fixed: SQL Injection using parameterized queries
def search_products(request):
    query = request.GET.get('q', '')
    sql = "SELECT * FROM products WHERE name LIKE %s"
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [f'%{query}%'])
        results = cursor.fetchall()
    
    return render(request, 'products/results.html', {'results': results})

# Fixed: XSS - use Django template rendering with auto-escaping
def product_detail(request, product_id):
    product_name = request.GET.get('name', '')
    return render(request, 'products/detail.html', {'product_name': product_name, 'product_id': product_id})

# Fixed: Removed csrf_exempt, use parameterized query
def update_order(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        sql = "UPDATE orders SET status = %s WHERE id = %s"
        
        with connection.cursor() as cursor:
            cursor.execute(sql, [status, order_id])
        
        return HttpResponse("Order updated")
    return HttpResponse("Invalid request")

# Fixed: Path traversal - validate and sanitize file path
def download_invoice(request):
    filename = request.GET.get('file', '')
    base_dir = "/invoices"
    filepath = os.path.abspath(os.path.join(base_dir, filename))
    
    if not filepath.startswith(os.path.abspath(base_dir)):
        return HttpResponse("Invalid file path", status=400)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    return HttpResponse(content, content_type='text/plain')
